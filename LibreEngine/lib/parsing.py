# -*- coding: utf-8 -*-
__author__ = '나유타'

import pypandoc


def mwtohtmlrender(mwtext):



    output = pypandoc.convert(mwtext, 'html', format='mediawiki' )

    rendered = output
    return rendered

def mwtomwrender(mwtext):



    output = pypandoc.convert(mwtext, 'mediawiki', format='mediawiki' )

    rendered = output
    return rendered