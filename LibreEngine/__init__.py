__author__ = 'Wonwoo'
from flask import Flask
from LibreEngine.conf import config

app = Flask(__name__)
app.config['NAME'] = config.default_config.NAME

from LibreEngine.include import routes