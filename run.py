import argparse

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from annotate.annotator import Annotator

app = Flask(__name__)
api = Api(app)


def _local_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ac_path', type=str, default='./data/ac.pickle', help='Path of aho-corasick.')
    parser.add_argument('--mean_path', type=str, default='./data/means.pickle', help='Path of means.')
    args = parser.parse_args()
    return args


def _http_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('text', type=str, help='Input text.')
    parser.add_argument('type', type=str, help='Input text type.')
    args = parser.parse_args()
    return args


class TextAnnotator(Resource):
    def __init__(self, args=_local_parser()):
        self.annotator = Annotator(args)

    def put(self):
        # text = request.form['text']
        args = _http_parser()
        text = args['text']
        return {'annotated': self.annotator.annotate(text)}


api.add_resource(TextAnnotator, '/annotation')


if __name__ == '__main__':
    app.run(debug=True)
