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

''' A mini test for the generator

Uses genTestParser.py, generated from genTest.pijnu
'''

from sys import exit as end

# get parser
from pijnu.generator import makeParser
grammar = file("genTest.pijnu").read()

#~ grammar = """
#~ genTest
#~ <toolset>
#~ pass
#~ <definition>
#~ X	: 'x'
#~ XX	: X XXX			: join
#~ XXX	: XX / X		: @
#~ """
#~ parser = makeParser(grammar)
#~ source = r"""x xxx xxxxx"""
#~ parser.test(source,"findAll")
#~ end()

make_parser = makeParser(grammar)
parser = make_parser()

# test it
sources = """\
1
- 1.1
1.1 * -2
-3 + +4.4
-3 ++4.4
3 *-4.4
9*8*7*6*5
1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1*1
9+8+7+6+5
3*(2+1)
1*4 + 3*2
""".splitlines()
parser.testSuiteDict(sources)

print parser.digits
print parser.foo
print parser.bar
print parser.baz
print repr(parser.foo)
print repr(parser.bar)
print repr(parser.baz)
print parser.foo.pattern
print parser.bar.klass
print parser.baz.klass
