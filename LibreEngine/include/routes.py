# -*- coding: utf-8 -*-

__author__ = '이츠레아, 나유타'
from flask import render_template, request, flash, session, url_for, redirect
from LibreEngine.include.models import *
from LibreEngine.lib.parsing import *
import pymysql

@app.route('/')
def main():
    page_role = "메인페이지"
    return redirect(url_for('read', name='FrontPage'))
@app.route('/<string:page>')
def index(page):
    page_role = "프론트페이지"
    front = "/wiki/FrontPage"
    if page == front:
        return redirect(url_for('read', name='FrontPage'))
    else:
        return redirect(url_for('read', name='FrontPage'))
@app.route('/wiki/<string:name>')
def read(name):
    page_role = "문서페이지"
    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()

    unwritenpage = "<p>해당 문서를 찾을수 없습니다.</p>" + "<a href=" + url_for('edit', name = newname) + ">" + "해당 문서를 만드시겠습니까?" + "</a>"
    pagedocument = "<h1 class=\"title\">" + newname + "</h1>"
    if page:
        newpage = page.text.replace("]]", "]] ")

        source = mwtohtmlrender(newpage)

        return render_template('wiki/wiki.html', name=name, contents=source, documents=pagedocument)
    else:
        return render_template('wiki/wiki.html', name=name, contents=unwritenpage, documents=pagedocument)

@app.route('/edit/<string:name>')
def edit(name):
    page_role = "편집 페이지"
    detourtext = detour(page_role)
    #detourstatus = 0
    documents = name

    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()

    if page:
        rendered = mwtomwrender(page.text)

        return render_template('wiki/edit.html', name=name, contents=rendered, documents=name)
    else:
        return render_template('wiki/edit.html', name=name, contents=detourtext)

@app.route("/commit/<string:name>")
def commit(name):


    return render_template('commit/' + name)


'''
@app.route("/jsraw/<string:name>")
def js_raw(name):
    page_role = "글쓰기 페이지"
    detourtext = detour(page_role)

    detourstatus = 0

    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()
    return page
'''


@app.route('/search/<string:name>')
def search(name):

    query = dbtitlesearch(name)


    if query:
        return render_template('wiki/wiki.html', name=name, contents=query)
    else:
        return render_template('wiki/wiki.html', name=name, contents="Something's wrong!")
