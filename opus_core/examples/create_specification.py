# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


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

def create_simple_specification_from_dictionary():
    """Corresponds to the specification in 'create_simple_regression_specification'."""
    spec = {
       -2: [ # use always -2, if there are no submodels
           ('constant', 'b_0'),
           ('dataset.some_primary_attribute', 'b_1'),
           ('my_variable = log(package.dataset.variable1*package.dataset.variable2)', 'b_2')
           ]     
            }
    return EquationSpecification(specification_dict=spec)

def create_specification_with_multiple_submodels():
    """It has 2 submodels and a fixed value for cofficient 'bias'."""
    spec = {
       1: [
           'constant',
           ('dataset.some_primary_attribute', 'b_1'),
           ('my_variable = log(package.dataset.variable1*package.dataset.variable2)', 'b_2')
           ],
       5: [
           'constant',
           'package.dataset.variable1',
           ('bias', 'bias', 1) 
           ]
            }
    return EquationSpecification(specification_dict=spec)

def create_specification_with_definition():
    """All variables are defined in a preamble. They are then further referenced only by aliases.
    """
    spec = {
        '_definition_': [
                         ('dataset.some_primary_attribute', 'b_1'),
                         ('my_variable = log(package.dataset.variable1*package.dataset.variable2)', 'b_2'),
                         'package.dataset.variable1',
                         'var2 = log(package.dataset.variable2*1000)',
                         ('bias', 'bias', 1)
                         ],
       1: [
           'constant',
           'some_primary_attribute',
           'my_variable',
            'var2'
           ],
       5: [
           'constant',
           'variable1',
           'bias'
           ]
            }
    return EquationSpecification(specification_dict=spec)

if __name__ == "__main__":
    create_simple_regression_specification().summary()
    create_simple_specification_from_dictionary().summary()
    create_specification_with_multiple_submodels().summary()
    create_specification_with_definition().summary()
    