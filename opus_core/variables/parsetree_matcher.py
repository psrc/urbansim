# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
    

# Match function for parse trees, along with parse tree patterns for use in autogenerating variable classes.
# See the file utils/parsetree_pattern_generator for utility functions for generating new tree fragments.


# the match function is adapted from the example in the Python documentation for the parser module
# Section 18.1.6.2 Information Discovery
# It matches a pattern against a parse tree (represented as a tuple), and extracts variables
# It is augmented from the Python documentation version with patterns that allow optional element.

from itertools import zip_longest

def match(pattern, data, vars=None):
    """Match `data' to `pattern', with variable extraction.

    pattern
        Pattern to match against, possibly containing variables.  There are two kinds of patterns:
        ['varname'] -- matches anything
        ['?', subpattern] -- for optional information.  Matches subpattern against the data if present.  If 
            the data is present, succeeds or fails depending on whether the subpattern matches.  If there isn't
            any data there, also succeeds.  The subpattern is a tuple, possibly containing other variable names
            or optional patterns.  There isn't any backtracking -- if an optional subpattern doesn't match the
            data, we just fail rather than continuing on to see if the remainder of the pattern can match.

    data
        Data to be checked and against which variables are extracted.

    vars
        Dictionary of variables which have already been found.  If not
        provided, an empty dictionary is created.

    The `pattern' value may contain variables of the form ['varname'] which
    are allowed to match anything.  The value that is matched is returned as
    part of a dictionary which maps 'varname' to the matched value.  'varname'
    is not required to be a string object, but using strings makes patterns
    and the code which uses them more readable.

    This function returns two values: a boolean indicating whether a match
    was found and a dictionary mapping variable names to their associated
    values.
    """
    if vars is None:
        vars = {}
    type_pattern = type(pattern)
    if type_pattern is list:
        lpattern = len(pattern)
        if lpattern==1:
            # pattern is of the form ['varname']
            vars[pattern[0]] = data
            return True, vars
        if lpattern==2 and pattern[0]=='?':
            if data is None:
                return True, vars
            else:
                return match(pattern[1], data, vars)
        raise ValueError('bad syntax for pattern')
    if type_pattern is not tuple:
        return (pattern == data), vars
    if data is None:
        # we're trying to match a pattern that isn't a list (so not an optional element)
        # with no data -- just fail
        return False, vars
    if len(data)>len(pattern):
        return False, vars

    for pattern, data in zip_longest(pattern, data):
        same, vars = match(pattern, data, vars)
        if not same:
            break
    return same, vars



# unit tests for the match function and to check that the parse trees
# for this version of python correspond to those in the patterns

from opus_core.tests import opus_unittest
import parser
import symbol, token
from opus_core.variables.parsetree_patterns import *

TEST_PATTERN_FULLY_QUALIFIED_VARIABLE =  \
    (symbol.power,
     (symbol.atom_expr,
     (symbol.atom, (token.NAME, 'urbansim')),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, 'gridcell')),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, 'population'))))
    
TEST_PATTERN_FULLY_QUALIFIED_VARIABLE_TO_POWER =  \
    (symbol.power,
     (symbol.atom_expr,
     (symbol.atom, (token.NAME, 'urbansim')),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, 'gridcell')),
     (symbol.trailer,
      (token.DOT, '.'),
      (token.NAME, 'population')),
     (token.DOUBLESTAR, '**'),
     (symbol.factor,
      (symbol.power,
       (symbol.atom_expr,
       (symbol.atom, (token.NUMBER, '2')))))))
    
class Tests(opus_unittest.OpusTestCase):

    def test_fully_qualified_varible_pattern(self):
        same, vars = match(SUBPATTERN_FULLY_QUALIFIED_VARIABLE, TEST_PATTERN_FULLY_QUALIFIED_VARIABLE)
        self.assertTrue(same, msg="pattern did not match")
        self.assertEqual(len(vars), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars['shortname'], 'population', msg="bad value in dictionary")

    def test_fully_qualified_varible_pattern_to_power(self):
        same, vars = match(SUBPATTERN_FULLY_QUALIFIED_VARIABLE, TEST_PATTERN_FULLY_QUALIFIED_VARIABLE_TO_POWER)
        self.assertTrue(same, msg="pattern did not match")
        self.assertEqual(len(vars), 4, msg="wrong number of items in dictionary")
        self.assertEqual(vars['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars['shortname'], 'population', msg="bad value in dictionary")
        self.assertEqual(vars['exponent'], '2', msg="bad value in dictionary")

    def test_no_match(self):
        same, vars = match(SUBPATTERN_DATASET_QUALIFIED_ATTRIBUTE, TEST_PATTERN_FULLY_QUALIFIED_VARIABLE)
        self.assertEqual(same, False, msg="bad match")

    def test_full_expression(self):
        """
        Parse an expression and match it.  This checks that this version of Python is producing parse trees like
        those that the patterns were constructed from.  Not a complete check, but does some checking for changes
        between versions of Python.
        """
        full_expr = "urbansim.gridcell.population"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_EXPRESSION, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")
       
    def test_full_expression_with_comment(self):
        """
        Parse an expression and match it.  In addition to test_full_expression,
        this checks if comments are supported for a variable.  This test used to fail
        for Python 2.7.
        """
        full_expr = "urbansim.gridcell.population #comment"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_EXPRESSION, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")
       
    def MASK_test_full_expression_with_comment_and_newline(self):
        """
        Parse an expression and match it.  In addition to test_full_expression_and_newline,
        this checks if comments terminated by newline are supported for a variable.  Currently broken for Python 2.6.
        """
        full_expr = "urbansim.gridcell.population #comment\n"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_EXPRESSION, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")
        
    def test_full_assignment(self):
        """
        Parse an assignment and match it.  Similar to test_full_expression.
        """
        full_expr = "myvar = urbansim.gridcell.population"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_ASSIGNMENT, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")
        
    def test_full_assignment_with_comment(self):
        """
        Parse an assignment and match it.  In addition to test_full_assignment,
        this checks if comments are supported for a variable.  This test used to fail
        for Python 2.7.
        """
        full_expr = "myvar = urbansim.gridcell.population # comment"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_ASSIGNMENT, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")
        
    def MASK_test_full_assignment_with_comment_and_newline(self):
        """
        Parse an assignment and match it.  In addition to test_full_assignment_with_comment,
        this checks if comments terminated by newline are supported for a variable.  Currently broken for Python 2.6.
        """
        full_expr = "myvar = urbansim.gridcell.population # comment\n"
        t = parser.st2tuple(parser.suite(full_expr))
        same1, vars1 = match(FULL_TREE_ASSIGNMENT, t)
        self.assertTrue(same1, msg="pattern did not match")
        expr_tree = vars1['expr']
        same2, vars2 = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, expr_tree)
        self.assertTrue(same2, msg="pattern did not match")
        self.assertEqual(len(vars2), 3, msg="wrong number of items in dictionary")
        self.assertEqual(vars2['package'], 'urbansim', msg="bad value in dictionary")
        self.assertEqual(vars2['dataset'], 'gridcell', msg="bad value in dictionary")
        self.assertEqual(vars2['shortname'], 'population', msg="bad value in dictionary")

if __name__=='__main__':
    opus_unittest.main()
