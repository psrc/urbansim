#
# Opus software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

# Utility classes that can be used to generate parse tree patterns.  These
# utilities take a sample expression or statement, and return a parse tree that
# uses symbolic names for the nodes.  You'll need to then do additional editing on 
# the parse tree as needed (for example, replacing a specific value with a pattern).


import parser
from symbol import sym_name
from token import tok_name
from pprint import pprint

# pretty-prints a symbolic parse tree for expr
# the symbolic names will be strings, so to use this as a constant
# in some code you'll need to replace the quotes with nothing
# (except for the actual string constants ...)
# for trees for statements rather than expressions, change 'expr' to 'suite'
def print_symbolic_tree(expr):
    t = parser.ast2tuple(parser.expr(expr))
    pprint(integer2symbolic(t))

# take a parse tree represented as a tuple, and return a new tuple
# where the integers representing internal nodes and terminal nodes are 
# replaced with symbolic names
def integer2symbolic(fragment):
    head = fragment[0]
    if head in sym_name:
        rest = tuple(map(integer2symbolic, fragment[1:]))
        return ('symbol.' + sym_name[head], ) + rest
    if head in tok_name:
        return ('token.' + tok_name[head], ) + fragment[1:]
    raise ValueError("bad value in parsetree")

# example of use:
print_symbolic_tree("urbansim.gridcell.population**2")


