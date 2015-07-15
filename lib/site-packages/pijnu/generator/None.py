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

""" genTest
<definition>
X	: 'x'
XX	: X XXX			: join
XXX	: XX / X		: @

"""

from pijnu.library import *

genTestParser = Parser()
state = genTestParser.state

### title: genTest ###

###   <toolset>
pass

###   <definition>
# recursive pattern(s)
XXX = Recursive(name='XXX')
X = Char('x', expression="'x'", name='X')
XX = Sequence([X, XXX], expression='X XXX', name='XX')(join)
XXX **= Choice([XX, X], expression='XX / X', name='XXX')

genTestParser._recordPatterns(vars())
genTestParser._setTopPattern("XXX")
genTestParser.grammarTitle = "genTest"
genTestParser.filename = "None.py"
