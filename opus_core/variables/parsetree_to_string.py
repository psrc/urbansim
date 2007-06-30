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
    
import token

def parsetree_to_string(parsetree):
    """function to take a parse tree and turn it back into Python source code"""
    if len(parsetree)==2 and token.ISTERMINAL(parsetree[0]):
        return parsetree[1]
    else:
        result = ''
        for t in parsetree[1:]:
            result = result + parsetree_to_string(t)
        return result


from opus_core.tests import opus_unittest
import parser

class Tests(opus_unittest.OpusTestCase):

    # Parse some expressions, turn them back into strings, and see if each is equal to the original
    # Note that the result won't have spaces, so in each case we use an original expression with no
    # whitespace.
    
    def test_var(self):
        expr = "x"
        t = parser.ast2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_constant(self):
        expr = "42"
        t = parser.ast2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_expr1(self):
        expr = "urbansim.gridcell.population"
        t = parser.ast2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)

    def test_expr2(self):
        expr = "myneighborhood.aggregate(10*myzone.my_variable,intermediates=[myfaz,myfazdistr],function=sum)"
        t = parser.ast2tuple(parser.suite(expr))
        s = parsetree_to_string(t)
        self.assertEqual(s, expr)
       
if __name__=='__main__':
    opus_unittest.main()
