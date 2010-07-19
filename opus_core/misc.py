# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

"""Collection of useful miscellaneous functions and definitions"""

import os.path
import re
import shutil
import socket
import sys
import tempfile

from opus_core.logger import logger
from numpy import ma, array
from scipy.ndimage import standard_deviation
from inspect import getmembers, ismethod


DEFAULT_BYTEORDER = 'little'

class DebugPrinter(object):
    """Class for printing debugging messages on different levels."""
    def __init__(self, flag):
        self.flag = flag

    def print_debug(self, message, level):
        if self.flag >= level:
            logger.log_status(message)

# Functions:

def copytree(src, dst, skip_subdirectories=[]):
    """recursively copy the directory tree rooted at src to the destination directory dst.
    Skip any subdirectories in skip_subdirectories."""
    # This function is adapted from the shutil.copytree function.  It adds the optional 
    # skip_subdirectories parameter, and omits the symlinks parameter.
    names = os.listdir(src)
    os.mkdir(dst)
    for name in names:
        if name not in skip_subdirectories:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                copytree(srcname, dstname, skip_subdirectories=skip_subdirectories)
            else:
                shutil.copy2(srcname, dstname)
            
def ematch (list, str):
    """ Exact match of a string in a 1D-array of strings. Returns an array of matches.
    """
    from numpy import where

    imatches = (list == str)
    return where(imatches)[0]

def get_indices_of_matched_items(valuearray, items_to_match):
    """Returns indices of matched items from items_to_match within valuearray.
    """
    from numpy import array
    return array(map(lambda x: ematch(valuearray, x)[0], items_to_match))
    
def create_list_string(list, sep):
    """Returns a string of the list elements separated by sep."""
    # a very efficient function
    return sep.join(list)

def byteswap_if_needed(data, byteorder):
    """
    Ensures that data is read and written in the correct byteorder.
    To be used with the fromfile and tofile methods provided in numpy,
    which assume native byteorder rather than letting you specify.
    """
    if sys.byteorder <> byteorder:
        data.byteswap(True)

def module_path_from_opus_path(opus_path):
    """Returns the operating system path to this fully-specified opus module name,
    e.g. 'opus_core.misc' might be translated to 'C:\workspace\misc.py'
    """
    return '%s.py' % directory_path_from_opus_path(opus_path)

def directory_path_from_opus_path(opus_path):
    """Returns the operating system path to this fully-specified opus directory name,
    e.g. 'opus_core.docs.database_tables' might be translated to 'C:\workspace\opus_core\docs\database_tables'
    """
    parts = opus_path.split('.')
    exec('import %s as _start_package' % parts[0])
    path = _start_package.__path__[0]
    if len(parts) > 1:
        for part in parts[1:]:
            path = os.path.join(path, part)
    return path

def opus_path_for_variable_from_module_path(file_path):
    """Given the os path to a variable's module, return the opus path for that variable"""
    # abspath will be the absolute path to the variable (throwing away the .py extension -- that's the _ part in the pair)
    (abspath, _) = os.path.splitext(os.path.abspath(file_path))
    # the last 3 things in the path will be the package name, dataset name, and variable name
    (a, variable_name) = os.path.split(abspath)
    (b, dataset_name) = os.path.split(a)
    (_, package_name) = os.path.split(b)
    # return opus_path
    return '.'.join((package_name, dataset_name, variable_name))

def read_dataset_from_flt(dataset_name, file_path='.'):
    """Reads a dataset from a binary storage. Return a dictionary with attribute names as keys and data arrays as values."""
    from opus_core.store.file_flt_storage import file_flt_storage
    storage = file_flt_storage(file_path)
    return storage.load_table(dataset_name)
    
def write_to_file(filename, data, byteorder=DEFAULT_BYTEORDER):
    """Writes float data to a file."""
    byteswap_if_needed(data, byteorder)
    float_file = file(filename, mode="wb")
    data.tofile(float_file)
    float_file.close()
    byteswap_if_needed(data, byteorder)

def write_to_text_file(filename, data, mode="wb", delimiter="\n", end_delimiter="\n"):
    """Writes data to a text file."""
    text_file = file(filename, mode=mode)
    try:
        if isinstance(data, list):
            n = len(data)
        else:
            n = data.size

        if n > 0:
            for index in xrange(n-1):
                text_file.write(str(data[index]) + delimiter)

            text_file.write(str(data[n-1]) + end_delimiter)
        else:
            text_file.write(end_delimiter)

    finally:
        text_file.close

def write_table_to_text_file(filename, table, mode="wb", delimiter=' '):
    """Writes table (2D array) into a text file. Entries in each row are delimited by 'delimiter'"""
    write_to_text_file(filename, table[0,:], mode=mode, delimiter=delimiter)
    for k in range(1,table.shape[0]):
        write_to_text_file(filename, table[k,:], delimiter=delimiter, mode="ab")

def load_table_from_text_file(filename, convert_to_float=False, split_delimiter=' ', header=False, comment=None):

    """Reads table from a file. It returns a tuple, where the first element
       is an array of the values in file, the second element is the header.
       If 'convert_to_float' is False, the value array a strings array.
       Otherwise the value array is a 2D numpy array. In the latter case, a row is splitted using the 'split_delimiter'.
       If header is False, no header is assumed and the second element of the resulting tuple is None.
       If comment is not None, lines that start with that character are ignored.
    """
    from numpy import array, reshape

    def readlineandignorecomments():
        line = text_file.readline()
        while (line != ''):
            if (comment is None) or not line.startswith(comment):
                break
            line = text_file.readline()
        return line
    
    text_file = file(filename, "rb")
    
    line = readlineandignorecomments()
 
    header_line = None
    if header:
        header_line = re.split('\s+', line)[0:-1]
        line = readlineandignorecomments()

    line_list = re.split('\s+', line)
    ncol = len(line_list)-1
    data = []
    nrow=0
    while (line != ''):
        nrow += 1
        for column_number in range(ncol):
            data.append(line_list[column_number])
        line = readlineandignorecomments()
        line_list = re.split('\s+', line)
    text_file.close()
    if convert_to_float:
        def split_and_convert(row):
            splitted_row = row.split(split_delimiter)
            if len(splitted_row) == 1:
                return float(splitted_row[0])
            return map(lambda x: float(x), splitted_row)
        return (reshape(array(map(lambda x: split_and_convert(x), data)), (nrow, ncol)), header_line)
    return (reshape(array(data), (nrow, ncol)), header_line)

