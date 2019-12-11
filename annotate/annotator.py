import sys
import os
import argparse
import pickle

import ahocorasick

from utils.utils import check_file

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ac_path', type=str, default='../data/ac.pickle', help='Path of aho-corasick.')
    parser.add_argument('--mean_path', type=str, default='../data/means.pickle', help='Path of means.')
    args = parser.parse_args()
    return args


class Annotator:
    def __init__(self, args):
        check_file(args.ac_path)
        check_file(args.mean_path)
        with open(args.ac_path, 'rb') as infile:
            ac = pickle.load(infile)
        if isinstance(ac, ahocorasick.Automaton):
            self.ac = ac
        else:
            raise TypeError("{} must be ahocorasick.Automaton".format(args.ac_path))
        with open(args.mean_path, 'rb') as infile:
            mean = pickle.load(infile)
        if isinstance(mean, list) and all(isinstance(elem, str) for elem in mean):
            self.mean = mean
        else:
            raise TypeError("{} must be list of str".format(args.mean_path))

    def annotate(self, text):
        if not text:
            return None
        assert type(text) == str

        note = list()
        for end_index, (insert_order, original_value) in self.ac.iter(text):
            start_index = end_index - len(original_value) + 1
            # print(((start_index, end_index), (insert_order, original_value)))
            note.append(((start_index, end_index), (insert_order, original_value)))
            assert text[start_index:start_index + len(original_value)] == original_value

        if len(note) > 1:
            new_note = list()
            note.append(((0, 0), (-1, 'watch_dog')))
            p1, p2 = 0, 1  # set two pointer
            while p2 < len(note):
                p1_item = note[p1]
                p2_item = note[p2]
                p1_range = set(range(p1_item[0][0], p1_item[0][1] + 1))
                p2_range = set(range(p2_item[0][0], p2_item[0][1] + 1))
                overlap = p1_range.intersection(p2_range)
                if not overlap:
                    new_note.append(p1_item)
                    p1 = p2
                else:
                    p1_len = p1_item[0][1] - p1_item[0][0]
                    p2_len = p2_item[0][1] - p2_item[0][0]
                    if p1_len < p2_len:
                        p1 = p2
                p2 += 1
            note = new_note

        out_text = ''

        if note:
            index = 0
            for nt in note:
                (l, r), (idx, w) = nt
                out_text += text[index:l] + '[{}]'.format(w) + '({})'.format(self.mean[idx])
                index = r + 1
        else:
            out_text = text

        out_text += ' 补充语料 https://wj.qq.com/s2/5170542/a685'
        return out_text


if __name__ == '__main__':
    args = _get_parser()
    annotator = Annotator(args)
    in_text = '中方跟美方就韩春雨团队非主观造假事件充分交换了意见，测试愉快。'
    res = annotator.annotate(in_text)
    print(res)
