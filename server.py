__author__ = 'seyriz'

from flask import *
from conf.config import *
import pymysql

conn = pymysql.connect(host='sv3.al.gl', port=3306, user='libredev', passwd='libre_dev', db='libredev', charset='utf8')
cur = conn.cursor()


def printDATABASES():
	cur.execute("SHOW DATABASES;")

	for row in cur:
		print(row[0])


app = Flask(__name__)
conf = default_config

@app.route('/')
def index():
    return printDATABASES


if(__name__ == "__main__"):
    app.run(conf.HOST,conf.PORT)
