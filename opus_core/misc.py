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

"""Collection of useful miscellaneous functions and definitions"""

import copy
import os
import os.path
import re
import shutil
import socket
import sys
import tempfile

from opus_core.logger import logger
#from numpy import float32
from scipy.ndimage import standard_deviation
from inspect import getmembers, ismethod
from exceptions import Exception


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

def get_field_names(recarray, lower=True):
    """Returns a list of field names of a record array. If lower equals 1, the names are transformed to lower case."""
    # using list comprehensions make things clearer, and we only do the (lower) test *once*
    if lower:
        return [field.lower() for field in recarray.dtype.fields.keys()]
    else:
        return [field for field in recarray.dtype.fields.keys()]

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
    parts = file_path.rsplit(os.sep, 3)
    package_name = parts[-3]
    dataset_name = parts[-2]
    module_name = parts[-1]
    # only remove the extension
    variable_name = module_name.rsplit('.', 1)[0]
    # return opus_path
    return '.'.join((package_name, dataset_name, variable_name))

def get_temp_file_name():
    temp_fd, temp_file_name = tempfile.mkstemp()
    os.close(temp_fd)
    return temp_file_name

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

def load_from_file(filename, byteorder=DEFAULT_BYTEORDER, type='float32'):
    from numpy import fromfile

    """Reads float data from a file."""
    float_file = file(filename, mode="rb")
    data = fromfile(float_file,dtype=type)
    float_file.close()
    byteswap_if_needed(data, byteorder)
    return data

def load_table_from_text_file(filename, convert_to_float=False, split_delimiter=' ', header=False):

    """Reads table from a file. If 'convert_to_float' is False, it returns a strings array.
       Otherwise it returns a 2D numpy array. In the latter case, a row is splitted using the 'split_delimiter'.
    """
    from numpy import array, reshape

    text_file = file(filename, "rb")
    line = text_file.readline()
    header_line = None
    if header:
        header_line = re.split('\s+', line)[0:-1]
        line = text_file.readline()
    line_list = re.split('\s+', line)
    ncol = len(line_list)-1
    data = []
    nrow=0
    while (line != ''):
        nrow += 1
        for column_number in range(ncol):
            data.append(line_list[column_number])
        line = text_file.readline()
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

def load_from_text_file(filename, convert_to_float=False, split_delimiter=' '):
    """Reads character data from a file. If 'convert_to_float' is False, it returns a strings array.
       Otherwise it returns a numpy array. In the latter case, a row is splitted using the 'split_delimiter'.
    """
    from numpy import array

    text_file = file(filename, "rb")
    line = text_file.readline()
    data = []
    while (line != ''):
        while line.endswith('\n') or line.endswith('\r'):
            line = line[:-1]
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
    from opus_core.path import path

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

def create_name_array(prefix,cols,rows,z):
    from numpy import array, reshape

    name_list = []
    if z <= 1:
        if rows == 1: #1d array
            name_list=create_string_list(prefix,cols)
        else:         #2d array
            for j in range(rows):
                for i in range(cols):
                    name_list.append(prefix + `j+1` + '_' + `i+1`)
    else:             # 3d array
        for j in range(rows):
            for i in range(cols):
                for k in range(z):
                    name_list.append(prefix + `j+1` + '_' + `i+1` + '_' + `k+1`)
    return reshape(array(name_list), (rows*cols*z,))

def create_string_list(prefix, n):
    """Create a list of strings 'prefix+number' with number=1,...,n.
    """
    name_list = []
    for i in range(n):
        name_list.append(prefix + `i+1`)
    return name_list

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

def unique(arr):
    """Return an array of unique elements.
    """
    from numpy import array, reshape, where, concatenate

    new_array = reshape(array(arr[0]), (1,arr.shape[1]))
    if arr.shape[0] > 1:
        for item in arr[1:]:
            s = new_array.sum(axis=1)
            w = where(s == arr.shape[1])[0]
            if w.size <= 0:
                new_array = concatenate((new_array,reshape(item, (1,arr.shape[1]))))
    if arr.ndim == 1:
        return reshape(new_array,(arr.size,))
    return new_array

