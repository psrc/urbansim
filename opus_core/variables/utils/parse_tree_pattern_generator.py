# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# Utility classes that can be used to generate parse tree patterns.  These
# utilities take a sample expression or statement, and return a parse tree that
# uses symbolic names for the nodes.  You'll need to then do additional editing on 
# the parse tree as needed (for example, replacing a specific value with a pattern).


import parser
from symbol import sym_name
from token import tok_name
from pprint import pprint

# pretty-prints a symbolic parse tree for expr (as for use with 'eval')
# the symbolic names will be strings, so to use this as a constant
# in some code you'll need to replace the quotes with nothing
# (except for the actual string constants ...)
def print_eval_tree(expr):
    t = parser.ast2tuple(parser.expr(expr))
#    t = parser.ast2tuple(parser.suite(expr))
    pprint(integer2symbolic(t))

# same as print_eval_tree, except as for use with 'exec' (for definitions, statements, etc)
def print_exec_tree(expr):
    t = parser.ast2tuple(parser.suite(expr))
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

# examples of use:
# print_eval_tree("urbansim.gridcell.population**2")
# print_exec_tree("x = urbansim.gridcell.population**2")

s = """def foo(x=5):
    y = x+3
    return y*2
"""

print_exec_tree(s)