def load_from_text_file(filename, convert_to_float=False, split_delimiter=' ', comment=None):
    """Reads character data from a file. If 'convert_to_float' is False, it returns a strings array.
       Otherwise it returns a numpy array. In the latter case, a row is splitted using the 'split_delimiter'.
       If comment is not None, lines that start with that character are ignored.
    """
    from numpy import array

    text_file = file(filename, "rb")
    line = text_file.readline()
    data = []
    while (line != ''):
        while line.endswith('\n') or line.endswith('\r'):
            line = line[:-1]
        if (comment is None) or not line.startswith(comment):
            data.append(line)
        line = text_file.readline()
    text_file.close()
    if convert_to_float:
        def split_and_convert(row):
            splitted_row = row.split(split_delimiter)
            if len(splitted_row) == 1:
                return float(splitted_row[0])
            return map(lambda x: float(x), splitted_row)
        return array(map(lambda x: split_and_convert(x), data))
    return array(data)

def remove_directories_with_this_name(top, dir_name):
    """Removes any directory contained in top whose name is dir_name.
    """
    for root, dirs, files in os.walk(top, topdown=False):
        for name in dirs:
            if dir_name in name:
                shutil.rmtree(os.path.join(root, dir_name))

def replace_string_in_files(directory, find, replace):
    """
    Replace (recursively) all instances of find with replace for any file
    in directory.
    """
    from opus_core.third_party.path import path

    dir = path(directory)
    for file in dir.walkfiles():
        f = open(file)
        in_text = f.read()
        out_text = in_text.replace(find, replace)
        if in_text != out_text:
            file.write_text(out_text)

def get_distinct_list(list):
    """Returns a list of distinct elements of the argument list."""
    newlist = []
    for item in list:
        if not(item in newlist):
            newlist = newlist + [item]
    return newlist

def create_string_list(prefix, n):
    """Create a list of strings 'prefix+number' with number=1,...,n.
    """
    name_list = []
    for i in range(n):
        name_list.append(prefix + `i+1`)
    return name_list

def list2string(l, sep=' '):
    """Return a string created from the elements of the list 'l' separated by 'sep'."""
    return sep.join(["%s" % x for x in l])

def check_dimensions(array1, array2):
    """Return True if all dimensions of array1 correspond to all dimensions of array2, otherwise False.
    Both arrays hahve to be numpy arrays.
    """
    return array1.shape == array2.shape

def remove_all(valuelist, element):
    """Remove all occurences of element in the list.
    """
    result = []
    for item in valuelist:
        if element <> item:
            result.append(item)
    return result

def remove_elements_with_matched_prefix_from_list(valuelist, prefixlist):
    """Remove all occurences of elements with one of the prefix in the prefixlist
       from valuelist.
    """
    from numpy import array, reshape, compress, apply_along_axis, logical_and

    def match_prefix(prefix, arr):
        def match_single_element(item, prefix):
            q = re.match('^'+prefix, item[0])
            if q:
                return 0
            return 1
        t = apply_along_axis(match_single_element, 1, arr.reshape(arr.size,1), prefix[0])
        return t

    result = valuelist
    pl = array(prefixlist)
    m = apply_along_axis(match_prefix, 1, pl.reshape(pl.size,1), array(valuelist))
    l = logical_and(m[0,:], m[1,:])
    return compress(l, result)

def type_convert(valuelist):
    """Convert numerical values of the given list to float. Nonnumerical values are unchanged."""
    def tryconvert(x):
        try:
            return float(x)
        except:
            return x
    return map(lambda x: tryconvert(x), valuelist)

def get_distinct_names(namesarray):
    """Return a list of distinct names from a list of names"""
    from numpy import array, reshape, sort, asarray
    
    if len(namesarray) <= 0:
        return array([], dtype='int32')
    allnames = asarray(namesarray).copy()
    allnames.sort()
    n = allnames.shape[0]
    names = []
    i = 0
    while i < n:
        matches = ematch(allnames, allnames[i])
        names.append(allnames[i])
        i += len(matches)
    return reshape(array(names), (len(names),))

def take_choices(what, choices):
    """'what' is a 1D or a 2D array, 'choices' is a 1D array. It returns a 1D array of what[choices] or what[:,choices].
    """
    from numpy import zeros

    result = zeros((what.shape[0],), dtype="int32")
    if what.ndim > 1:
        for i in range(what.shape[0]):
            result[i] = what[i,choices[i]]
    else:
        result = what[choices]
    return result

def sample_1d(population, k, probabilities):
    """Called from sample, here probabilities must be 1D array."""
    from numpy import searchsorted
    from numpy.random import random

    n = population.size
    if n <> probabilities.shape[0]:
        raise StandardError, "Mismatch in size of population and probabilities."
    cumulative_probability = probabilities.cumsum()
    if cumulative_probability[n-1]<=0:
        raise StandardError, "Sum of probabilities must be > 0."
    cumulative_probability = cumulative_probability/float(cumulative_probability[n-1])
    draw = random([k])
    choices = searchsorted(cumulative_probability, draw)
    return population[choices]

