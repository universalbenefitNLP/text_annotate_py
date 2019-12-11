import sys
import os
import argparse
import pickle

import ahocorasick

from utils.utils import check_file, ensure_dir

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', type=str, default='../data/synonym', help='Directory of input file.')
    parser.add_argument('--output', type=str, default='../data', help='Directory to save output file.')
    parser.add_argument('--ac_name', type=str, default='ac.pickle', help='Filename of aho-corasick.')
    parser.add_argument('--mean_name', type=str, default='means.pickle', help='Filename of means.')
    args = parser.parse_args()
    return args


def builder():
    args = _get_parser()
    check_file(args.infile)
    ensure_dir(args.output)

    A = ahocorasick.Automaton()
    origin, annotation = list(), list()

    infile = open(args.infile, 'r', encoding='utf-8')
    for line in infile:
        line = line.rstrip()
        if not line:
            continue
        phrase, means = line.split(':::')
        if not phrase or not means:
            continue
        origin.append(phrase)
        annotation.append(means)

    infile.close()
    assert len(origin) == len(annotation)

    for idx, phrase in enumerate(origin):
        A.add_word(phrase, (idx, phrase))

    A.make_automaton()

    ac_name = os.path.join(args.output, args.ac_name)
    means = os.path.join(args.output, args.mean_name)
    with open(ac_name, 'wb') as outfile:
        pickle.dump(A, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    with open(means, 'wb') as outfile:
        pickle.dump(annotation, outfile, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    builder()
