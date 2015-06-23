__author__ = '이츠레아,나유타'
from flask import Flask
from flask.ext.elasticsearch import FlaskElasticsearch
from LibreEngine.conf import config

es = FlaskElasticsearch()

app = Flask(__name__)
es = FlaskElasticsearch(app)
app.config['NAME'] = config.default_config.NAME

es.init_app(app)

from LibreEngine.include import routes