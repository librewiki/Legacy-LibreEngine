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

""" testValid
<definition>

x	: "x"		: noX
letter	: [a..z]	: noX
text	: letter{4..6}

"""


from pijnu.library import *

testValidParser = Parser()
state = testValidParser.state



### title: testValid ###
###   <toolset>
def noX(node):
	if node.value == 'x':
		message = "'x' is an invalid letter."
		(pattern,pos,source) = (node.pattern,node.start,node.source)
		raise Invalidation(message, pattern=pattern, source=source,pos=pos)

###   <definition>
x = Word('x', expression='"x"')(noX)
letter = Klass(format='[a..z]', expression='abcdefghijklmnopqrstuvwxyz')(noX)
text = Repetition(letter, numMin=4,numMax=6, expression='letter{4..6}')



testValidParser._recordPatterns(vars())
testValidParser._setTopPattern("text")
testValidParser.grammarTitle = "testValid"
testValidParser.fileName = "testValidParser.py"
