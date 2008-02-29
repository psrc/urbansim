#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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


###############
# These are examples how to create a model specification, i.e. an object of EquationSpecification. 
# Such object can be then passed to the 'estimate' method of several models. 
###############

from opus_core.equation_specification import EquationSpecification

def create_simple_regression_specification():
    """
        y ~ b_0 + b_1*x_1 + b_2*x_2
        
        b_{i} are coefficients, x_1 is a variable 'dataset.some_primary_attribute', 
        x_2 is an expression 'my_variable = log(package.dataset.variable1*package.dataset.variable2)'
    """
    specification = EquationSpecification(
                        #'constant' is a reserved word in Opus' specification for an intercept
                        variables = ('constant', 'dataset.some_primary_attribute', 'my_variable = log(package.dataset.variable1*package.dataset.variable2)'),
                        coefficients = ( 'b_0', 'b_1', 'b_2')
                                          )
    return specification

if __name__ == "__main__":
    create_simple_regression_specification().summary()