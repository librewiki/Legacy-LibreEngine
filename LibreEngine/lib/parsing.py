# -*- coding: utf-8 -*-
__author__ = '나유타'

from pypandoc import convert
import pymysql
from pymysqlreplication import BinLogStreamReader



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

#def dbtitlesearch(target):
