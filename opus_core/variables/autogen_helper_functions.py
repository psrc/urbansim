# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# helper functions for autogen_variable_factory

import symbol, token


# return a string in quotes, or else 'None' 
def quote(name):
    return 'None' if name is None else "'%s'" % name


# various functions to manipulate parsetrees

def parsetree_to_string(parsetree):
    """function that takes a parse tree and turns it back into Python source code"""
    if len(parsetree)==2 and token.ISTERMINAL(parsetree[0]):
        return parsetree[1]
    else:
        result = ''
        for t in parsetree[1:]:
            # Insert a space if need be.  We need a space if the last thing 
            # in result and the first thing in the new string are both alphnumeric.
            st = parsetree_to_string(t)
            if len(result)>0 and len(st)>0 and (result[-1]).isalnum() and (st[0]).isalnum():
                result = result + ' ' + st
            else:
                result = result + st
        return result

def parsetree_substitute(parsetree, dict):
    """function that takes a parsetree and returns a new tree, substituting subtrees in dict 
       with the corresponding replacement tree.  dict is a dictionary whose keys are the 
       tree fragments to replace and whose values are the replacement tree fragments"""
    if type(parsetree) is tuple:
        newtree = ()
        for t in parsetree:
            if t in dict:
                newtree = newtree + ( dict[t] , )
            else:
                newtree = newtree + ( parsetree_substitute(t, dict) , )
        return newtree
    else:
        if parsetree in dict:
            return dict[parsetree]
        else:
            return parsetree
        

from opus_core.tests import opus_unittest
import parser

class Tests(opus_unittest.OpusTestCase):
    
    def test_quote(self):
        self.assertEqual(quote('squid'), "'squid'")
        self.assertEqual(quote(None), 'None')

    # Parse some expressions, turn them back into strings, and see if each is equal to the original
    # Note that the result won't have spaces unless they are needed, so in each case we use an 
    # original expression with only necessary whitespace.
    
    def test_var_parsetree_to_string(self):
        expr = "x"
        t = parser.st2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_constant_parsetree_to_string(self):
        expr = "42"
        t = parser.st2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_expr1_parsetree_to_string(self):
        expr = "urbansim.gridcell.population"
        t = parser.st2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_expr2_parsetree_to_string(self):
        expr = "myneighborhood.aggregate(10*myzone.my_variable,intermediates=[myfaz,myfazdistr],function=sum)"
        t = parser.st2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)
        
    def test_adjacent_keywords_parsetree_to_string(self):
        expr = "x not in dict and y<3*z"
        t = parser.st2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)
       
    def test_parsetree_substitute(self):
        tree =  (symbol.power,
            (symbol.atom, (token.NAME, 'dataset')),
            (symbol.trailer,
             (token.DOT, '.'),
             (token.NAME, 'attribute')))
        dict = {'dataset': 'newdata', (token.DOT, '.'): (token.EQUAL, 'newname')}
        newtree = parsetree_substitute(tree, dict)
        should_be =  (symbol.power,
            (symbol.atom, (token.NAME, 'newdata')),
            (symbol.trailer,
             (token.EQUAL, 'newname'),
             (token.NAME, 'attribute')))
        self.assertEqual(newtree, should_be)
       
if __name__=='__main__':
    opus_unittest.main()