def sample(population, k, probabilities=None):
    """Return a sample (array) of size k from the 'population' according to the given 'probabilities' (sampling with replacement).
    'probabilities' can be 'None', 1D or 2D array. In case of 2D array, i-th row is considered as probabilities
    for i-th draw. The probabilities do not need to sum to 1, they are rescaled within the procedure. They should
    be positive and their sum should be > 0.
    """
    from numpy import array, reshape, where, alltrue
    from numpy.random import random

    if isinstance(population, list):
        population = array(population)
    n = population.size
    if probabilities == None:
        probabilities = array(n*[1.0/n])
    if isinstance(probabilities, list):
        probabilities = array(probabilities)

    if probabilities.ndim <= 1:
        return sample_1d(population, k, probabilities)

    if (n <> probabilities.shape[1]) or (k <> probabilities.shape[0]) :
        raise StandardError, "Mismatch in size of population and probabilities."
    cumulative_probability = probabilities.cumsum(axis=1)
    if not alltrue(cumulative_probability[:,n-1]):
        raise StandardError, "Sums of probabilities must be > 0."
    cumulative_probability = cumulative_probability/reshape(cumulative_probability[:,n-1],(k,1)).astype('float32')
    draw = random([k])
    choices = reshape(n-where(reshape(draw, (k,1)) <= cumulative_probability,1,0).sum(axis=1), (k,))
    if choices.max() >= n:
        raise StandardError, "Something is wrong with the probabilities."
    return population[choices]

def intersect1d(ar1, ar2, **kwargs):
    """ wrapper for numpy.intersect1d and numpy.intersect1d_nu for different version of numpy
    """
    import numpy
    ver = numpy.__version__ 
    if ver < '1.4.0':
        f = numpy.intersect1d_nu
        return f(ar1, ar2)
    else:
        f = numpy.intersect1d
        return f(ar1, ar2, **kwargs)

def unique(arr, return_index=False, **kwargs):
    """ wrapper for numpy.unique and numpy.unique1d for different version of numpy
    """
    import numpy
    ver = numpy.__version__ 
    if ver < '1.2.0':   #numpy 1.0 and 1.1 don't accept extra argument
        f = numpy.unique1d
        return f(arr, return_index=return_index)[::-1]
    elif ver < '1.3.0': #numpy 1.2+ accepts return_inverse argument
        f = numpy.unique1d
        return f(arr, return_index=return_index, **kwargs)[::-1]
    elif ver < '1.4.0': #numpy 1.3 reverses the order of outputs from unique1d
        f = numpy.unique1d
    else:               #unique1d is deprecated in numpy 1.4+, use unique instead
        f = numpy.unique
    return f(arr, return_index=return_index, **kwargs)

def uniquend(arr):
    """Returns unique elements of arr; works with n-dimension array
    """
#    from numpy import array, reshape, where, concatenate
#
#    new_array = reshape(array(arr[0]), (1,arr.shape[1]))
#    if arr.shape[0] > 1:
#        for item in arr[1:]:
#            s = new_array.sum(axis=1)
#            w = where(s == arr.shape[1])[0]
#            if w.size <= 0:
#                new_array = concatenate((new_array,reshape(item, (1,arr.shape[1]))))
#    if arr.ndim == 1:
#        return reshape(new_array,(arr.size,))
#    return new_array

##   LW: was above, which I think is incorrect:
#from numpy.randon import randint
#arr=randint(0, 3, size=100) 
#arr.resize((50,2))
#unique(arr)
#>>>array([[2, 0]])  #depending on the values of b, sometimes unique gives correct results by chance

    if arr.ndim == 1:
        return unique(arr)
    
    d = {}
    for element in arr:
        k = totuple(element)
        if k not in d.keys():
            d[k] = 1
        else:
            d[k] += 1
    return array(d.keys())

def has_this_method(object, method_name):
    """Does this object have a method named method_name?"""
    members = getmembers(object)
    method_found = map(lambda x: method_name in x, members)
    return (1 in method_found) and ismethod(getattr(object, method_name))

def all_in_list(list1, list2):
    """ Return 1 if all elements of list1 are contained in list2, otherwise 0."""
    return set(list1) <= set(list2)

def do_id_mapping(recarray, fieldname):
    return do_id_mapping_dict_from_array(recarray.field(fieldname))

def do_id_mapping_dict_from_array(id_array):
    from numpy import ndarray

    if isinstance(id_array, ndarray) and id_array.ndim > 1: # transfer to tuples, since dict does not work with arrays as keys
        new_id_array = map(lambda x: tuple(x.tolist()), id_array)
    else:
        new_id_array = id_array
    id_mapping = {}
    i = 0
    for row in new_id_array:
        id_mapping[row] = i
        i += 1
    return id_mapping

def do_id_mapping_array_from_array(id_array, minid=None, maxid=None):
    # id_array must be a 1D numpy array
    from numpy import resize, array, arange

    if id_array.size <= 0:
        return array([], dtype="int32")
    if maxid is None:
        maxid = id_array.max()
    if minid is None:
        minid = id_array.min()
    id_mapping = resize(array([-1], dtype="int32"), maxid-minid+1)
    id_mapping[id_array-minid] = arange(id_array.size).astype(id_mapping.dtype)
    return id_mapping


def remove_from_array(arr, index):
    """Remove elements given by index from a numpy 'arr'."""
    from numpy import compress, ones

    a = ones(arr.shape, dtype="int32")
    a[index] = 0
    return compress(a,arr)

def flatten_list(list):
    """Flattens a nested 'list' (of 2 levels)."""
    return [element for sublist in list for element in sublist]

def ncumsum(prob_array, axis=0, dtype='float64'):
    """n(ormalized)-cumsum that normalizes the cumsum result by dividing the array
    by the last item in cumsum result"""
    from numpy import take, ma

    if not ma.allclose(prob_array.sum(axis=axis, dtype=dtype), 1.0, rtol=1.e-2):
        raise ValueError, "The probability array must sum up to 1. It is " + \
                               str(prob_array.sum(axis=axis, dtype=dtype))

    cum_prob = prob_array.cumsum(axis=axis, dtype=dtype)
    return cum_prob / take(cum_prob, (-1,), axis=axis)

