__author__ = '이츠레아,나유타'
from LibreEngine import app
from LibreEngine.include.models import *
from flask import render_template, request, flash, session, url_for, redirect

@app.route('/')
def index():
    return redirect(url_for('wiki'))

@app.route('/wiki')
def wiki():
    return render_template('wiki/wiki.html')

@app.route('/testdb')
def testdb():
    return db.session.query

@app.route('/wikitext/<int:page_num>')
def wikipage_num(page_num):
    page = WikiText.query.filter(WikiText.id == page_num).first()
    if page:
        return page.text
    else:
        return "No Such Page"



