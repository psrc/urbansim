# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# Functions for use in Opus expressions.  The autogenerated code will import all
# of these, so that they are available for use in computing the values of expressions.

from numpy import ma, rank
import numpy, scipy
import opus_core.misc
from pkg_resources import parse_version
from opus_core.misc import ismember as misc_ismember
import scipy.stats as stats

try:
    if parse_version(scipy.__version__) <= parse_version('0.7.0'):
        from scipy.stats.stats import zs as scipy_zscore
    else:
        from scipy.stats.stats import zscore as scipy_zscore
except ImportError:
    print "There is an error importing zscore from scipy; zscore function is not available."

def clip_to_zero(v):
    """Returns the given values with all negative values clipped to 0."""
    return opus_core.misc.clip_to_zero_if_needed(v)

def exp(v):
    """Returns exp of its argument."""
    return numpy.exp(v)

def expfin(v):
    """Returns exp of its argument where all infinite values are clipped to the maximum of its type."""
    result = numpy.exp(v)
    pidx = numpy.isinf(result)
    result[numpy.where(pidx)] = numpy.finfo(result.dtype).max
    return result

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

def zscore(v):
    """Returns a 1D array of z-scores, one for each score in the passed array, computed relative to the passed array.
    """
    if rank(v) > 1:
        shape = v.shape
        z = scipy_zscore(v.ravel())
        return z.reshape(shape)
    return scipy_zscore(v)

def sfg(v, fill=0):
    """safeguard: fill in NaN and inf with a default filling value
    """
    results = v.copy()
    results[numpy.isinf(results)] = fill
    results[numpy.isnan(results)] = fill
    return results

def ismember(v, member_list):
    """ an in1d replacement that is compatible with low version of numpy (<=1.4.0)
    """
    return misc_ismember(v, member_list)

def scoreatpercentile(v, percentile):
    return stats.scoreatpercentile(v, percentile)

def ones_like(v):
    return numpy.ones_like(v)

def zeros_like(v):
    return numpy.zeros_like(v)

def random_like(v):
    return numpy.random.random(v.size)

def subtract_mean(v):
    """Subtract overall average."""
    return v - v.mean()

def mean_with_exclude(v, exclude=None):
    """Compute mean after excluding elements with values equal to 'exclude'.
    The resulting array has identical values.
    """
    from numpy import repeat
    if exclude is None:
        return v.mean()
    return repeat(v[v <> exclude].mean(), v.size).reshape(v.shape)
    
def replace_value_with_mean(v, value=0):
    """Compute mean of the 'v' array while excluding 'value'. Replace all cells 
    that are equal to 'value' with the computed mean.
    """
    return v*(v<>value) + mean_with_exclude(v, value)*(v==value)


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

    def test_zscore(self):
        import numpy as np
        z = lambda x: (x - np.mean(x)) / np.std(x)

        input = np.random.random(100) * 100
        self.assert_(np.allclose(zscore(input), z(input)))

        input = np.random.randn(2, 3, 6) * 6 + 4.5
        self.assert_(np.allclose(zscore(input), z(input)))
        
    def test_expfin(self):
        import numpy as np
        type = np.exp(1).dtype
        self.function_tester('expfin', np.array([1000, 8, 700, 10, 0], dtype='int32'), 
                                        [np.finfo(type).max, 2980.9579870417283, 1.0142320547350045e+304,
                                         22026.465794806718, 1.0])

    def test_scoreatpercentile(self):
        import numpy as np
        numbers = np.random.permutation(100) + 1
        self.assert_( scoreatpercentile(numbers, 0), 0)
        self.assert_( scoreatpercentile(numbers, 5), 5)
        self.assert_( scoreatpercentile(numbers, 21), 21)
        self.assert_( scoreatpercentile(numbers, 100), 100)
       
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
    
    def test_ones_like(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"attr1": array([5, 10, 0, 3]), "attr2": array([5.0, 0.0, 8.0, 1.1]), "id": arange(4)}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        expr1 = 'ones_like(attr1)'
        result = dataset.compute_variables([expr1])
        should_be = array([1, 1, 1, 1])
        self.assert_(numpy.allclose(result, array(should_be), rtol=1e-6), "Error in ones_like")
        self.assert_(result.dtype==should_be.dtype, "Error in ones_like")

        expr2 = 'ones_like(attr1)'
        result = dataset.compute_variables([expr2])
        should_be = array([1, 1, 1, 1])
        self.assert_(numpy.allclose(result, array(should_be), rtol=1e-6), "Error in ones_like")
        self.assertEqual(result.dtype, should_be.dtype, "Error in ones_like")
        
    def test_mean_with_exclude(self):
        self.function_tester('mean_with_exclude', [4, 0, 0, 8, 0, 0], array(6*[6]), 'exclude=0')
        self.function_tester('mean_with_exclude', [4, 0, 0, 8, 0, 0], array(6*[2]))
        
    def test_replace_value_with_mean(self):
        self.function_tester('replace_value_with_mean', [4, 0, 0, 8, 0, 0], array([4, 6, 6, 8, 6, 6]))

if __name__=='__main__':
    opus_unittest.main()
