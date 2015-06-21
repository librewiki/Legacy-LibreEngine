# -*- coding: utf-8 -*-

__author__ = '이츠레아, 나유타'
from flask import render_template, request, flash, session, url_for, redirect
from LibreEngine.include.models import *
from LibreEngine.include.parsing import mwrender



@app.route('/')
def index():
    return redirect(url_for('read', name='frontpage'))

@app.route('/wiki/<string:name>')
def read(name):
    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()

    unwritenpage = "<p>해당문서를 찾을수 없습니다.</p>"
    pagedocument = "<h1 class=\"title\">" + newname + "</h1>"
    if page:

        source = mwrender(page.text)
        return render_template('wiki/wiki.html', name=name, contents=source, documents=pagedocument)
    else:
        return render_template('wiki/wiki.html', name=name, contents=unwritenpage, documents=pagedocument)

@app.route('/wikitext/<int:page_num>')
def wikipage_num(page_num):
    page = WikiText.query.filter(WikiText.id == page_num).first()
    if page:
        return page.text
    else:
        return "No Such Page"



