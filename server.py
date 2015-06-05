__author__ = 'seyriz'

from flask import *
from conf.config import *
from conf.database import *
from lib.dbConnect import *

conf = default_config

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if(__name__ == "__main__"):
    app.run(conf.HOST,conf.PORT)