def corr(var_array, *var_arrays):
    """return the correlation between vars"""
    from numpy import zeros, concatenate, newaxis, dot, transpose

    try:
        if var_array.ndim == 2:
            X = var_array
        elif var_array.ndim == 1:
            X = var_array[:, newaxis]

        for var in var_arrays:
            if var_array.ndim == 2:
                Y = var
            elif var_array.ndim == 1:
                Y = var[:, newaxis]
            X = concatenate((X, Y), axis=1)
    except:
        raise ValueError, "Input variable arrays must have the same number of observations"

    Z = zeros(X.shape).astype('float32')
    nobs, nvar = X.shape

    for col in range(nvar):
        mean = X[:,col].mean()
        sd = standard_deviation(X[:,col])
        sd = sd * ((nobs-1)/float(nobs))**.5
        #from numpy import power
        #sd = power(sum(power((X[:,col] - mean),2)) / nobs, .5)
        Z[:,col] = (X[:,col] - mean) / sd

    R = dot(transpose(Z), Z) / nobs

    return R

def quantile(values, probs):
    """Return quantiles of given probability from the values. 'values' and probs are numpys.
    The function returns an array of the same shape as 'probs'. Quantile is here defined as
    the nearest order statistic."""
    from numpy import sort, maximum

    sorted_values = sort(values)
    return sorted_values[maximum((probs*values.size-1).astype("int32"),0)]

def is_masked_array(a):
    """test whether the argument is a masked array.  (This is a function because ma.array used
    to be a class, and now it's a function, and the actual class changed subpackage, so we can't just
    test it directly.)"""
    ma_array_type = type(ma.array([3]))
    return isinstance(a, ma_array_type)
def unique_values(arr, return_index=False, **kwargs):
    import warnings
    warnings.warn("opus_core.misc.unique_values is deprecated; use opus_core.misc.unique instead.", DeprecationWarning)
    return unique(arr, return_index=return_index, **kwargs)

#def unique_values(input_array, sort_values=True):
#    """return unique elements of input_array
#    input_array - a sortable numpy array or list object
#    """
#    from numpy import array, ndarray, sort, where
#    import copy
#    if isinstance(input_array, ndarray):
#        if input_array.ndim <> 1:
#            input_array = input_array.ravel()
#            raise RuntimeWarning, "input_array is converted into a rank-1 array"
#    elif not isinstance(input_array, list):
#        raise TypeError, "input_array must be of type ndarray or list."
#
#    n = len(input_array)
#    if n == 0:
#        return array([], dtype='int32')
#
#    t = copy.copy(input_array)
#    try:
#        t.sort()
#    except TypeError:
#        del t
#        raise RuntimeError, "input_array is not sortable; unique_values fails."
#    else:
#        assert n > 0
#        last = t[0]
#        lasti = i = 1
#        while i < n:
#            if t[i] != last:
#                t[lasti] = last = t[i]
#                lasti += 1
#            i += 1
#    if sort_values:
#        return t[:lasti]
#    else:
#        if isinstance(input_array, ndarray):
#            unsorted_index = [where(input_array==v)[0][0] for v in t[:lasti]]
#            unsorted_index.sort()
#            return input_array[unsorted_index]
#        else:
#            unsorted_index = [input_array.index(v) for v in t[:lasti]]
#            unsorted_index.sort()
#            return [input_array[n] for n in unsorted_index]
       
def ismember(ar1, ar2) :
    """Return a Boolean 1-d array of the length of ar1 which is True whenever that 
    element is contained in ar2 and False when it is not.
    (The numpy function setmember1d claims to do the same but works only on ar1 with unique values.) 
    """
    import numpy
    if numpy.__version__ >= '1.4.0':
        return numpy.in1d(ar1, ar2)
    
    a = numpy.sort(ar2)
    il = a.searchsorted(ar1, side='left')
    ir = a.searchsorted(ar1, side='right')
    return ir != il
    
def get_host_name():
    """Get the host name of this computer in a platform-independent manner."""
    fullname = socket.gethostname()
    # Depending on the operating system, fullname might be just the machine name,
    # or might also have the full internet address; and it might be in lower or
    # upper case.  Normalize to be just the machine name, in lower case.
    return fullname.split('.')[0].lower()

def clip_to_zero_if_needed(values, function=""):
    from numpy import clip

    global_min = values.min()
    if global_min >= 0:
        return values
    global_max = values.max()
    logger.log_warning("Negative values detected in function/method '%s'" % function)
    logger.log_warning("Minimum: %s. Negative values clipped to zero." % global_min)
    return clip(values, 0, global_max)

def convert_lower_case_with_underscores_into_camel_case(name):
    """Creates CamelCase name from this lower_case_with_underscores name.
    """
    return ''.join(map(lambda s: s.capitalize(), name.split('_')))

def get_camel_case_class_name_from_opus_path(opus_path):
    """return CamelCase class name from opus_path.
    """
    class_name = opus_path.split('.')[-1]
    class_name = convert_lower_case_with_underscores_into_camel_case(class_name)    
    return class_name

def create_import_for_camel_case_class(opus_path, import_as=None):
    """Creates statement to import this class.

    opus_path is full Opus path.
    Module name is lower_case_with_underscores.
    Class name is CamelCase version of module name.
    To do import, exec returned statement.
    """
    class_name = get_camel_case_class_name_from_opus_path(opus_path)
    if import_as is not None:
        return 'from %s import %s as %s' % (opus_path, class_name, import_as)
    else:
        return 'from %s import %s' % (opus_path, class_name)

def get_config_from_opus_path(opus_path):
    class_name = get_camel_case_class_name_from_opus_path(opus_path)
    import_stmt = 'from %s import %s' % (opus_path, class_name)
    exec(import_stmt)

    # Create a local variable 'config' with the configuration.
    stmt = 'config = %s()' % class_name
    exec(stmt)

    # Return the config that we just created.
    return config

def create_import_for_class(classpath, class_name):
    """Creates an import statement that may be exec'ed to import the given class
    from the Opus path specified by the config_key.
    """
    return 'from %s import %s' % (classpath, class_name)

