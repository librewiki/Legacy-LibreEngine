# -*- coding: utf-8 -*-
__author__ = '나유타'

from pypandoc import convert
import pymysql
#from pymysqlreplication import BinLogStreamReader
import re

def htmltolibre(mwtext):

    mwtext = mwtext.replace('<del>','--')
    mwtext = mwtext.replace('</del>','--')
    mwtext = mwtext.replace('[편집]','')
    mwtext = mwtext.replace('/w/','/wiki/')
    mwtext = re.sub('\<a class\=\"wiki\-fn\-content\" title\=\"(.*?)\" href\=\"\#fn(.*?)\"\>\<span class\=\"target\" id=\"rfn(.*?)\"\>\<\/span\>\[(.*?)\]\<\/a\>', r'[ref] \1 [/ref]',mwtext)
    mwtext = re.sub('\<span class\=\"footnote\-list\"\>.*?\<\/span\>','<del>\1</del>',mwtext)
    mwtext = re.sub('\<span class\=\"wiki\-edit\-section\"\>.*?\<\/span\>','',mwtext)
    mwtext = re.sub('\<span class\=\"target\".*?\<\/span\>','<ref>\1</ref>',mwtext)
    output = convert(mwtext, 'mediawiki', format='html')

    '''
    refcount = output.count('[ref]')
    while refcount > 0:
        output = output.replace('[ref]','<ref>',1)
        output = output.replace('[/ref]','</ref>',1)
        refcount = output.count('[ref]')
    '''
    '''
    output = output.replace("<","&lt;")
    output = output.replace(">","&gt;")
    output = output.replace("\"","$quot;")
    '''

    rendered = output

    return rendered



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



def namutolibresyntax(target):

    output = target
    #a라고쓰고b라고읽는다 인듯
    #fuck = bool(re.search('\[\[(.*?)\|(.*?)\]\]',output))

    #if bool(re.search('\[\[(.*?)\|(.*?)\]\]',output)) == True:
    output = re.sub(u"\[\[(.*?)\|(.*?)\]\]",r"[[\1|\2]]",output)

    #if bool(re.search('\[\[wiki\:\"(.*?)\" (.*?)\]\]',output)) == True:
    output = re.sub(u"\[\[wiki\:\"(.*?)\" (.*?)\]\]",r"[[\1|\2]]",output)

    #if bool(re.search('\[(.*?)\|(.*?)\]',output)) == True:
    output = re.sub(u"\[(.*?)\|(.*?)\]",r"[\1|\2]",output)

    #주소|예제

    #if bool(re.search('\[\[http(.*?)\|(.*?)\]\]',output)) == True:
    output = re.sub(u"\[\[http(.*?)\|(.*?)\]\]",r"[http\1 \2]",output)


    #if bool(re.search('\[\[http(.*?) (.*?)\]\]',output)) == True:
    output = re.sub(u"\[\[http(.*?) (.*?)\]\]",r"[http\1 \2]",output)
    '''
    if bool(re.search('\[http(.*?)\|(.*?)',output)) == True:
        output = re.sub(u"\[http(.*?)\|(.*?)\]",r"[http\1 \2]",output)
    '''
    #취소선
    delcount = output.count('~~')
    while delcount > 0:
        newoutput = output.replace('~~','<del>',1)
        output = newoutput
        newoutput = output.replace('~~','</del>',1)
        output = newoutput
        delcount = output.count('~~')
    ''' # 알고리즘상 문제로 주석처리함.
    if bool(re.search('~~(.*?)~~',output)) == True:
        output = re.sub(u"~~(.*?)~~",r"{{~~|\1}}",output)
    '''
    delcount = output.count('--')
    while delcount > 0:
        newoutput = output.replace('--','<del>',1)
        output = newoutput
        newoutput = output.replace('--','</del>',1)
        output = newoutput
        delcount = output.count('--')
    ''' # 알고리즘상 문제로 주석처리함.
    if bool(re.search('--(.*?)--',output)) == True:
        newoutput = re.sub(u"--(.*?)--",r"{{--|\1}}",output)
        output = newoutput
    '''
    #윗첨자
    supcount = output.count('^^')
    while supcount > 0:
        newoutput = output.replace('^^','<sup>',1)
        output = newoutput
        newoutput = output.replace('^^','</sup>',1)
        output = newoutput
        supcount = output.count('^^')
    ''' 알고리즘상 문제로 주석처리함. 대체.
    if bool(re.search('\^\^(.*?)\^\^',output)) == True:
        output = re.sub(u"\^\^(.*?)\^\^",r"<sup>\1</sup>",output)
    '''
    #아래첨자
    subcount = output.count(',,')
    while subcount > 0:
        newoutput = output.replace(',,','<sub>',1)
        output = newoutput
        newoutput = output.replace(',,','</sub>,1')
        output = newoutput
        subcount = output.count(',,')
    '''
    if bool(re.search('\,\,(.*?)\,\,',output)) == True:
        output = re.sub(u"\,\,(.*?)\,\,",r"<sub>\1</sub>",output)
    '''

    #글자 키우기
    #if bool(re.search('\{\{\{\+1(.*?)\}\}\}',output)) == True:
    output = re.sub(u"\{\{\{\+1(.*?)\}\}\}",r"{{+1|\1}}",output)

    #youtube
    #if bool(re.search('\[\[youtube\((.*?)\)\]\]',output)) == True:
    output = re.sub(u"\[\[youtube\((.*?)\)\]\]",r"{{youtube|\1}}",output)

    #if bool(re.search('\[youtube\((.*?)\)\]',output)) == True:
    output = re.sub(u"\[youtube\((.*?)\)\]",r"{{youtube|\1}}",output)

    #주석
    #if bool(re.search('\[\* (.*)\]',output)) == True:
    output = re.sub(u"\[\* (.+?)\]",r"<ref>\1</ref>",output)


    output = output.replace('[각주]','{{각주}}')
    #gakjucount = output.count('[각주]')


    output = re.sub(u'\{\{\{(.*?)\=\"\/\/(.*?)\"(.*?)\}\}\}',r"{{youtube|http://\2}}",output)



    return output
