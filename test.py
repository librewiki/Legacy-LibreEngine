import os

templates = {}
allowed_tags = []
allowed_self_closing_tags = []
allowed_attributes = []
interwiki = {}
namespaces = {}

from preprocessor import make_parser
preprocessor = make_parser(templates)

from html import make_parser
parser = make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)

source = open("test.txt")

preprocessed_text = preprocessor.parse(source)
output = parser.parse(preprocessed_text.leaves())
