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

# Parse tree patterns for use in autogenerating variable classes.
# See the file utils/parse_tree_pattern_generator for utility functions for generating new tree fragments.

import symbol, token, sys
    
# Python 2.4 and 2.5 have different parse trees, because of the introduction of if expressions
# The function _or_test_subtree is the identity function for Python 2.3 and 2.4, and constructs
# a bit of subtree for Python 2.5
def _or_test_subtree(tree):
    (major, minor, micro, releaselevel, serial) = sys.version_info
    if major==2 and (minor==3 or minor==4):
        return tree
    elif major==2 and minor==5:
        return (symbol.or_test, tree)
    else:
        raise StandardError, 'this version of Python not supported -- the only supported versions are Python 2.3, 2.4, and 2.5'
    
# ************************************************************************************
# The patterns named FULL_TREE_* match entire trees (as generated by the parser)
# ************************************************************************************

# This pattern matches a tree consisting of an expression (as opposed to a statement)
FULL_TREE_EXPRESSION =  \
    (symbol.file_input,
     (symbol.stmt,
      (symbol.simple_stmt,
       (symbol.small_stmt,
        (symbol.expr_stmt, ['expr'])),
       (token.NEWLINE, ''))),
     (token.ENDMARKER, ''))

# This pattern matches a tree consisting of a single assignment statement alias=expr
FULL_TREE_ASSIGNMENT =  \
    (symbol.file_input,
     (symbol.stmt,
      (symbol.simple_stmt,
       (symbol.small_stmt,
        (symbol.expr_stmt,
         (symbol.testlist,
          (symbol.test,
           _or_test_subtree(           
            (symbol.and_test,
             (symbol.not_test,
              (symbol.comparison,
               (symbol.expr,
                (symbol.xor_expr,
                 (symbol.and_expr,
                  (symbol.shift_expr,
                   (symbol.arith_expr,
                    (symbol.term,
                     (symbol.factor,
                      (symbol.power,
                       (symbol.atom, (token.NAME, ['alias'])))))))))))))))),
            (token.EQUAL, '='), ['expr'])),
       (token.NEWLINE, ''))),
     (token.ENDMARKER, ''))

# ************************************************************************************
# The patterns named EXPRESSION_IS_* match expressions that consist just of the named item
# ************************************************************************************

# This pattern matches an expression that is simply a fully qualified variable (not a more
# complex expression).
EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE =  \
    (symbol.testlist,
      (symbol.test,
       _or_test_subtree(                  
        (symbol.and_test,
         (symbol.not_test,
          (symbol.comparison,
           (symbol.expr,
            (symbol.xor_expr,
             (symbol.and_expr,
              (symbol.shift_expr,
               (symbol.arith_expr,
                (symbol.term,
                 (symbol.factor,
                  (symbol.power,
                   (symbol.atom, (token.NAME, ['package'])),
                   (symbol.trailer,
                    (token.DOT, '.'),
                    (token.NAME, ['dataset'])),
                   (symbol.trailer,
                    (token.DOT, '.'),
                    (token.NAME, ['shortname']))))))))))))))))

# This pattern matches an expression that is simply a dataset qualified variable (not a more
# complex expression).
EXPRESSION_IS_DATASET_QUALIFIED_VARIABLE =  \
    (symbol.testlist,
      (symbol.test,
       _or_test_subtree(                  
        (symbol.and_test,
         (symbol.not_test,
          (symbol.comparison,
           (symbol.expr,
            (symbol.xor_expr,
             (symbol.and_expr,
              (symbol.shift_expr,
               (symbol.arith_expr,
                (symbol.term,
                 (symbol.factor,
                  (symbol.power,
                   (symbol.atom, (token.NAME, ['dataset'])),
                   (symbol.trailer,
                    (token.DOT, '.'),
                    (token.NAME, ['shortname']))))))))))))))))

# This pattern matches an expression that is simply an attribute (not a more
# complex expression).
EXPRESSION_IS_ATTRIBUTE =  \
    (symbol.testlist,
      (symbol.test,
       _or_test_subtree(                  
        (symbol.and_test,
         (symbol.not_test,
          (symbol.comparison,
           (symbol.expr,
            (symbol.xor_expr,
             (symbol.and_expr,
              (symbol.shift_expr,
               (symbol.arith_expr,
                (symbol.term,
                 (symbol.factor,
                  (symbol.power,
                   (symbol.atom, (token.NAME, ['shortname']))))))))))))))))

# ************************************************************************************
# The patterns named SUBPATTERN__* match bits of expressions consisting of the named item.
# These can be used in picking out bits of a more complex tree.
# ************************************************************************************

