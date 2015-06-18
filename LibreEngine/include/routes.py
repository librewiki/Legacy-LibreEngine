__author__ = '이츠레아'
from LibreEngine import app
from flask import render_template, request, flash, session, url_for, redirect

@app.route('/')
def index():
    return redirect(url_for('wiki'))

@app.route('/wiki')
def wiki():
    return render_template('wiki/wiki.html')