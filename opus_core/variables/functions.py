#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

# Functions for use in Opus expressions.  The autogenerated code will import all
# of these, so that they are available for use in computing the values of expressions.

from numpy import ma
import numpy
import opus_core.misc

def clip_to_zero(v):
    """Returns the given values with all negative values clipped to 0."""
    return opus_core.misc.clip_to_zero_if_needed(v)

def exp(v):
    """Returns exp of its argument."""
    return numpy.exp(v)

def ln(v):
    """Returns an array of natural logarithms. Values = 0 result in 0."""
    return ma.filled(ma.log(ma.masked_where(v==0,v)),0.0)

def ln_bounded(v):
    """Returns an array of natural logarithms. Values < 1 result in 0."""
    return ma.filled(ma.log(ma.masked_where(v<1,v)),0.0)
    
def ln_shifted(v, shift=1):
    """'v' is shifted by 'shift' before doing log."""
    return ma.log(v + shift)
    
def ln_shifted_auto(v):
    """If 'v' has values <= 0, it is shifted in a way that min(v)=1 before doing log. 
    Otherwise the log is done on the original 'v'."""
    vmin = ma.minimum(v)
    if vmin <= 0:
        values = v - vmin + 1
    else:
        values = v
    return ma.log(values)

def safe_array_divide(numerator, denominator, return_value_if_denominator_is_zero=0.0, type='float32'):
    """If denominator == 0, return return_value_if_denominator_is_zero.  Else return numerator / denominator."""
    return opus_core.misc.safe_array_divide(numerator, denominator, return_value_if_denominator_is_zero, type)

def sqrt(v):
    """Returns an array of square roots.  Values < 0 result in 0."""
    return numpy.sqrt(ma.filled(ma.masked_where(v<0, v), 0.0))


# unit tests for all the functions

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, arange

class Tests(opus_unittest.OpusTestCase):
    
    # helper function to invoke a function and check the resulting values
    def function_tester(self, func, values, should_be, optional_args=None):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"my_variable": array(values), "id": arange(len(values))}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        if optional_args is None:
            expr = "%s(my_variable)" % func
        else:
            expr = "%s(my_variable, %s)" % (func, optional_args)
        result = dataset.compute_variables([expr])
        self.assert_(ma.allclose(result, array(should_be), rtol=1e-6), "Error in " + func)

    def test_clip_to_zero(self):
        self.function_tester('clip_to_zero', [4,8,-5,0], [4, 8, 0, 0])

    def test_exp(self):
        self.function_tester('exp', [10, 1, 0, -3], [22026.4657948, 2.718281828459, 1.0, 0.049787068368])

    def test_ln(self):
        self.function_tester('ln', [4,8,0], [1.386294, 2.079442, 0.0])

    def test_ln_bounded(self):
        self.function_tester('ln_bounded', [4,8,0.5,1,-10], [1.386294, 2.079442, 0.0, 0.0, 0.0])

    def test_ln_shifted(self):
        self.function_tester('ln_shifted', [4,8,0.5,0], [1.60943791, 2.19722458, 0.40546511, 0.0])

    def test_ln_shifted_with_arg(self):
        self.function_tester('ln_shifted', [-6,-9, 10, 20], [1.38629436, 0, 2.99573227, 3.40119738], 'shift=10')

    def test_ln_shifted_auto(self):
        self.function_tester('ln_shifted_auto', [4,8,0.5,-1], [1.79175947, 2.30258509, 0.91629073, 0.00])
        self.function_tester('ln_shifted_auto', [4,8,0.5,1], [1.386294, 2.079442, -0.6931472, 0.0])

    def test_sqrt(self):
        self.function_tester('sqrt', [4,-8,0.5,1], [2,0,0.70710678118654757,1])
        
    # the function_tester is just set up for unary functions, and safe_array_divide takes two numpy arguments,
    # so it is tested separately
    def test_safe_array_divide(self):
        expr = 'safe_array_divide(numerator, denominator)'
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"numerator": array([5, 10, 0, 3]), "denominator": array([5, 0, 8, 1]), "id": arange(4)}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([1, 0, 0, 3])
        self.assert_(ma.allclose(result, array(should_be), rtol=1e-6), "Error in safe_array_divide")

    def test_safe_array_divide_with_return_value(self):
        expr = 'safe_array_divide(numerator, denominator, return_value_if_denominator_is_zero=100)'
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"numerator": array([5, 10, 0, 3]), "denominator": array([5, 0, 8, 1]), "id": arange(4)}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([1, 100, 0, 3])
        self.assert_(ma.allclose(result, array(should_be), rtol=1e-6), "Error in safe_array_divide")
    
        
if __name__=='__main__':
    opus_unittest.main()
