__author__ = '이츠레아'
from LibreEngine import app
from flask import render_template, request, flash, session, url_for, redirect
from LibreEngine.conf import config

app.config['NAME'] = config.default_config.NAME

@app.route('/')
def index():
    return redirect(url_for('wiki'))

@app.route('/wiki')
def wiki():
    return render_template('wiki/wiki.html')