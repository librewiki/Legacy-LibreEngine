# -*- coding: utf-8 -*-
__author__ = 'myshytf'

import pypandoc


def mwrender(mwtext):



    output = pypandoc.convert(mwtext, 'html5', format='mediawiki' )

    rendered = output
    return rendered