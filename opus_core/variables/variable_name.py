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


class VariableName(object):
    """Object representing the name of an Opus variable.  The fields are as follows.  We'll use
    the variable 'urbansim.gridcell.population as a running example'.
    
    expression: a string that defines the variable name, e.g. 'urbansim.gridcell.population'
        or 'ln(urbansim.gridcell.population)'
    _squished_expression: same as expression, but with whitespace removed
    package_name: the name of the package containing the variable definition (e.g. 'urbansim'), or None 
    dataset_name: the name of the dataset (e.g. 'gridcell'), or None
    short_name: the name of the attribute that holds the variable value in the dataset, e.g. 'population'
        (this is required; it can't be None)
    alias: an alias for the variable, or None.  Example: for 'lnpop = ln(urbansim.gridcell.population)' 
        the alias is 'lnpop'
    autogen_class: for variables denoted by an expression (rather than just a partially or fully qualified
        name), this will be a reference to the generated class that is the definition of that variable.
    VariableName keeps a cache of information for variable names that have already been generated, and reuses
    that information when possible (in particular, so that it doesn't need to make a new autogen class).
    """
 
    # class dictionary of expressions for which variables have already been generated.  The keys are
    # strings (the source expression, with whitespace removed).  The values are tuples 
    # (package_name, dataset_name, short_name, alias, autogen_class)
    _cache = {}

    def __init__(self, expression):
        self._expression = expression
        # squished is a copy of the expression with whitespace removed
        # by using this in the cache we make expressions equivalent that differ only by whitespace
        squished = ''
        for c in expression:
            if not c.isspace():
                squished = squished + c
        self._squished_expression = squished
        if squished not in self._cache:
            # put the import here to avoid a circular import at the top level
            from opus_core.variables.autogen_variable_factory import AutogenVariableFactory
            t = AutogenVariableFactory(expression).generate_variable_name_tuple()
            self._cache[squished] = t
        (package_name, dataset_name, short_name, alias, autogen_class) = self._cache[squished]
        self._package_name = package_name
        self._dataset_name = dataset_name
        self._short_name = short_name
        self._alias = alias
        self._autogen_class = autogen_class

    def get_expression(self):
        return self._expression

    def get_package_name(self):
        return self._package_name

    def get_dataset_name(self):
        return self._dataset_name

    def get_short_name(self):
        return self._short_name
    
    def get_squished_expression(self):
        return self._squished_expression
    
    def get_alias(self):
        if self._alias is None:
            return self.get_short_name()
        else:
            return self._alias

    def get_autogen_class(self):
        return self._autogen_class

    # setters
    def set_dataset_name(self, n):
        self._dataset_name = n

    # comparison operations
    def __eq__(self, n):
        return self._squished_expression == n._squished_expression

    def __ne__(self, n):
        return not (self==n)

from opus_core.tests import opus_unittest
class Tests(opus_unittest.OpusTestCase):

    def test_eq_and_neq(self):
        v1 = VariableName('p = urbansim.gridcell.population')
        v2 = VariableName('p=urbansim.gridcell.population')  # same as v1, but no spaces
        v3 = VariableName('x')
        self.assert_(v1==v2)
        self.assert_(not (v1!=v2))
        self.assert_(v1!=v3)
        self.assert_(not (v1==v3))
        
if __name__=='__main__':
    opus_unittest.main()
