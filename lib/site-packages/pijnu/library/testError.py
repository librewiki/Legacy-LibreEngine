# -*- coding: utf8 -*-

'''
Copyright 2009 Denis Derman <denis.spir@gmail.com> (former developer)
Copyright 2011-2012 Peter Potrowl <peter017@gmail.com> (current developer)

This file is part of Pijnu.

Pijnu is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pijnu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Pijnu.  If not, see <http://www.gnu.org/licenses/>.
'''

from pijnu.generator import makeParser
from pijnu.library.pattern import *


def testLocation():
    print ("=== creation")
    # data
    klass = Klass("a..z  0..9   \x09\x0a")
    string = String(klass, numMin=999)
    source = """abc def\tghi
1234567890987654321
1234567890987654321
1234567890987654321
jkl\t mno pqr\tstu vwx yz&"""
    string.name, klass.name = "string", "klass"
    # match errors
    for pos in (0, 5, 12, 39, 95):
        s = source[:pos] + '#' + source[pos:]
        try:
            string.match(s)
        except PijnuError, e:
            print e


def testWrap():
    print ("=== wrap error")
    # patterns
    X = Word("X")
    Y = Word("Y")
    ch = Choice((X, Y))
    seq = Sequence((X, Y))
    X.name, Y.name = "X", "Y"
    ch.name, seq.name = "ch", "seq"
    # yield wrap error
    # choice
    text = "ZYX"
    ch.test(text)
    # sequence
    text = "XZY"
    seq.test(text)


def testEOT():
    print ("=== EOT error")
    w, c = Word("abc"), Char('1')
    w.name, c.name = "w", "c"
    p = Sequence((w, c))
    p.name = "p"
    # yield EOT error
    text = "abc"
    p.test(text)


def testIncomplete():
    k = Klass("[0..9]")
    p = String(k, numMin=1)
    p.name, k.name = "p", "k"
    # yield error
    print ("=== incomplete parse error")
    text = "1234567890987654321abcdefghijklmnopqrstuvwxyzyxwvutsrq"
    p.test(text, "parseTest")


def testInvalid():
    testValidGrammar = r"""
testValid
<toolset>
def noX(node):
    if node.value == 'x':
        message = "'x' is an invalid letter."
        (pattern,pos,source) = (node.pattern,node.start,node.source)
        raise Invalidation(message, pattern=pattern, source=source,pos=pos)
<definition>
    x       : "x"           : noX
    letter  : [a..z]        : noX
    text    : letter{4..6}
"""

    make_parser = makeParser(testValidGrammar)
    parser = make_parser()

    source = "abcxyz"
    # check 'x' not matched alone
    parser.x.test('x')
    # check 'x' not matched in sequence
    parser.letter.test(source, "findAll")
    # check repetition match stops on 'x'
    parser.test(source)


def test():
    testLocation()
    print RULER
    testWrap()
    print RULER
    testEOT()
    print RULER
    testIncomplete()
    print RULER
    testInvalid()
if __name__ == "__main__":
    test()
