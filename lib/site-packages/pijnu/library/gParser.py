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

"""
<definition>
k:[a..e\t\n]
"""

from pijnu.library import *

gParser = Parser()
state = gParser.state

### title: g ###
###   <definition>
k = Klass(format='[a..e\\t\\n]', charset='abcde\t\n')

gParser._recordPatterns(vars())
gParser._setTopPattern("k")
gParser.grammarTitle = "g"
gParser.fileName = "gParser.py"