def switch(arr, pos1, pos2):
    """Exchange the 'pos1'-th item in the array 'arr' with the one on the 'pos2'-th position."""
    from numpy import arange

    index = arange(arr.size)
    index[pos2] = pos1
    index[pos1] = pos2
    return arr[index]

def has_this_method(object, method_name):
    """Does this object have a method named method_name?"""
    members = getmembers(object)
    method_found = map(lambda x: method_name in x, members)
    return (1 in method_found) and ismethod(getattr(object, method_name))

def all_in_list(list1, list2):
    """ Return 1 if all elements of list1 are contained in list2, otherwise 0."""
    a = map(lambda x: x in list2, list1)
    return not (0 in a)

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

def do_id_mapping_array_from_array(id_array):
    # id_array must be a 1D numpy array
    from numpy import resize, array, arange

    if id_array.size <= 0:
        return array([], dtype="int32")
    maxid = id_array.max()
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

def ncumsum(prob_array,axis=0, dtype='float64'):
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

def unique_values(input_array, sort_values=True):
    """return unique elements of input_array
    input_array - a sortable numpy array or list object
    """
    from numpy import array, ndarray, sort, where
    import copy
    if isinstance(input_array, ndarray):
        if input_array.ndim <> 1:
            input_array = input_array.ravel()
            raise RuntimeWarning, "input_array is converted into a rank-1 array"
    elif not isinstance(input_array, list):
        raise TypeError, "input_array must be of type ndarray or list."

    n = len(input_array)
    if n == 0:
        return array([], dtype='int32')

    t = copy.copy(input_array)
    try:
        t.sort()
    except TypeError:
        del t
        raise RuntimeError, "input_array is not sortable; unique_values fails."
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
    if sort_values:
        return t[:lasti]
    else:
        if isinstance(input_array, ndarray):
            unsorted_index = [where(input_array==v)[0][0] for v in t[:lasti]]
            unsorted_index.sort()
            return input_array[unsorted_index]
        else:
            unsorted_index = [input_array.index(v) for v in t[:lasti]]
            unsorted_index.sort()
            return [input_array[n] for n in unsorted_index]
       
def get_host_name():
    """Get the host name of this computer in a platform-independent manner."""
    fullname = socket.gethostname()
    # Depending on the operating system, fullname might be just the machine name,
    # or might also have the full internet address; and it might be in lower or
    # upper case.  Normalize to be just the machine name, in lower case.
    return fullname.split('.')[0].lower()

def reverse_dictionary(dictionary):
    """Returns a dictionary where values are keys and keys are values of the given 'dictionary'."""
    newdict = {}
    for key, value in dictionary.iteritems():
        newdict[value]=key
    return newdict

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

def create_import_for_camel_case_class(opus_path, import_as=None):
    """Creates statement to import this class.

    opus_path is full Opus path.
    Module name is lower_case_with_underscores.
    Class name is CamelCase version of module name.
    To do import, exec returned statement.
    """
    class_name = opus_path.split('.')[-1]
    class_name = convert_lower_case_with_underscores_into_camel_case(class_name)
    if import_as is not None:
        return 'from %s import %s as %s' % (opus_path, class_name, import_as)
    else:
        return 'from %s import %s' % (opus_path, class_name)

def get_config_from_opus_path(opus_path):
    class_name = opus_path.split('.')[-1]
    class_name = convert_lower_case_with_underscores_into_camel_case(class_name)
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