# Match a fully qualified variable, perhaps raised to a power.  (The power part is optional.)
# Because of Python's grammar we need to include the power part in this pattern.
# Minor kludge: this pattern will also match 'urbansim.gridcell.population**' (i.e. missing
# the exponent).  However, we would never get far enough to feed that tree to the matcher, 
# since it would have caused a parse error earlier.  (Iit's not part of a legal Python expression.)
# The same thing is true for the patterns for dataset-qualified attribute and attribute.
SUBPATTERN_FULLY_QUALIFIED_VARIABLE =  \
    (symbol.power,
     (symbol.atom, (token.NAME, ['package'])),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, ['dataset'])),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, ['shortname'])),
     ['?', (token.DOUBLESTAR, '**')],
     ['?', (symbol.factor, (symbol.power, (symbol.atom, (token.NUMBER, ['exponent']))))])

SUBPATTERN_DATASET_QUALIFIED_ATTRIBUTE =  \
    (symbol.power,
     (symbol.atom, (token.NAME, ['dataset'])),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, ['shortname'])),
     ['?', (token.DOUBLESTAR, '**')],
     ['?', (symbol.factor, (symbol.power, (symbol.atom, (token.NUMBER, ['exponent']))))])

# match a single attribute name
SUBPATTERN_ATTRIBUTE =  \
    (symbol.power,
     (symbol.atom, (token.NAME, ['shortname'])),
     ['?', (token.DOUBLESTAR, '**')],
     ['?', (symbol.factor, (symbol.power, (symbol.atom, (token.NUMBER, ['exponent']))))])


SUBPATTERN_ARGLIST = symbol.arglist

# Match a method call (for use in matching functions in interaction set expressions and aggregations)
# For this pattern there must be 1 or more arguments (zero-argument methods won't match)
SUBPATTERN_METHOD_CALL_WITH_ARGS =  \
    (symbol.power,
     (symbol.atom, (token.NAME, ['receiver'])),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, ['method'])),
     (symbol.trailer,
      (token.LPAR, '('),
      ['args'],
      (token.RPAR, ')')))

SUBPATTERN_NAME = (token.NAME, ['name'])

# number_of_agents has a required argument 'agent', and an optional argument 'target'
SUBPATTERN_NUMBER_OF_AGENTS = \
    (symbol.arglist,
     (symbol.argument,
      (symbol.test,
       _or_test_subtree(
        (symbol.and_test,
         (symbol.not_test,
          (symbol.comparison,
           (symbol.expr,
            (symbol.xor_expr,
             (symbol.and_expr,
              (symbol.shift_expr,
               (symbol.arith_expr,
                (symbol.term,
                 (symbol.factor,
                  (symbol.power,
                   (symbol.atom,
                    (token.NAME,
                     ['agent'])))))))))))))))))

# Pattern that matches the arguments to a call to aggregate(...) and disaggregate(...)
# The first argument is required, but can be either a dataset-qualified name or a fully-qualified name.
# The remaining 3 arguments are optional.
SUBPATTERN_AGGREGATION =  \
    (symbol.arglist,
     (symbol.argument,
      (symbol.test,
       _or_test_subtree(           
        (symbol.and_test,
         (symbol.not_test,
          (symbol.comparison,
           (symbol.expr,
            (symbol.xor_expr,
             (symbol.and_expr,
              (symbol.shift_expr,
               (symbol.arith_expr,
                (symbol.term,
                 (symbol.factor,
                  (symbol.power,
                   (symbol.atom,
                    (token.NAME,
                     ['aggr_name1'])),
                   (symbol.trailer,
                    (token.DOT, '.'),
                    (token.NAME,
                     ['aggr_name2'])),
                   ['?', (symbol.trailer, (token.DOT, '.'), (token.NAME, ['aggr_name3']))])))))))))))))),
     ['?', (token.COMMA, ',')],
     ['?', ['arg2']],
     ['?', (token.COMMA, ',')],
     ['?', ['arg3']])

 # match an argument, optionally with a keyword
SUBPATTERN_ARGUMENT = \
    (symbol.argument,
     ['part1'],
     ['?', (token.EQUAL, '=')],
     ['?', ['part2']])


 # match an argument consisting of just a name
SUBPATTERN_NAME_ARG = \
    (symbol.test,
     _or_test_subtree(           
      (symbol.and_test,
       (symbol.not_test,
        (symbol.comparison,
         (symbol.expr,
          (symbol.xor_expr,
           (symbol.and_expr,
            (symbol.shift_expr,
             (symbol.arith_expr,
              (symbol.term,
               (symbol.factor,
                (symbol.power,
                 (symbol.atom,
                  (token.NAME, ['name'])))))))))))))))

# match an argument consisting of a list (either empty or nonempty)
SUBPATTERN_LIST_ARG = \
    (symbol.test,
     _or_test_subtree(           
      (symbol.and_test,
       (symbol.not_test,
        (symbol.comparison,
         (symbol.expr,
          (symbol.xor_expr,
           (symbol.and_expr,
            (symbol.shift_expr,
             (symbol.arith_expr,
              (symbol.term,
               (symbol.factor,
                (symbol.power,
                 (symbol.atom,
                  (token.LSQB, '['),
                  ['?', ['list']],  # if the list is empty this will match the right bracket; otherwise the list contents
                  ['?', (token.RSQB, ']')]))))))))))))))