def is_file_in_directory(file, directory):
    """Return True if 'file' in 'directory', otherwise False."""
    files = os.listdir(directory)
    if file in files:
        return True
    return False

def safe_array_divide(numerator, denominator, return_value_if_denominator_is_zero=0.0, type='float32'):
    """If denominator == 0, return return_value_if_denominator_is_zero.
        Else return numerator / denominator. numerator and denominator must be numpy arrays."""
    from numpy import ma

    return ma.filled(numerator/ma.masked_where(denominator == 0, denominator.astype(type)), return_value_if_denominator_is_zero)

def try_transformation(data, transformation):
    """Performs 'transformation' on 'data'. Transformation is a character string naming a function
       implemented in numpy, e.g. 'sqrt', 'log'. It can be also '**2' for power, or '* 10' for simple
       multiplication (the same holds for addition etc.). The 'data' is a numpy array.
       If the procedure fails, a warning is issued and
       the raw data are returned. Otherwise the transformed data are returned.
    """
    if transformation is None:
        tdata = data
    else:
        try:
            exec("from numpy import %s" % transformation)
            tdata = eval("%s(data)" % transformation)
        except:
            try:
                tdata = eval("data%s" % transformation) # would work for e.g. **2, * 10, ...
            except:
                logger.log_warning("Transformation not successful. Using raw data instead.")
                tdata = data
    return tdata

def create_combination_indices(shape):
    """Creates an index array which is a combination of all posibilities in shape. shape is a tuple.""" 
    from numpy import product, indices, zeros, array
    lshape = len(shape)
    if lshape == 0:
        return array([])
    tindices = indices(shape)
    index = zeros((product(shape), lshape), dtype="int32")
    for idim in range(lshape):
        index[:,idim] = tindices[idim].ravel()
    return index

def get_string_or_None(arg):
    if arg is not None:
        return "'%s'" % arg
    return None

def digits(int_scalar_or_int_sequence):
    """ return number of digits """
    if hasattr(int_scalar_or_int_sequence, '__iter__'):
        return [digits(scalar) for scalar in int_scalar_or_int_sequence]

    n = int_scalar_or_int_sequence
    if n < 0:
        n = -n
    d = 0
    step = 1
    while (step <= n):
        d += 1
        step *= 10
    return max(d, 1)

def djbhash(sequence):
    """Hash function from D J Bernstein
    References: 
    http://www.gossamer-threads.com/lists/python/python/679002#679002
    http://eternallyconfuzzled.com/tuts/algorithms/jsw_tut_hashing.aspx
    """
    h = 5381L
    for i in sequence:
        t = (h * 33) & 0xffffffffL
        h = t ^ i
    return h 

def fnvhash(sequence):
    """Fowler, Noll, Vo Hash function
    References: 
    http://www.gossamer-threads.com/lists/python/python/679002#679002
    http://eternallyconfuzzled.com/tuts/algorithms/jsw_tut_hashing.aspx
    http://www.isthe.com/chongo/tech/comp/fnv/
    """
    h = 2166136261
    for i in sequence:
        t = (h * 16777619) & 0xffffffffL
        h = t ^ i
    return h

def ndsum(input, labels, index=None):
    """ extend scipy.ndimage.sum to handle labels with multi-array
    index argument is not used

    e.g.
    input =  array([3, 7, 4, 6, 2, 5 ])
    attr_a = array([0, 0, 1, 0, 1, 1])
    attr_b = array([3, 1, 2, 1, 2, 0])
    result = ndsum(input, labels=column_stack([attr_a, attr_b]))
    print result
    >>> (array([13, 3, 5, 6]), (array([0, 0, 1, 1]), array([1, 3, 0, 2])) )
    """
    from numpy import array, ndarray
    from scipy.ndimage import sum
    if labels is None or not isinstance(labels, ndarray):
        return sum(input, labels=labels, index=index)
    
    assert input.size == labels.shape[0]
    #labels = column_stack(labels)
    hash_table = {}
    def hashlabel(label):
        hash_value = djbhash(label)
        hash_table.update({hash_value:label})
        return hash_value
    labels_hash = array(map(hashlabel, labels)).astype("int32")

    index = array(hash_table.keys()).astype("int32")
    value = array(hash_table.values())
    result = sum(input, labels=labels_hash, index=index)

    return array(result), [value[:, col] for col in range(value.shape[-1])]

def get_dataset_from_storage(dataset_name, directory, storage_type, package_order=['opus_core'], dataset_args=None):
    """ Returns an object of class Dataset (or its child) with data stored in a storage of type 'storage_type' in 'directory'. If the child class is defined in a specific package, 
    this package must be included in 'package_order'. If there is no child class definition for this 'dataset_name', set 'dataset_args' to a dictionary 
    (possibly empty) and a generic Dataset will be returned. 'dataset_args' should contain entries needed as arguments for the Dataset class, e.g. 'in_table_name', 'id_name'.
    """
    from opus_core.storage_factory import StorageFactory
    from opus_core.datasets.dataset_pool import DatasetPool
    from opus_core.datasets.dataset_factory import DatasetFactory
    from opus_core.datasets.dataset import Dataset
    
    storage = StorageFactory().get_storage(storage_type, storage_location = directory)
    if dataset_args is None:
        pool = DatasetPool(storage=storage, package_order=package_order)
        return pool.get_dataset(dataset_name)
    dataset_args.update({'in_storage':storage})
    try:
        return DatasetFactory().search_for_dataset(dataset_name, package_order, arguments=dataset_args)
    except: # take generic dataset
        return Dataset(dataset_name=dataset_name, **dataset_args)
    
def get_dataset_from_tab_storage(dataset_name, directory, package_order=['opus_core'], dataset_args=None):
    """See doc string to get_dataset_from_storage which  is called with storage_type='tab_storage'."""
    return get_dataset_from_storage(dataset_name, directory, 'tab_storage', package_order=package_order, dataset_args=dataset_args)

