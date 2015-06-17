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

@app.route('/wiki/<int:page_num>')
def page_view(page_num):
    page = WikiPage.query.filter(WikiPage.id == page_num).first()
    if page:
        return page.text
    else:
        return "No such page"

if(__name__ == "__main__"):
    app.run(conf.HOST,conf.PORT)