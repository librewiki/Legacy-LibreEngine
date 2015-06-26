__author__ = '이츠레아,nayuta'
from LibreEngine.lib.dbConnect import *
from flask import url_for
from pypandoc import convert
import pymysql




class WikiText(db.Model):

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Unicode(convert_unicode=True), unique=True)
    rev = db.Column(db.Integer)
    text = db.Column(db.Unicode(convert_unicode=True))
    date = db.Column(db.Integer)

def detour(page_role):
    editpage = str(page_role)
    detour = "<p>현재 " + editpage + "(은)는 아직 준비중입니다!</p>" + "<a href=" + url_for('main') + ">메인페이지</a>로 돌아가시겠습니까?"
    return detour


def mwtohtmlrender(mwtext):


    output = convert(mwtext, 'html', format='mediawiki' )

    scharfor = output.count('--')

    while scharfor > 0:
        outputnew = output.replace('--','<s>',1)
        output = outputnew
        outputnew = output.replace('--','</s> ',1)
        output = outputnew
        scharfor = output.count('--')
    rendered = output

    return rendered

def mwtomwrender(mwtext):



    output = convert(mwtext, 'mediawiki', format='mediawiki' )

    rendered = output
    return rendered

def dbtitlesearch(target):






    searchname = "'%"+target+"%'"

    connection = pymysql.connect(host='sv3.al.gl',
                                 user='libredev',
                                 passwd='libre_dev',
                                 db='libredev',
                                 charset='utf8mb4')

    cursor = connection.cursor()

    sql = "SELECT * FROM `documents` WHERE `document` LIKE " + searchname + " ORDER BY `document` ASC;"

    cursor.execute(sql)

    result = cursor.fetchall()
    if result:
        return result
    else:
        return "somthing's wrong"



