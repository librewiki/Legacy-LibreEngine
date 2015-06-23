__author__ = '이츠레아,나유타'
from flask import Flask
from LibreEngine.conf import config


app = Flask(__name__)
app.config['NAME'] = config.default_config.NAME


from LibreEngine.include import routes