def lookup(subarray, fullarray, index_if_not_found=-1):
    """
    look up subarray in fullarray, return the index of
    subarray's elements in fullarray; fill index with
    index_if_not_found for elements not found in fullarray

    >>> a = array([1, 9, 2, 7, 3, 5, 6])
    >>> b = array([0, 3, 2, 9, 7, 10])
    >>> lookup(b, a)
    array([-1, 4, 2, 1, 3, -1])
    """
    from numpy import arange, searchsorted, not_equal, rank
    if rank(subarray)!=1 or rank(fullarray)!=1:
        raise ValueError, "lookup only works with 1-d input arrays."
    
    array_size = fullarray.size
    index_all = arange(array_size)
    index_argsort = fullarray.argsort()
    index_sorted = searchsorted(fullarray[index_argsort], subarray)
    ## to avoid "index out of range" error
    index_sorted[index_sorted == array_size] = array_size - 1
    index_unsorted = index_all[index_argsort][index_sorted]
    index_unsorted[not_equal(fullarray[index_unsorted], subarray)] = index_if_not_found
    return index_unsorted
 
def totuple(arr):
    """
    equivalent of tolist() for ndarray    
    """
    return tuple(map(totuple, arr)) if arr.ndim>1 else tuple(arr)

from opus_core.tests import opus_unittest
import opus_core