def does_database_server_exist_for_this_hostname(module_name, hostname, protocol='mysql', log_on_failure=True):
    from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
    from opus_core.database_management.database_server import DatabaseServer

    if not 'MYSQLUSERNAME' in os.environ:
        if log_on_failure:
            logger.log_warning('The tests will not be run for module:\n'
                               '  %s\n'
                               'since the MYSQLUSERNAME environment variable is not defined.'
                               % module_name)
        return False
    user_name = os.environ['%sUSERNAME'%protocol.upper()]

    if not '%sPASSWORD'%protocol.upper() in os.environ:
        if log_on_failure:
            logger.log_warning('The tests will not be run for module:\n'
                               '  %s\n'
                               'since the MYSQLPASSWORD environment variable is not defined.'
                               % module_name)
        return False
    password = os.environ['%sPASSWORD'%protocol.upper()]

    try:
        db_config = DatabaseServerConfiguration(
            host_name = hostname,
            user_name = user_name,
            password = password,
            protocol = protocol
        )
        db_server = DatabaseServer(db_config)
            
    except:
        if log_on_failure:
            logger.log_warning('The tests will not be run for module:\n'
                               '  %s\n'
                               'since we cannot connect to database server on host %s '
                               ' with user %s.'
                               % (module_name, hostname, os.environ['%sUSERNAME'%protocol.upper()]))
        return False
    finally:
        db_server.close()
    return True

def does_test_database_server_exist(module_name, protocol = 'mysql', log_on_failure=True, logger=logger):
    if '%sHOSTNAMEFORTESTS'%(protocol.upper()) in os.environ:
        return True

    if log_on_failure:
        logger.log_warning('The tests will not be run for module:\n'
            '  %s\n'
            'since the %sHOSTNAMEFORTESTS environment variable has\n'
            'not been defined.  See documentation for how to define\n'
            'a connection to a database server for tests.'
                % (module_name,protocol.upper()))

    return False

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

from opus_core.tests import opus_unittest
import shutil
import opus_core

class MiscellaneousTests(opus_unittest.OpusTestCase):
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
        temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        try:
            files = [
                ['CVS', 'f1'],
                ['d1', 'f2'],
                ['d1', 'CVS', 'f3'],
                ['f4'],
                ]
            for t in files:
                path = temp_dir
                for n in t:
                    path = os.path.join(path, n)
                os.makedirs(path)
                self.assert_(os.path.exists(path))
            remove_directories_with_this_name(temp_dir, 'CVS')
            for t in files:
                path = temp_dir
                for n in t:
                    path = os.path.join(path, n)
                if 'CVS' in t:
                    self.assert_(not os.path.exists(path))
                else:
                    self.assert_(os.path.exists(path))
        finally:
            self.assert_(os.path.exists(temp_dir))
            shutil.rmtree(temp_dir)

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
        from numpy import array, ma

        a = array(["max_attribute1", "min_attribute1", "attribute1", "attribute2_max", "attribute2"])
        prefix_list = ["min", "max"]
        result = remove_elements_with_matched_prefix_from_list(a, prefix_list)
        self.assertEqual(ma.allequal(result, array(["attribute1", "attribute2_max", "attribute2"])), True,
                         msg = "Error in test_remove_elements_with_matched_prefix" )

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

    def test_copytree(self):
        temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        dest = os.path.join(temp_dir, 'dest')
        os.mkdir(dest)
        dirs = [
            ['d1', 'd2', 'd3', 'CVS', 'sub'],
            ['d2', 'd3'],
            ['d4', 'CVS', 'd1'],
            ['d5'],
            ['d6', '.svn', 'd1', 'd2'],
            ]
        try:
            for t in dirs:
                path = temp_dir
                for n in t:
                    path = os.path.join(path, n)
                os.makedirs(path)
                source = os.path.join(temp_dir, t[0])
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
        finally:
            shutil.rmtree(temp_dir)

    def test_unique_values(self):
        from numpy import array, ma

        a = array([0.01, 0.1, 0.01, 0.2, 0.1, 0.5, 0.08])
        self.assertEqual(ma.allequal(unique_values(a), array([0.01, 0.08, 0.1, 0.2, 0.5])), True)
        self.assertEqual(ma.allequal(unique_values(a, sort_values=False), array([0.01, 0.1, 0.2, 0.5, 0.08])), True)
        b = [0.01, 0.1, 0.01, 0.2, 0.1, 0.5, 0.08]
        self.assertEqual(unique_values(b), [0.01, 0.08, 0.1, 0.2, 0.5])
        self.assertEqual(unique_values(b, sort_values=False), [0.01, 0.1, 0.2, 0.5, 0.08])

if __name__ == "__main__":
    opus_unittest.main()