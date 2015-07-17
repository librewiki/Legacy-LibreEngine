# -*- coding: utf-8 -*-

__author__ = '이츠레아, 나유타'
from flask import render_template, request, flash, session, url_for, redirect
from LibreEngine.include.models import *
from LibreEngine.lib.parsing import *



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

@app.route('/wiki/<path:name>')
def read(name):
    page_role = "문서페이지"
    newname = name.replace("_", " ")
    #page_title = WikiInfo.query.filter(WikiInfo.page_title == newname).first()

    getpageid = WikiInfo.query.filter(WikiInfo.page_title == newname).first()
    print(getpageid.page_id)

    page = WikiText.query.filter(WikiText.old_id == getpageid.page_id).first()


    content = page.old_text


    unwritenpage = "<p>해당 문서를 찾을수 없습니다.</p>" + "<a href=" + url_for('edit', name = newname) + ">" + "해당 문서를 만드시겠습니까?" + "</a>"
    pagedocument = "<h1 class=\"title\">" + newname + "</h1>"
    if page:
        #newpage = page.replace("]]", "]] ")
        source = content.decode("UTF-8")
        #source = mwtohtmlrender(newpage)

        return render_template('wiki/wiki.html', name=name, contents=source, documents=pagedocument)
    else:
        return render_template('wiki/wiki.html', name=name, contents=unwritenpage, documents=pagedocument)


@app.route('/edit/<path:name>')
def edit(name):
    page_role = "편집 페이지"
    detourtext = detour(page_role)
    #detourstatus = 0
    #documents = name

    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()

    if page:
        #rendered = mwtomwrender(page.text)

        return render_template('wiki/edit.html', name=name, contents=page.text, documents=name)
    else:
        return render_template('wiki/edit.html', name=name, contents=detourtext)

@app.route("/commit/<path:name>")
def commit(name):


    return render_template('commit/' + name)


'''
@app.route("/jsraw/<path:name>")
def js_raw(name):
    page_role = "글쓰기 페이지"
    detourtext = detour(page_role)

    detourstatus = 0

    newname = name.replace("_", " ")
    page = WikiText.query.filter(WikiText.document == newname).first()
    return page
'''


@app.route('/search/<path:name>')
def search(name):

    query = dbtitlesearch(name)


    if query:
        return render_template('wiki/wiki.html', name=name, contents=query)
    else:
        return render_template('wiki/wiki.html', name=name, contents="Something's wrong!")

@app.route('/namutolibre')
def namutolibre():



    return render_template('wiki/namutolibre.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():

    if request.method == 'POST':
        test = request.form.get('namu-mark', type=str)
        text = namutolibresyntax(test)
        rendered = mwtohtmlrender(text)
        return render_template('wiki/convert.html',text=text,test=test, rendered=rendered)
    else :
        return render_template('wiki/wiki.html')

@app.route('/htmltolibre', methods=['GET', 'POST'])
def htolconvertor():

    if request.method == 'POST':
        test = request.form.get('namu-mark', type=str)
        text = htmltolibre(test)
        text = re.sub("(<.*?>)", "", text)

        refcount = text.count('[ref]')
        while refcount > 0:
            text = text.replace('[ref]','<ref>',1)
            text = text.replace('[/ref]','</ref>',1)
            refcount = text.count('[ref]')

        scharfor = text.count('--')

        while scharfor > 0:
            text = text.replace('--','<del>',1)

            text = text.replace('--','</del  > ',1)

            scharfor = text.count('--')


        rendered = mwtohtmlrender(text)
        return render_template('wiki/htmltolibre.html',text=text,test=test, rendered=rendered)
    else :
        return render_template('wiki/htmltolibre.html')