class MiscellaneousTests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        # make a temp directory for use by multiple tests
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
    def tearDown(self):
        # remove the temp directory (note that tearDown gets called even if a unit tests fails)
        shutil.rmtree(self.temp_dir)

    def test_digits(self):
        import copy
        a = 382795
        d1 = digits(a)
        self.assertEqual(d1, 6)
        self.assertEqual(a, 382795)

        b = [0, -777, 777, 328795, 23]
        c = copy.copy(b)
        d2 = digits(b)
        self.assertEqual(d2, [1, 3, 3, 6, 2])
        self.assertEqual(b, c)

    def test_ndsum(self):
        from numpy import array, column_stack, argsort, allclose, zeros
        input =  array([3, 7, 4, 6, 2, 5 ])
        attr_a = array([0, 0, 1, 0, 1, 1])
        attr_b = array([3, 1, 2, 1, 2, 0])
        result = ndsum(input, labels=column_stack([attr_a, attr_b]))
        result_mat = zeros( (1+result[1][0].max(), 1+result[1][1].max()) )
        result_mat[result[1]] = result[0]
        
        expected = ( array([13, 3, 5, 6]), (array([0, 0, 1, 1]), array([1, 3, 0, 2])) )
        expected_mat = zeros( (2, 4)) 
        expected_mat[expected[1]] = expected[0]
        
        self.assert_(allclose(result_mat, expected_mat))

       
    def test_opus_path_for_variable_from_module_path(self):
        file_path = os.path.join('C:', 'foo', 'workspace', 'package_name', 'dataset_name', 'variable_name.py')
        self.assertEqual(opus_path_for_variable_from_module_path(file_path),
                         'package_name.dataset_name.variable_name')

    def test_create_import_for_camel_case_class(self):
        self.assertEqual(create_import_for_camel_case_class('a_package.a_dir.a_class', import_as='alias'),
                         'from a_package.a_dir.a_class import AClass as alias')
        self.assertEqual(create_import_for_camel_case_class('a_package.a_dir.a_class'),
                         'from a_package.a_dir.a_class import AClass')

    def test_remove_directories_with_this_name(self):
        files = [
            ['CVS', 'f1'],
            ['d1', 'f2'],
            ['d1', 'CVS', 'f3'],
            ['f4'],
            ]
        for t in files:
            path = self.temp_dir
            for n in t:
                path = os.path.join(path, n)
            os.makedirs(path)
            self.assert_(os.path.exists(path))
        remove_directories_with_this_name(self.temp_dir, 'CVS')
        for t in files:
            path = self.temp_dir
            for n in t:
                path = os.path.join(path, n)
            if 'CVS' in t:
                self.assert_(not os.path.exists(path))
            else:
                self.assert_(os.path.exists(path))
        # make sure we didn't accidentally delete the temp directory itself
        self.assert_(os.path.exists(self.temp_dir))

    def test_concatenate_on_strings(self):
        from numpy import array, concatenate, alltrue

        a = array(['a','bb','ccc'])
        b = array(['ddd','ee'])
        self.assert_(alltrue(concatenate([a,b]) == array(['a','bb','ccc','ddd','ee'])))

    def test_concatenate_on_ints(self):
        from numpy import array, concatenate, alltrue

        a = array([1,2,3])
        b = array([44,55])
        self.assert_(alltrue(concatenate([a,b]) == array([1,2,3,44,55])))

    def test_concatenate_on_mix_of_ints_and_floats(self):
        from numpy import array, concatenate, alltrue

        a = array([1,2,3])
        b = array([4.4,5.5])
        self.assert_(alltrue(concatenate([a,b]) == array([1,2,3,4.4,5.5])))

    #def test_concatenate_on_mix_of_ints_and_strings(self):
        #a = array(['a','bb','ccc'])
        #b = array([44,55])
        #threw_exception = False
        #try:
            #concatenate([a,b])
        #except Exception:
            #threw_exception = True
        #self.assert_(threw_exception)

    def test_concatenate_on_2d_ints(self):
        from numpy import array, reshape, concatenate

        a = array([['1','2','3'],['4','5','6']])
        b = array(['44','55']).reshape(2,1)
        try:
            concatenate([a,b])
        except Exception:
            threw_exception = True
        self.assert_(threw_exception)

    def test_clip_to_zero_if_needed(self):
        from numpy import array, ma

        logger.enable_hidden_error_and_warning_words()
        result = clip_to_zero_if_needed(array([0,3,6,-4,8]), "test1")
        logger.disable_hidden_error_and_warning_words()
        self.assertEqual(ma.allequal(result, array([0,3,6,0,8])), True, msg = "Error in test_clip_to_zero_if_needed" )

        result = clip_to_zero_if_needed(array([0,3,6,4,8.5]), "test2")
        self.assertEqual(ma.allequal(result, array([0,3,6,4,8.5])), True, msg = "Error in test_clip_to_zero_if_needed" )

    def test_module_path_from_opus_path(self):
        opus_core_path = opus_core.__path__[0]
        self.assertEqual(module_path_from_opus_path('opus_core.__init__'),
                         os.path.join(opus_core_path, '__init__.py'))

    def test_create_import_for_class(self):
        config = {'model':'opus_core.model'}
        expected_import_statement = 'from opus_core.model import Model'
        import_statement = create_import_for_class(config['model'], 'Model')

        self.assertEqual(import_statement, expected_import_statement)

    def test_is_file_in_directory(self):
        opus_core_path = opus_core.__path__[0]
        self.assertEqual(is_file_in_directory('data', opus_core_path), True)
        self.assertEqual(is_file_in_directory('dataxxx', opus_core_path), False)

    def test_safe_array_divide(self):
        from numpy import array, ma

        a = array([10, 20, 30, 40])
        b = array([4, 0, 10, 0])
        self.assertEqual(ma.allequal(safe_array_divide(a,b), array([2.5, 0, 3, 0])), True)

    def test_transformation(self):
        from numpy import array, ma

        a = array([9, 4, 25, 36])
        self.assertEqual(ma.allequal(try_transformation(a, "sqrt"), array([3, 2, 5, 6])), True)
        self.assertEqual(ma.allequal(try_transformation(a, "*2"), array([18, 8, 50, 72])), True)
        self.assertEqual(ma.allequal(try_transformation(a, "**2"), a**2), True)

    def test_quantile(self):
        from numpy import array, ma

        a = array([35, 6, 22, 1, 60])
        b = array([6, 3, 5, 9, 1, 7, 10, 2, 8, 4, 0])
        self.assertEqual(ma.allequal(quantile(a, array([0.2, 0.9, 0.5])), array([1, 35, 6])), True)
        self.assertEqual(ma.allequal(quantile(b, array([0, 0.2, 0.9, 0.5, 1])), array([0, 1, 8, 4, 10])), True)

    def test_remove_elements_with_matched_prefix(self):
        from numpy import array, alltrue

        a = array(["max_attribute1", "min_attribute1", "attribute1", "attribute2_max", "attribute2"])
        prefix_list = ["min", "max"]
        result = remove_elements_with_matched_prefix_from_list(a, prefix_list)
        self.assertEqual(result.size == 3, True, msg = "Error in test_remove_elements_with_matched_prefix: Size of the resulting array must be 3.")
        self.assertEqual(alltrue(result == array(["attribute1", "attribute2_max", "attribute2"])), True,
                         msg = "Error in test_remove_elements_with_matched_prefix" )
        
    def test_remove_elements_with_matched_prefix_with_constraints_header(self):
        from numpy import array, alltrue

        a = array(["constraint_id", "city_id", "is_in_wetland", "min_units", "max_units", "min_commercial_sqft", 
                   "max_commercial_sqft", "min_industrial_sqft", "max_industrial_sqft"])
        prefix_list = ["min", "max"]
        result = remove_elements_with_matched_prefix_from_list(a, prefix_list)
        self.assertEqual(result.size == 3, True, msg = "Error in test_remove_elements_with_matched_prefix_with_constraints_header: Size of the resulting array must be 3.")
        self.assertEqual(alltrue(result == array(["constraint_id", "city_id", "is_in_wetland"])), True,
                         msg = "Error in test_remove_elements_with_matched_prefix_with_constraints_header" )

    def test_ematch(self):
        from numpy import array, ma

        self.assertEqual(ma.allequal(ematch(array(["abcde", "abcd"]), "abcd"), array([1])), True,
                         msg = "Error in ematch.")
        self.assertEqual(ma.allequal(ematch(array(["ab(c]de", "abcd"]), "ab(c]de"), array([0])), True,
                         msg = "Error in ematch.")
    def test_get_indices_of_matched_items(self):
        from numpy import array, ma
        self.assertEqual(ma.allequal(get_indices_of_matched_items(array(["abcde", "abcd", "vvv"]), 
                                                                  array(["abcd", "vvv"])), array([1,2])), True,
                         msg = "Error in get_indices_of_matched_items.")
            
    def test_directory_path_from_opus_path(self):
        path_to_opus_core = opus_core.__path__[0]
        input_output = (
            ('opus_core.tests', os.path.join(path_to_opus_core, 'tests')),
            ('opus_core.a_directory_that_does_not_exist', os.path.join(path_to_opus_core, 'a_directory_that_does_not_exist')),
            ('opus_core', os.path.join(path_to_opus_core)),
        )
        for input, output in input_output:
            result = directory_path_from_opus_path(input)
            self.assertEqual(result, output)

    def test_is_masked_array(self):
        import numpy
        a1 = ma.array([3])
        self.assert_(is_masked_array(a1))
        a2 = numpy.array([4])
        self.assert_(not is_masked_array(a2))
        
    def test_copytree(self):
        dest = os.path.join(self.temp_dir, 'dest')
        os.mkdir(dest)
        dirs = [
            ['d1', 'd2', 'd3', 'CVS', 'sub'],
            ['d2', 'd3'],
            ['d4', 'CVS', 'd1'],
            ['d5'],
            ['d6', '.svn', 'd1', 'd2'],
            ]
        for t in dirs:
            path = self.temp_dir
            for n in t:
                path = os.path.join(path, n)
            os.makedirs(path)
            source = os.path.join(self.temp_dir, t[0])
            sub = os.path.join(dest, t[0])
            copytree(source, sub, skip_subdirectories=['CVS', '.svn'])
        for t in dirs:
            path = dest
            for n in t:
                path = os.path.join(path, n)
            if 'CVS' in t or '.svn' in t:
                self.assert_(not os.path.exists(path))
            else:
                self.assert_(os.path.exists(path))

    def test_unique(self):
        from numpy import array

        a = array([0.01, 0.1, 0.01, 0.2, 0.1, 0.5, 0.08])
        self.assertArraysEqual(unique(a), array([0.01, 0.08, 0.1, 0.2, 0.5]))
        self.assertArraysEqual(unique(a, return_index=True)[0], array([0.01, 0.08, 0.1, 0.2, 0.5]))
        self.assertArraysEqual(unique(a, return_index=True)[1], array([0, 6, 1, 3, 5]))
        b = [0.01, 0.1, 0.01, 0.2, 0.1, 0.5, 0.08]
        self.assertArraysEqual(unique(b), array([0.01, 0.08, 0.1, 0.2, 0.5]))
        self.assertArraysEqual(unique(b, return_index=True)[0], array([0.01, 0.08, 0.1, 0.2, 0.5]))
        self.assertArraysEqual(unique(b, return_index=True)[1], array([0, 6, 1, 3, 5]))
        
    def test_get_dataset_from_tab_storage(self):
        import opus_core
        
        attribute = 'g2'
        location = os.path.join(opus_core.__path__[0], 'data', 'tab')
        dataset = get_dataset_from_tab_storage('test', directory=location)
        self.assertAlmostEqual(21, dataset.attribute_sum(attribute))
        
    def test_list2string(self):
        self.assertEqual(list2string([42, 900.4, 20.333]), "42 900.4 20.333")
        self.assertEqual(list2string(["aaa", 5, "xx", 6.8], sep=', '), "aaa, 5, xx, 6.8")   
        
    def test_get_distinct_list(self):
        self.assertEquals(get_distinct_list([]), [])
        self.assertEquals(get_distinct_list(['zxq', 'zxq', 5.4, 9, ['3', 'a'], 5.4, 5.4, ['3', 'a']]), ['zxq', 5.4, 9, ['3', 'a']] )
        
    def test_create_list_string(self):
        self.assertEquals(create_list_string(['aa', 'b', '', ' dd'], 'SEP'), 'aaSEPbSEPSEP dd')
             
    def test_flatten_list(self):
        nestedList = [3, 4.0, 'five']
        testList = [nestedList]
        self.assertEquals(flatten_list(testList), nestedList)
        
    def test_ismember(self):
        from numpy import array
        a = array([1, 2])
        b = array([1, 2])
        c = array([1, 1])
        d = array([2, 1, 2, 2, 1])
        e = array([])
        f = array([3,1])       
        self.assertEqual(ismember(a,a).all(), ismember(a,b).all(), array([True, True]).all())
        self.assertEqual(ismember(c,a).all(), ismember(a,d).all(), array([True, True]).all())
        self.assertEqual(ismember(d,a).all(), array([True, True, True, True, True]).all())
        self.assertEqual(ismember(d,c).all(), array([False, True, False, False, True]).all())
        self.assertEqual(ismember(a,c).all(), array([True, False]).all())
        self.assertEqual(ismember(a,f).all(), array([False, True]).all())
        self.assertEqual(ismember(a,e).all(), ismember(a,f).all(), array([False, False]).all())
     
    # also tests the load_from_text_file function
    def test_write_to_text_file(self):
        from numpy import array
        file_name = os.path.join(self.temp_dir,'misc_test_file')
        arr = array(['a', 'b', 'c'])
        delim = '|'
        write_to_text_file(file_name, arr, 'wb', delim)
        written_data = ''
        i=0
        for i in range(len(arr)-1):
            written_data += (arr[i] + delim) 
        written_data += arr[i+1]
        self.assertEqual(load_from_text_file(file_name), written_data)

    def test_create_string_list(self):
        self.assertEqual(create_string_list('prefix',0), [])
        self.assertEqual(create_string_list('prefix',3), ['prefix1','prefix2','prefix3'])

    def test_remove_all(self):
        self.assertEqual(remove_all((),()), [])
        self.assertEqual(remove_all((1,'a'),'b'), [1,'a'])
        self.assertEqual(remove_all(('a', 1,'a', 'a'),'a'), [1])
        
    def test_lookup(self):
        from numpy import array, alltrue
        a = array([1, 9, 2, 7, 3, 5, 6])
        b = array([0, 3, 2, 9, 7, 10])
        expected = array([-1, 4, 2, 1, 3, -1])
        self.assert_(alltrue(lookup(b, a)==expected))

    def test_totuple(self):
        a = array([1, 2, 3, 5, 7, 9])
        result = totuple(a)
        self.assertEqual(result, (1,2,3,5,7,9))

        a = array([[1, 2], [3, 5], [7,9]])
        result = totuple(a)
        self.assertEqual(result, ((1,2),(3,5),(7,9)))

        a = array([[[1, 2], [3, 5]], [[7, 9], [4, 6]]])
        result = totuple(a)
        self.assertEqual(result, (((1,2),(3,5)),((7,9), (4,6))))
            
    def test_uniquend(self):
        from numpy.random import randint
             
        b = randint(0, 5, size=100)
        result = uniquend(b)
        self.assertTrue( all([i in b for i in result]) )
        self.assertTrue( all([i in result for i in b]) )
        self.assertTrue( set(b) == set(result) )
        
        b = randint(0, 3, size=100)
        b.resize((50,2))
        result = uniquend(b)
        self.assertTrue( all([i in b for i in result]) )
        self.assertTrue( all([i in result for i in b]) )
        self.assertTrue( set(totuple(b)) == set(totuple(result)) )
        
        b = randint(0, 2, size=54)
        b.resize((9,3,2))
        result = uniquend(b)
        self.assertTrue( all([i in b for i in result]) )
        self.assertTrue( all([i in result for i in b]) )
        self.assertTrue( set(totuple(b)) == set(totuple(result)) )
        
if __name__ == "__main__":
    opus_unittest.main()
