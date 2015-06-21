# -*- coding: utf-8 -*-
__author__ = '나유타'

import pypandoc


def mwrender(mwtext):



    output = pypandoc.convert(mwtext, 'html', format='mediawiki' )

    rendered = output
    return rendered