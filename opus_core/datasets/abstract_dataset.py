# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import gc
import copy
import os

from numpy import array, where, float32, int32, sort, argsort, reshape, dtype, any, abs
from numpy import zeros, arange, ones, clip, ndarray, concatenate, searchsorted, resize
from numpy import compress, transpose, logical_and, ma, isscalar, asarray
#from scipy import ndimage  ## use opus_core.ndimage instead
from opus_core import ndimage, paths
from numpy.random import randint
from numpy import ma

from opus_core.session_configuration import SessionConfiguration
from opus_core.misc import all_in_list, is_masked_array
from opus_core.strings import create_list_string, indent_text
from opus_core.misc import do_id_mapping_dict_from_array, do_id_mapping_array_from_array
from opus_core.misc import DebugPrinter, corr
from opus_core.variables.variable_factory import VariableFactory
from opus_core.variables.attribute_box import AttributeBox
from opus_core.resources import Resources
from opus_core.specified_coefficients import update_constants
from opus_core.misc import uniquend
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.attribute_type import AttributeType
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from opus_gui.util.exception_formatter import formatPlainTextExceptionInfo

class DataElement(object):
    """Represents one individual of the Dataset object. It is created by the method
    'get_data_element' of the Dataset class.
    """
    pass

class AbstractDataset(object):
    """
    Dataset is defined as a set of individuals of the same dataset that are characterized by a set of attributes.
    One can imagine it as an n x m table where n is the number of individuals and m is the number of attributes.
    Different attributes can be of different type (of scalars). Each attribute has a name.
    A Dataset is characterized by:
        - list of attribute names that serve as a unique identifier of the individuals. Values of unique identifiers
            should be integers > 0.
        - n - number of individuals
        - list of attribute names
        - dataset name which determines the directory in which variables for this dataset are implemented.

    The class provides a method for accessing the data, called 'get_attribute(attribute_name)' which returns
    an array of values of the given attribute.
    The class offers a method 'load_dataset' which reads the data from storage. If this method is not used,
    the data are loaded as they are needed, i.e. when using 'get_attribute'. Note that a method 'load_dataset'
    implemented for the given storage object is required.

    Computed variables for the dataset are treated as attributes. They can be thought as additional columns in
    the n x m table. In order to differentiate them from fixed attributes, each attribute/variable (represented
    by the class AttributeBox) holds one of the metadata
    PRIMARY (fixed attribute), COMPUTED (computed variable).
    """
    hidden_id_name = "_hidden_id_"
    _coordinate_system = None  # Override in child, if needed (used in get_2D_attribute, plot_map, r_image)
                               # It is a tuple of attribute names that contain the (x_coordinate, y_coordinate) 

    def __init__(self, resources=None, id_name=None, dataset_name=None,
            out_storage=None, in_table_name=None, out_table_name=None, debug=None):
        """The argument 'resources' is of type Resources and can contain all other arguments
        (as a pair of argument_name:value). If not None, argument values given directly to the constructor overwrite
        the corresponding values in resources (in a local copy, thus not seen outside).
        'id_name' is a list of strings that determine a unique identifiers of the dataset.
            If 'id_name' is an empty list, there will be a hidden unique identifier created (its name is given
            in the class constant 'hidden_id_name').
        'dataset_name' specifies the directory in which variables for this dataset are implemented.
            It is also used as a directory for caching.
        'out_storage' is a Storage object that is used for dataset output.
        'in_table_name' is name of the table/file that contains the data for this dataset.
        'out_table_name' is name of the table/file for the dataset output.
        'debug' is either of type DebugPrinter or an integer value determining the level of debugging messages.

        id_name has to be given (but can be an empty list), all other arguments are optional.
        """

        self.resources = Resources(resources)
        self.resources.merge_if_not_None({ "id_name":id_name,
                            "dataset_name":dataset_name,
                            "out_storage":out_storage,
                            "in_table_name":in_table_name,
                            "out_table_name":out_table_name,
                            "debug":debug})
        self.resources.merge_with_defaults({"dataset_name":"dataset"})
        self.dataset_name = self.resources.get("dataset_name", None)
        self.attribute_cache = AttributeCache()
        self.attribute_boxes = {}
        self.n = 0
        self.id_mapping=None
        self.id_mapping_type=None
        self.id_mapping_shift=0
        self._primary_attribute_names = []
        self.debug = self.resources.get("debug",  0)
        if not isinstance(self.debug, DebugPrinter):
            self.debug = DebugPrinter(self.debug)
        self.variable_factory = VariableFactory()
        # self._aliases is a dictionary mapping aliases to VariableNames - used just for error checking,
        # to check for duplicate aliases
        self._aliases = {}
        self._id_names = self.resources.get("id_name", None)
        if self._id_names == None:
            self._raise_error(StandardError,
                              "Must specify 'id_name' when creating a dataset.")
        if not isinstance(self._id_names, list):
            self._id_names = [self._id_names]
        self._primary_attribute_names = self.determine_stored_attribute_names(resources=self.resources,
                                                                                attribute_type=AttributeType.PRIMARY)
        self._precached_attribute_names = self.determine_stored_attribute_names(resources=self.resources,
                                                                                attribute_type=AttributeType.COMPUTED)
        if not self._id_names:
            # The size of an id_name attribute determines the size of the dataset (done later). 
            # If there are no id_name attributes, load some attribute to determine size of the dataset.
            if not self._primary_attribute_names:
                self.load_dataset()
            else:
                self.load_dataset(attributes=[self._primary_attribute_names[0]])

    ##################################################################################
    ## Methods for adding columns
    ##################################################################################
    
    def add_primary_attribute(self, data, name):
        """ Add values given in argument 'data' to the dataset as an attribute 'name'. 
        'data' should be an array of the same size as the dataset.
        If this attribute already exists, its values are rewritten.
        The attribute is marked as a primary attribute.
        """
        self._ensure_id_attribute_is_loaded()
        if not isinstance(data, ndarray):
            data=array(data)
        if data.size <> self.size():
            logger.log_warning("In add_attribute: Mismatch in sizes of the argument 'data' and the Dataset object.")
        self.add_attribute(data, name, metadata=AttributeType.PRIMARY)

    def add_attribute(self, data, name, metadata=2):
        """Add values given in argument 'data' to dataset as an attribute 'name' as type 'metadata'. If this
        attribute already exists, its values are overwritten. 
        'metadata' should be of type AttributeType (PRIMARY=1, COMPUTED=2).
        The method increments and returns the version number of the attribute.
        """
        if not (isinstance(data, ndarray) or is_masked_array(data)):
            data=array(data)
        name = self.create_and_check_qualified_variable_name(name)
        short_name = name.get_alias()
        if short_name in self.get_attribute_names():
            self.attribute_boxes[short_name].set_data(data)
            self.attribute_boxes[short_name].set_is_in_memory(True)
            self.attribute_boxes[short_name].set_type(metadata)
        else:
            self.attribute_boxes[short_name] = AttributeBox(self, data=data, variable_name=name,
                                                type=metadata)
        if metadata == AttributeType.PRIMARY:
            self._add_to_primary_attribute_names(short_name)
            
        self.__increment_version(short_name)
        return self.get_version(short_name)

    ##################################################################################
    ## Methods for adding rows
    ##################################################################################
    
    def add_elements(self, data, require_all_attributes=True, change_ids_if_not_unique=False):
        """ Add elements of 'data' to self. 'data' is a dictionary with keys equal attribute names
        and values equal numpy arrays of the attribute values.
        All computed attributes of self that are not contained in data are deleted.
        If require_all_attributes==True 'data' is required to contain
        all self.primary attributes. If require_all_attributes==False and if there is
        an attribute missing in 'data', it is filled with 0's.
        If the joined ids are not unique and 'change_ids_if_not_unique' is True, the ids
        of the new rows are modified to unique ids. Otherwise it raises an exception.
        It returns index of the new elements.
        """
        # Before we append rows, we first need to load the rows that are in the storage.
        attributes = self.get_nonloaded_attribute_names()
        if attributes:
            self.load_dataset(attributes=attributes)

        # Now append to these rows.
        for attrname in self.get_computed_attribute_names():
            if attrname not in data.keys() and attrname not in self.get_id_name():
                self.delete_one_attribute(attrname)
        data_size = data[data.keys()[0]].size
        for attr in self.get_known_attribute_names():
            old_data = self.get_attribute(attr)
            if (not require_all_attributes) and (attr not in data.keys()):#missing attribute
                if old_data.dtype.kind == 'S':
                    new_data = array(data_size*[''])
                else:
                    type = old_data.dtype
                    new_data = zeros((data_size,), dtype=type)
            else:
                new_data = data[attr]
            self.__increment_version(attr)
            self.attribute_boxes[attr].set_data(concatenate((old_data, new_data)))
        # check if ids are unique
        ids = self.get_id_attribute()
        unique_ids = uniquend(ids)
        if unique_ids.size <> ids.size:
            #change ids to be unique
            if change_ids_if_not_unique:

                if ids.ndim == 1:
                    if self.size() == 0:
                        maxid = 0
                    else:
                        maxid = ids[0:self.size()].max()
                    self.modify_attribute(self.get_id_name()[0], arange(maxid+1, maxid+data_size+1),
                                           arange(self.size(), self.size()+data_size))
                else:
                    maxids = []
                    i=0
                    for id_name in self.get_id_name():
                        if self.size() == 0:
                            maxids.append(0)
                        else:
                            maxids.append(ids[0:self.size(),i].max())
                        i+=1
                    i=0
                    for id_name in self.get_id_name():
                        self.modify_attribute(self.get_id_name()[i], arange(maxids[i]+1, maxids[i]+data_size+1),
                                           arange(self.size(), self.size()+data_size))
                        i+=1
            else:
                self._raise_error(StandardError,
                              "Attribute '%s'  is not unique in the resulting dataset!"
                              % create_list_string(self.get_id_name(), ","))
        self._update_id_mapping()
        self.update_size()
        return arange(self.size()-data_size, self.size())

    def duplicate_rows(self, index):
        """Duplicates rows given by index."""
        attrs = self.get_known_attribute_names()
        data = {}
        for attr in attrs:
            data[attr] = self.get_attribute_by_index(attr, index)
        return self.add_elements(data=data, change_ids_if_not_unique=True)
        
    ##################################################################################
    ## Methods for obtaining columns
    ##################################################################################
    
    def get_attribute(self, name): 
        """ Must be defined in a child class. It should return a 1D array of the same size as dataset.
        """
        raise NotImplementedError('get_attribute')
    
    def get_attribute_as_column(self, name):
        """ Return values of the attribute 'name' as a column vector (i.e. a table of n rows and 1 column) 
        """
        value = self.get_attribute(name)
        return reshape(value, (self.n, 1))
    
    def get_attribute_by_id(self, name, id):
        """ Return values of the given attribute (arg. 'name') that correspond
        to the given identifier 'id'. 'id' can be a single number, a list or an array.
        """
        index = self.get_id_index(id)
        return self.get_attribute_by_index(name, index)

    def get_attribute_by_index(self, name, index):
        """ Return values of the given attribute (arg. 'name') that correspond
        to the given index. 'index' must be an array. It can be also a boolean array.
        """
        return self.get_attribute(name)[index]

    def get_id_attribute(self):
        """ Return values of the primary key (unique identifier). If there is one primary key,
        the result is a 1D array. Otherwise it is a 2D array n x m, where n is the dataset size and
        m is the number of unique identifiers. The ordering of the columns corresponds to 
        the output of self.get_id_name().
        """
        if not self.get_id_name():
            self._create_hidden_id()
        return self.get_multiple_attributes(self.get_id_name())
    
    def get_multiple_attributes(self, names):
        """Return a 2D array of (dataset size x number of attributes). names must be a list or array of attribute names."""
        lnames = len(names)
        if lnames <= 0:
            return array([])
        result = self.get_attribute(names[0])
        if lnames == 1:
            return result
        array_size = result.size
        result = reshape(result, (array_size,1))
        for name in names[1:]:
            result=concatenate((result, reshape(self.get_attribute(name), (array_size,1))),
                                     axis=1)
        return result
        
    def get_2d_attribute(self, attribute=None, attribute_data=None, coordinate_system=None):
        """Returns an 2d array of the attribute given. If no attribute is given, attribute_data must be provided.
        If coordinate_system is None, dataset must have self._coordinate_system defined. It is a tuple of 2 attribute names, 
        that define the x and y axis, respectively.
        """
        if coordinate_system is None:
            self._check_2d_coordinates()
            x_attribute_name, y_attribute_name = self.get_coordinate_system()
        else:
            x_attribute_name, y_attribute_name = coordinate_system

        x = self.get_attribute(x_attribute_name).astype('int32')
        y = self.get_attribute(y_attribute_name).astype('int32')
        maxx = int(ma.maximum.reduce(x))
        maxy = int(ma.maximum.reduce(y))
        if attribute is not None:
            attribute_data = self.get_attribute(attribute)
        type = attribute_data.dtype.type
#        if type == dtype('b1'):
#            attribute_data = attribute_data.astype('int32')
#            type = attribute_data.dtype.type
            
        minz = ma.minimum(attribute_data)
        minx = int(ma.minimum.reduce(x))
        miny = int(ma.minimum.reduce(y))
        difx = maxx-minx
        dify = maxy-miny
        
        cell_size = (difx+1) * (dify+1)
        if cell_size > 10000000:
            logger.log_warning('The size of the 2d array is extraodinarily large (%i). You may run out of memory')
            
        two_d_array = resize(array([minz-1], dtype=type), (difx+1, dify+1))
        # fill the array with the proper values
        two_d_array[x-minx, y-miny] = ma.filled(attribute_data,minz-1)[:]
        return ma.masked_where(two_d_array < minz, two_d_array)
    
    ##################################################################################
    ## Methods for obtaining rows
    ##################################################################################
    
    def get_data_element(self, index, all_attributes=False):
        """Return an object of class DataElement of the given index. If 'all_attributes' is False,
        only attributes that are already loaded are included. Otherwise all primary
        attributes are loaded from storage. 'index' is an integer number.
        """
        object = DataElement()
        if all_attributes:
            self.load_dataset_if_not_loaded()
        for col in self.get_attribute_names():
            setattr(object, col, self.get_attribute_by_index(col,index))
        return object

    def get_data_element_by_id(self, id, all_attributes=False):
        """Return an object of class DataElement of the given identifier id. See get_data_element."""
        self._ensure_id_attribute_is_loaded()
        return self.get_data_element(self._get_one_id_index(id), all_attributes)
    
    ##################################################################################
    ## Methods for modifying columns
    ##################################################################################
    
    def modify_attribute(self, name, data, index=None):
        """ Synonym for set_values_of_one_attribute"""
        self.set_values_of_one_attribute(attribute=name, values=data, index=index)

    def set_values_of_one_attribute(self, attribute, values, index=None):
        """Replace values of the given attribute and of the given index by a copy of values
        given in the array 'values' and increment the version number. 'values' and 'index'
        should be numpy arrays.
        """
        if not isinstance(attribute, VariableName):
            attr_name = VariableName(attribute)
        else:
            attr_name = attribute
        short_name = attr_name.get_alias()
        if short_name not in self.get_attribute_names() or not self.attribute_boxes[short_name].is_in_memory(): # lazy loading
            self.get_attribute(attr_name)
        if isinstance(index, list):
            index = array(index)
        self.attribute_boxes[short_name].set_data(array(values),index)
        self.__increment_version(short_name)

    def set_value_of_attribute_by_id(self, attribute, value, id):
        """Replace a value of the given attribute that correspond to the given identifier 'id'
        by the given 'value'. 'value' and 'id' are scalars.
        """
        self.set_values_of_one_attribute(attribute,value,self.id_mapping[id])
        
    def touch_attribute(self, name):
        """Pretends that the attribute was changed (It increments its version number)."""
        self.__increment_version(name)
        
    ##################################################################################
    ## Methods for deleting columns
    ##################################################################################     
        
    def delete_one_attribute(self, name):
        """ Deletes data of attribute 'name' (incl. metadata)
        """
        if not isinstance(name, VariableName):
            name = VariableName(name)
        alias = name.get_alias()
        if alias in self._aliases:
            del self._aliases[alias]
        if alias in self.attribute_boxes.keys():
            del self.attribute_boxes[alias]
        self.remove_from_primary_attribute_names(alias)

    def delete_computed_attributes(self):
        """ Deletes all computed attributes, incl. metadata.
        """
        for attr in self.get_computed_attribute_names():
            if not attr in self.get_id_name():
                self.delete_one_attribute(attr)
            
    ##################################################################################
    ## Methods for deleting rows
    ##################################################################################
    
    def remove_elements(self, index):
        """Remove individuals from Dataset, given by 'index'. In order to avoid problems with
        lazy loading, all attributes are loaded."""
        if index == None or index.size == 0:
            return
        attributes = self.get_nonloaded_attribute_names()
        if attributes:
            self.load_dataset(attributes=attributes)
        index_array = ones((self.size(),), dtype="int32")
        index_array[index] = 0
        keep_index = where(index_array)[0]
        for attr in self.get_attribute_names():
            if not self.attribute_boxes[attr].is_in_memory():
                self.get_attribute(attr)
            data = self.attribute_boxes[attr].get_data()
            self.attribute_boxes[attr].set_data(data[keep_index])
            self.__increment_version(attr)
        self.update_size()
        self._update_id_mapping()

    def subset(self, n, is_random=False):
        """The method shrinks the size of the dataset to 'n'.
        If the argument 'is_random' == False, the first 'n' entries are taken. Otherwise
        the data entries are chosen randomly.
        """
        if n < self.size():
            if not is_random: # not randomly
                index = arange(n)
            else:      # choose entries randomly
                index = randint(0,self.size(), size=n)
            self.subset_by_index(index)

    def subset_by_index(self, index, flush_attributes_if_not_loaded=True):
        """Shrink the dataset to values given by 'index'. The removed data are then lost.
        'index' must be an array. If flush_attributes_if_not_loaded is True,
        all attributes that were not in memory are flushed to disk after resizing.
        """
        for varname in self.get_known_attribute_names():
            if varname in self.get_attribute_names() and \
                self.attribute_boxes[varname].is_in_memory():
                    self.attribute_boxes[varname].set_data(self.attribute_boxes[varname].get_data(index))
            else:
                self.get_attribute(varname)
                self.attribute_boxes[varname].set_data(self.attribute_boxes[varname].get_data(index))
                if flush_attributes_if_not_loaded:
                    self.flush_attribute(varname)
        self.n = len(self.get_attribute(self.get_attribute_names()[0]))
        self._update_id_mapping()
        
    def subset_by_ids(self, ids, **kwargs):
        """Determines index of elements given by the array 'ids' and calls 'subset_by_index'.
        """
        index = self.get_id_index(ids)
        self.subset_by_index(index, **kwargs)
        
    def subset_where_variable_larger_than_threshold(self, attribute, threshold=0, **kwargs):
        """Removes entries from the dataset for which value of the given attribute is smaller or equal
           to the given threshold.
        """
        index = self.get_index_where_variable_larger_than_threshold(attribute, threshold)[0]
        self.subset_by_index(index, **kwargs)

    ##################################################################################
    ## Methods for obtaining column names
    ##################################################################################
    
    def get_attribute_names(self):
        """Return a list of attribute names (including computed variables) that have been
        loaded or computed, regardless of whether they are currently in memory.
        Primary attributes that have not been used (and thus, are not loaded) will 
        not be included in the result. (see also get_known_attribute_names())
        """
        return self.attribute_boxes.keys()

    def get_known_attribute_names(self):
        """Return attribute names that are either primary or were computed (i.e. all attributes that the dataset 'knows' about)."""
        nda = self.get_primary_attribute_names()
        return nda + [attribute for attribute in self.get_attribute_names() if attribute not in nda]
    
    def get_attribute_long_names(self):
        """ Like get_attribute_names, but the attribute names are in their long format.
        """
        return map(lambda key: self.attribute_boxes[key].get_full_name(), self.attribute_boxes.keys())

    def get_attributes_in_memory(self):
        """Return a list of attributes that are currently in memory"""
        return [attribute for attribute in self.get_attribute_names() if self.attribute_boxes[attribute].is_in_memory()]

    def get_primary_attribute_names(self):
        """Return a list of attribute names whose values are accessible on the storage.
        """
#        return [key for key in self.attribute_boxes.keys() if self.attribute_boxes[key].get_type() == AttributeType.PRIMARY]
        return self._primary_attribute_names

    def get_non_id_primary_attribute_names(self):
        """Return a list of primary attribute names that are not unique identifiers."""
        names = copy.copy([attr for attr in self.get_primary_attribute_names() if attr not in self.get_id_name()])
        return names
    
    def get_computed_attribute_names(self):
        """ Return names of all computed attributes.
        """
        return [key for key in self.attribute_boxes.keys() if self._get_attribute_type(key) == AttributeType.COMPUTED]

    def get_cached_attribute_names(self):
        """ Return names of all cached computed attributes.
        """
        return set(self._precached_attribute_names + [key for key in self.attribute_boxes.keys() if self.attribute_boxes[key].is_cached()])

    def get_stored_attribute_names(self):
        """ Returns names of all attributes on storage, whether loaded or not.
        """
        return set(self.get_primary_attribute_names()) | set(self.get_cached_attribute_names())
    
    def get_nonloaded_attribute_names(self):
        """Return primary attribute names that are not loaded.
        """
        return [attr for attr in self.get_primary_attribute_names() if attr not in self.get_attribute_names()]
    
    def get_id_name(self):
        """Return a list of attribute names that specify the unique identifier of this dataset.
        """
        return self._id_names

    def get_non_hidden_id_name(self):
        """Return a list of attribute names that specify the unique identifier of this dataset.
        Do not return the special hidden id.
        """
        if self._id_names == [self.hidden_id_name]:
            return []
        
        return self._id_names
    
    ##################################################################################
    ## Methods handling I/O
    ##################################################################################
    
    def load_dataset(self, resources=None, nchunks=None, attributes=None, in_storage=None,
                     in_table_name=None, lowercase=None, load_id_with_each_chunk=None,
                     flush_after_each_chunk=None):
        """ Should be implemented in the child class. """
        raise NotImplementedError('load_dataset')

    def load_dataset_if_not_loaded(self, resources=None, nchunks=None, attributes=None,
                            in_storage=None, in_table_name=None, lowercase=None):
        """ Should be implemented in the child class. """
        raise NotImplementedError('load_dataset_if_not_loaded')
    
    def write_dataset(self, resources = None, attributes=None, out_storage=None,
                       out_table_name=None, valuetypes=None):
        """ Should be implemented in the child class. """
        raise NotImplementedError('write_dataset')

    def flush_attribute(self, name):
        """ Write into cache and remove from memory the attribute given by name and perform garbage collection.
        The dataset keeps the metadata.
        """
        self._do_flush_attribute(name)
        gc.collect()

    def flush_dataset(self):
        """ Write all attributes that are in memory into cache and perform garbage collection.
        """
        logger.log_status("Flushing %s" % self.get_dataset_name())
        for attribute_name in self.get_attributes_in_memory():
            if not(attribute_name in self.get_id_name() and self._is_hidden_id()):
                self._do_flush_attribute(attribute_name)
        gc.collect()

    def load_and_flush_dataset(self):
        """ Use to put all of the datasets attributes into the cache, including unloaded attributes.
        """
        nonloaded_attribute_names = self.get_nonloaded_attribute_names()
        # flush all attributes that are in memory
        self.flush_dataset()
        # flush all attributes that were not in memory
        for attr in nonloaded_attribute_names:
            self.get_attribute(attr)
            self.flush_attribute(attr)

    def flush_dataset_if_low_memory_mode(self):
        """ Call flush_dataset() only if the simulation runs in low memory mode.
        """
        if SimulationState().get_low_memory_run():
            self.flush_dataset()
            
    def get_cache_directory(self):
        """ Return the name of the cache directory (used for flushing dataset) 
        """
        return self.attribute_cache.get_storage_location()

    def remove_cache_directory(self):
        """ Remove the cache directory."""
        self.attribute_cache.simulation_state.remove_base_cache_directory()
        
    ##################################################################################
    ## Methods for computing variables
    ##################################################################################
    
    def compute_variables(self, names, dataset_pool=None, resources=None, quiet=False):
        """Compute variables defined by the expressions in the list/tuple 'names'. 'quiet' turns
        some warnings on and off.  If it is None, it is taken from self.resources.
        The available datasets are those in dataset_pool.
        """
        (versions, value) = self.compute_variables_return_versions_and_final_value(names, dataset_pool, resources, quiet)
        return value

    def compute_variables_return_versions_and_final_value(self, names, dataset_pool=None, resources=None, quiet=False):
        """Compute variables defined by the expressions in the list/tuple 'names'.  Return a pair
        (new_versions, value) where new_versions is a list of version numbers.
        """
        if isinstance(names, ndarray):
            names = names.tolist()
        if (not isinstance(names, list)) and (not isinstance(names, tuple)):
            names=[names]
        if not names:
            raise ValueError, "No variable given to the compute method."
        new_versions = []
        for ivar in range(len(names)):
            if isinstance(names[ivar], tuple):
                qualified_name, version = names[ivar]
            else:
                name = names[ivar]
                qualified_name = self.create_and_check_qualified_variable_name(name)
                if qualified_name.get_alias() in self.get_attribute_names():
                    version = self.get_version(qualified_name.get_alias())
                else:
                    version = None
            new_versions.append(
                self._compute_if_needed(qualified_name,
                                       dataset_pool,
                                       resources=resources, quiet=quiet, version=version))
        # return the new versions, and the value of the last variable in the list
        return (new_versions, self.get_attribute(qualified_name))
    
    def compute_one_variable_with_unknown_package(self, variable_name, dataset_pool=None, package_order=None):
        """ Compute one variable where the package is unknown. It iterates over packages either in package_order
            (which should be a list or None),
            or (if package_order is None) over packages in dataset_pool._package_order.
            'variable_name' must be an unqualified attribute name. The method extends it by 
            a package name and the dataset name of self.
        """
        if (package_order is None) and (dataset_pool is None):
            self._raise_error(ValueError,
                              "Either package_order or dataset_pool must be not None.")
        if package_order is None:
            package_order = dataset_pool.get_package_order()
            
        result = None
        errors = []
        def _format_error(full_variable_name):
            return formatPlainTextExceptionInfo("When trying to compute variable '%s':"  
                                                % full_variable_name)
            
        if len(package_order) == 0:
            full_variable_name = "%s.%s" % (self.get_dataset_name(), variable_name)
            try:
                result = self.compute_variables([full_variable_name], dataset_pool=dataset_pool)
            except:
                errors += [_format_error(full_variable_name)]
        for package in package_order:
            full_variable_name = "%s.%s.%s" % (package, self.get_dataset_name(), variable_name)
            try:
                result = self.compute_variables([full_variable_name], dataset_pool=dataset_pool)
                break
            except:
                errors += [_format_error(full_variable_name)]
        if result is None:
            errors = indent_text(''.join(errors))
            desc = create_list_string(("Computing variable '%s' in dataset pool '%s' failed for packages: '%s'."
                                       % (variable_name, dataset_pool, "', '".join(package_order)),
                                       errors))
            self._raise_error(StandardError, desc)
        return result
    
    ##################################################################################
    ## Methods for obtaining indices
    ##################################################################################
    
    def get_id_index(self, id):
        """Return an array of indices that correspond to the given id numbers.
        'id' is either a number, list or an array. It throws an exception if any of the
        id numbers are not found in the dataset. (See also try_get_id_index())
        """
        self._ensure_id_attribute_is_loaded() # Must have the id attributes loaded for the id_mapping to find them.

        if isscalar(id) or isinstance(id, tuple):
            return self._get_one_id_index(id)

        ids = id
        if not isinstance(ids, ndarray):
            ids = array(ids, dtype="int32")
        if ids.dtype.name.startswith('float'):
            ids = ids.astype('int32')
        if ids.ndim > 1:
            return array(map(lambda x: self.id_mapping[tuple(x)], ids), dtype=ids.dtype.char)
        if self.id_mapping_type == "A":
            isnegative = ids < 0
            if isnegative.sum() > 0:
                raise KeyError, "No negative ids allowed in dataset."
            result = self.id_mapping[ids - self.id_mapping_shift]
            if any(result < 0):
                raise KeyError, "Some ids not found in dataset %s." % self.get_dataset_name()
        else:
            result = array(map(lambda x: self.id_mapping[x], ids), dtype=ids.dtype.char)
        return result

    def try_get_id_index(self, id, return_value_if_not_found=-1):
        """Like get_id_index() but replaces indices for not existing id numbers by a value
        given in the argument 'return_value_if_not_found'.
        """
        ids = id
        if not isinstance(ids, ndarray):
            ids = array(ids)
        ids = ids.astype(int32)
        self._ensure_id_attribute_is_loaded() # Must have the id attributes loaded for the id_mapping to find them.
        if ids.ndim > 1:
            return array(map(lambda x: self.try_id_mapping(tuple(x), return_value_if_not_found), ids))
        try: # it might be faster if all values are found
            if any(ids <= 0): # do not consider negative or zero ids
                result = resize(array([return_value_if_not_found], dtype="int32"), ids.size)
                idx = where(ids > 0)[0]
                result[idx] = self.get_id_index(ids[idx])
                return result
            return self.get_id_index(ids)
        except:
            return array(map(lambda x: self.try_id_mapping(x, return_value_if_not_found), ids))

    def get_index_where_variable_larger_than_threshold(self, attribute, threshold=0):
        """Return index of entries for which value of the given attribute is larger than
           the given threshold.
        """
        return where(self.get_attribute(attribute) > threshold)
    
    def get_filtered_index(self, filter, threshold=0, index=None, dataset_pool=None, resources=None):
        """Return only those indices of index that pass through the given filter. Filter can be an expression/variable,
        it is computed within this method."""
        self.compute_variables([filter], dataset_pool=dataset_pool, resources=resources)
        name = VariableName(filter)
        filtered_index = self.get_index_where_variable_larger_than_threshold(
                name.get_short_name(), threshold=threshold)
        new_index = zeros((self.size(),), dtype=int32)
        if index == None:
            index = arange(self.size())
        if not isinstance(index,ndarray):
            index=array(index)
        new_index[index]=1
        new_index_tmp = zeros((self.size(),), dtype=int32)
        new_index_tmp[filtered_index]=1
        new_index = logical_and(new_index, new_index_tmp)
        return where(new_index)[0]
    
    ##################################################################################
    ## Methods for joining two datasets
    ##################################################################################
    
    def connect_datasets(self, dataset):
        """ Add attributes of 'dataset' to self. self and 'dataset' must have the same
        id_name and the same values of the unique identifier.
        """
        if self.get_id_name() <> dataset.get_id_name():
            self._raise_error(StandardError,
                              "Mismatch in id names of datasets('%' for this dataset versus '%' dataset passed into connect_datasets())."
                              % (self.get_id_name(), dataset.get_id_name()))
        ids = self.get_id_attribute()
        ds_ids = dataset.get_id_attribute()
        idx = dataset.get_id_index(ids)
        for attr in dataset.get_attribute_names():
            if attr not in self.get_attribute_names():
                self.add_attribute(data=dataset.get_attribute_by_index(attr, idx),
                                   name=dataset.attribute_boxes[attr].get_full_name(),
                                   metadata=AttributeType.PRIMARY) #T: why is this automatically set to be a primary attribute?
                attribute_box = self._get_attribute_box(attr)
                attribute_box.set_variable_instance(dataset.attribute_boxes[attr].get_variable_instance())

    def join(self, dataset, name, join_attribute=None, new_name=None, metadata=AttributeType.COMPUTED, **kwargs):
        """Call get_join_data() and add the resulting array
        to self.attribute_boxes as an additional attribute(s). 'new_name'
        specifies the name(s) of the new created attribute. If it is None, 'name' is used.
        'name' and 'new_name' can be either a character string or a list of char strings, if join is performed
        on mutiple attributes.
        **kwargs are passed to get_join_data().
        """

        if not isinstance(name, list):
            name = [name]

        if new_name is None:
            new_name=name
        if not isinstance(new_name, list):
            new_name = [new_name]

        data = self.get_join_data(dataset, name, join_attribute, **kwargs)
        for iattr in range(len(name)):
            if not isinstance(data, dict):
                tmpdata = data
            else:
                tmpdata = data[name[iattr]]
            self.add_attribute(data=tmpdata, name=new_name[iattr], metadata=metadata)

    def get_join_data(self, dataset, name, join_attribute=None, return_value_if_not_found=None,
                      filled_value=None ):
        """Does a join on a attribute of two datasets (self and 'dataset').
        'join_attribute' specifies the join attribute of self. If this is None it is
        assumed to be identical to dataset._id_names which is the join attribute of 'dataset'.
        The method returns values of the attribute 'name' (which is an attribute of 'dataset')
        for the joined ids, i.e. the resulting array should have the same size as self.
        If 'name' is a list, the method returns a dictionary with one attribute per item in 'name'.
        For values of 'join_attribute' not found in dataset constant given by
        'return_value_if_not_found' are used. 'filled_value' specifies a constant to be used
        for masked values of the dataset attribute 'name'.
        
        if return_value_if_not_found and filled_value is None, a default value according to the 
        dtype.kind ('biufcSUV') of the named attributed is applied:
           boolean (b): False; string (S): ''; Unicode (U): ''; integer (i): -1;
           unsigned (u): 0; float (f): -1.0; and undefined for complex (c) and Void (V)
        """
        
        default_return_values_by_type = default_filled_values_by_type = {'S':'',
                                                                         'U':'',
                                                                         'b':False,
                                                                         'i':-1,
                                                                         'u':0,
                                                                         'f':-1.0}
        
        id_name = dataset.get_id_name()
        jattr = join_attribute
        if jattr == None:
            jattr = id_name
        if not isinstance(jattr, list):
            jattr = [jattr]
        if not isinstance(name, list):
            name = [name]
        ID_NOT_FOUND = -1
        #T: won't the following only work if the join_attribute is an id col?
        idx = dataset.try_get_id_index(self.get_multiple_attributes(jattr).astype(int32), ID_NOT_FOUND)
        idx_found = idx <> ID_NOT_FOUND
        lname = len(name)
        for iattr in range(lname):
            attr_values = dataset.get_attribute_by_index(name[iattr], idx[idx_found])
            if idx_found.sum() == idx_found.size: # no missing value
                values = attr_values
            else:
                k = attr_values.dtype.kind
                if return_value_if_not_found is None and default_return_values_by_type.has_key(k):
                    values = array([ default_return_values_by_type[k] ], dtype=attr_values.dtype).repeat(self.size())
                else:
                    values = array([return_value_if_not_found], dtype=attr_values.dtype).repeat(self.size())
                
                if filled_value is None and default_filled_values_by_type.has_key(k):
                    values[idx_found] = ma.filled(attr_values, default_filled_values_by_type[k])
                else:
                    values[idx_found] = ma.filled(attr_values, filled_value)
            if lname > 1:
                if iattr == 0:
                    result = {}
                result[name[iattr]] = values
            else:
                result = values
        return result

    def join_by_rows(self, dataset, require_all_attributes=True, change_ids_if_not_unique=False):
        """Add elements of dataset to the elements of self.
        Only joins primary attributes.
        All computed attributes will be deleted.
        Will load both datasets before doing join.
        """
        self.load_dataset_if_not_loaded()
        dataset.load_dataset_if_not_loaded()
        data = {}
        for attrname in dataset.get_primary_attribute_names():
            data[attrname] = dataset.get_attribute(attrname)
        return self.add_elements(data, require_all_attributes, change_ids_if_not_unique)
    
    def aggregate_dataset_over_ids(self, dataset, function='sum', attribute_name=None, constant=None):
        """Aggregate atttribute (given by 'attribute_name') of the given 'dataset' over
        self by applying the given function. The dataset is expected to have an attribute of the same
        name as the unique identifier of self. If attribute_name is not given, the
        argument 'constant' must be given, which is either a scalar or a numpy array. if it
        is a scalar, for each individual to be counted the constant value is taken into the function;
        if it is a numpy array of the same size as dataset, the value in the same index as
        individual is counted into the function.
        The function can be one of ['sum', 'mean', 'variance', 'standard_deviation', 'minimum',
                                     'maximum', 'center_of_mass']
                                     (functions supported by scipy.ndimage)
        """
        dataset_id_values = dataset.get_attribute(self._id_names[0]).astype(int32)
        used = where(dataset_id_values > 0)[0] # only individuals that have assigned ids
        if attribute_name == None:
            if constant == None:
                self._raise_error(StandardError,
                                  "Either 'attribute_name' or 'constant' must be given.")
            elif isinstance(constant, ndarray):
                if constant.size <> dataset_id_values.size:
                    self._raise_error(StandardError,
                                      "constant's size (%d) must be of the same as dataset's size (%d)"
                                      % (constant.size, dataset_id_values.size))
                values = constant[used]
            else:
                values = resize(array([constant]), used.size)
        else:
            values = dataset.get_attribute(attribute_name)[used]
        return self.aggregate_over_ids(dataset_id_values[used], values, function)

    def sum_dataset_over_ids(self, dataset, attribute_name=None, constant=None):
        """ Synonym for aggregate_dataset_over_ids called with the function 'sum'.
        """
        return self.aggregate_dataset_over_ids(dataset, "sum", attribute_name, constant)

    def aggregate_over_ids(self, ids, what, function):
        """Applies given function to 'what' over the corresponding individuals grouped according to 'ids',
            i.e. what[i] belongs to individual with ID ids[i]. If an ids[i] is not found in self,
            the corresponding what[i] is not considered.
            'what' and 'ids' are 1D arrays.
           The function can be one of ['sum', 'mean', 'variance', 'standard_deviation', 'minimum',
                                     'maximum', 'center_of_mass']
                                     (functions supported by scipy.ndimage)
        """
        myids = self.get_id_attribute()
        if is_masked_array(what):
            ids_local = ids.copy()
            w = where(ma.getmask(what))
            if len(w)>0:
                where_masked = w[0]
                ids_local[where_masked] = 0 # do not consider those elements in the computation
            filled_what = ma.filled(what, 0)
        else:
            filled_what = what
            ids_local = ids
        try:
            # Work around  numpy/scipy bug -- need to fix the char and num attributes of arrays with dtype==int32
            # formerly: values = eval("ndimage."+function+"(filled_what, labels=ids, index=myids)")
            # f is the function from ndimage
            # f = getattr(ndimage, function)
            f = getattr(ndimage, function)
            values = f(*[filled_what], **{'labels': ids_local, 'index': myids})
            if isscalar(values):
                values = [values]
            result = asarray(values)
        except:
            logger.log_error( "Unknown function or error occured evaluating " + function + ".\n" )
            raise
        return result

    def sum_over_ids(self, ids, what):
        """ Synonym for aggregate_over_ids called with the function "sum".
        """
        return self.aggregate_over_ids(ids, what, "sum")

    ##################################################################################
    ## Methods for data analysis
    ##################################################################################
    
    def attribute_sum(self, name):
        """Return the sum of values of the attribute 'name'.
        """
        values = self.get_attribute(name)
        if isinstance(values,ndarray):
            return values.sum()
        return sum(values)

    def attribute_average(self, name):
        """Return the value of the given attribute averaged over the dataset.
        """
        return self.attribute_sum(name)/self.size()

    def summary(self, names=[], resources=None, output=logger, unload_after_each_attribute=False, index=None):
        """Print a summary of the attributes given in the list 'names' to 'output'.
        'output' should be a file or file-like object; the default is the logger.
        If names is an empty list, display summary for all primary attributes
        plus all computed attributes.
        If unload_after_each_attribute is True, each attributes that is not in memory and is not computed
        will be unloaded from memory right after its processing.
        If index is given, the summary is computed only on the records given by index.
        """
        attr_in_memory = self.get_attributes_in_memory()
        if not names:
            names = self.get_known_attribute_names()
        output.write("%25s\t%8s\t%8s\t%9s\t%7s\t%7s\n" %("Attribute name", "mean", "sd", "sum", "min", "max"))
        output.write("%94s\n" % (94*("-")))
        if (not isinstance(names, list)) and (not isinstance(names, tuple)):
            names = [names]
        if index is None:
            index = arange(self.size())
        for item in names:
            if isinstance(item, VariableName):
                item_name = item
                item = item_name.get_expression()
            else:
                item_name = VariableName(item)
            short_name = item_name.get_alias()
            if short_name not in self.get_id_name():
                computed = False
                if not (short_name in self.get_attribute_names()):
                    if short_name in self._primary_attribute_names:
                        self.load_dataset(attributes=[short_name])
                    else:
                        self.compute_variables([item], resources=resources)
                        computed = True
                if self.get_data_type(item).char <> 'S':
                    s = self.attribute_sum(short_name)
                    values = self.get_attribute(short_name)[index]
                    if self.size()==0:
                        output.write("%25s\n" % short_name)
                    else:
                        output.write("%25s\t%8s\t%8s\t%9g\t%7g\t%7g\n" %(short_name, round(values.mean(),2), round(ndimage.standard_deviation(values),2),
                                                                           s, values.min(), values.max()))
                if unload_after_each_attribute and (not computed) and (short_name not in attr_in_memory):
                    self.unload_one_attribute(short_name)
                    
        output.write("\nSize: %d records\n" % index.size)
        if index.size>0:
            output.write("identifiers:\n")
            for idname in self.get_id_name():
                output.write("\t%s in range %d-%d\n" % (idname, self.get_attribute(idname)[index].min(), 
                                                        self.get_attribute(idname)[index].max()))
    
    def aggregate_all(self, function='sum', attribute_name=None):
        """Aggregate atttribute (given by 'attribute_name') by applying the given function. 'attribute_name' must be given."""
        what = self.get_attribute(attribute_name)
        if is_masked_array(what):
            filled_what = ma.filled(what, 0)
        else:
            filled_what = what
        try:
            sum_value = eval("ndimage."+function+"(filled_what, labels=ones(self.size(), dtype='int16'), index=[1])")
            if isscalar(sum_value):
                sum_value = [sum_value]
            result = asarray(sum_value)
        except:
            logger.log_error( "Unknown function or error occured evaluating " + function + ".\n" )
            raise
        return result

    def categorize(self, attribute_name, bins):
        """ Return an array of membership of values of the specified attribute in the given bins. (See also docs to 
        the numpy function 'searchsorted'.)
        """
        values = self.get_attribute(attribute_name)
        return searchsorted(bins, values)
    
    def correlation_matrix(self, names, index=None):
        #This method does not work.
        """Computes a correlation matrix for attributes given by the list 'names'."""
        if not names:
            return None
        v = self.get_attribute(names[0])
        if index is None:
            index = arange(self.size())
        v = v[index].ravel() # ravel for the case if data are 2d
        evalstr = "corr(v"
        for i in range(1,len(names)):
            name = names[i]
            evalstr= evalstr + ", self.get_attribute('%s')[index].ravel()" % name 
        evalstr=evalstr+")"
        return eval(evalstr)

    def correlation_coefficient(self, name1, name2, index=None):
        """Computes correlation coefficient between 2 attributes given by name1 and name2."""
        R = self.correlation_matrix([name1,name2], index=index)
        return R[0,1]
    
    def get_data_type(self, attribute, default_type=None):
        """Return dtype of the attribute. If the attribute is not found, return default_type.
        """
        if attribute in self.get_known_attribute_names():
            return self.get_attribute(attribute).dtype
        return dtype(default_type)
    
    def size(self):
        """Return size of the dataset."""
        self._ensure_id_attribute_is_loaded()
        return self.n

    ##################################################################################
    ## Memory management
    ##################################################################################
    
    def itemsize_in_memory(self):
        """Get number of bytes of attributes that are in memory."""
        result = 0
        n = self.size()
        for attr in self.get_attributes_in_memory():
            result += n*self.get_attribute(attr).dtype.itemsize
        return result
    
    def unload_computed_attributes(self):
        """ Removes data of all computed attributes from memory, but keeps
        the metadata.
        """
        names = self.get_computed_attribute_names()
        self.unload_attributes(names)

    def unload_primary_attributes(self):
        """ Removes data of all primary attributes from memory, but keeps
        the metadata.
        """
        names = self.get_primary_attribute_names()
        self.unload_attributes(names)

    def unload_attributes(self, names):
        """ Removes data of attributes given in 'names' from memory, but keeps
        the metadata.
        """
        if (not isinstance(names, list)) and (not isinstance(names, tuple)):
            names = [names]
        for name in names:
            self.unload_one_attribute(name)

    def unload_all_attributes(self):
        """ Removes data of all loaded attributes from memory, but keeps
        the metadata.
        """
        self.unload_attributes(self.get_attribute_names())

    def unload_one_attribute(self, name):
        """ Removes data of attribute 'name' from memory, but keeps
        the metadata.
        """
        if name in self.get_attribute_names():
            self.attribute_boxes[name].set_data(None)
            self.attribute_boxes[name].set_is_in_memory(False)

    def unload_not_used_attributes(self, used_attributes):
        """Unload all loaded attributes that are not in the 'used_attributes' list.
        """
        for attr in self.get_attribute_names():
            if attr not in used_attributes:
                self.unload_one_attribute(attr)

    ##################################################################################
    ## Plotting methods
    ##################################################################################
    
    def plot_histogram(self, name, index=None, main="", filled_value=0.0, bins=None):
        """Plot a histogram of an attribute values given be name.
        If the attribute is a mask array, the masked values will be filled with 
        'filled_value'. Number of bins can be given by 'bins'.
        """
        from opus_core.plot_functions import plot_histogram
        if index is not None:
            values = ma.filled(self.get_attribute_by_index(name, index), filled_value)
        else:
            values = ma.filled(self.get_attribute(name), filled_value)
        plot_histogram(values, main=main, xlabel=name, bins=bins)

    def compute_and_plot_histogram(self, name, dataset_pool=None, **kwargs):
        self.compute_variables(name, dataset_pool=dataset_pool)
        self.plot_histogram(name, **kwargs)
        
    def plot_scatter(self, name_x, name_y, index=None, main="", npoints=None, **kwargs):
        """Create a scatter plot of the attributes given by 'name_x' (x-axis) and 'name_y' (y-axis) and display its correlation coefficient.
        'npoints' controls the number of points in the plot. If it is None, all points are plotted, otherwise they are selected randomly.
        The plot is created using matplotlib.
        """
        from opus_core.plot_functions import plot_scatter
        v1, v2 = self._scatter(name_x, name_y, index=index, npoints=npoints)
        plot_scatter(v1, v2, name_x, name_y, main, **kwargs)
        
    def r_histogram(self, name, index=None, main="", prob=1, breaks=None, file=None, device='png'):
        """Create a histogram of the attribute given by 'name', including density line, using R. 
        If 'file' is given, the plot is outputed into a file of type given by 'device' ('pdf', 'png', etc.)
        rpy2 module required.
        """
        import rpy2.robjects as robjects
        import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects

        r = robjects.r

        if breaks is None:
            breaks = "Sturges"
        if file:
            rcode = '%s("%s")' % (device, file)
            r(rcode)
        else:
            r.X11()

        if index is not None:
            values = self.get_attribute_by_index(name, index)
        else:
            values = self.get_attribute(name)
        values = robjects.FloatVector(values)
        r.hist(values, breaks=breaks, main=main, xlab=name, prob=prob)
        r.lines(r.density(values))
        if file:
            r['dev.off']()

    def r_scatter(self, name_x, name_y, index=None, main="", npoints=None, file=None, device='png'):
        """Using R, create a scatter plot of the attributes given by 'name_x' (x-axis) 
         and 'name_y' (y-axis) and display its correlation coefficient.
        'npoints' controls the number of points in the plot. If it is None, all points are plotted, 
        otherwise they are selected randomly.
        If 'file' is given, the plot is outputed into a file of type given by 'device'. ('pdf', 'png', etc.)
        rpy2 module required.
        """
        import rpy2.robjects as robjects
        import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects

        r = robjects.r
        v1, v2 = self._scatter(name_x, name_y, index, npoints)
        if file:
            rcode = '%s("%s")' % (device, file)
            r(rcode)
        else:
            r.X11()
        r.plot(robjects.FloatVector(v1), robjects.FloatVector(v2), main=main, xlab=name_x, ylab=name_y)
        if file:
            r['dev.off']()
            
    def r_image(self, name, main="", xlab="x", ylab="y", min_value=None, max_value=None, white_background=True, 
                file=None, device='png', coordinate_system=None):
        """ Plots a 2D image of attribute given by 'name'. rpy2 module and R library 'fields'
            required. The dataset must have a method 'get_2d_attribute' defined that returns
            a 2D array that is to be plotted. If min_value/max_value are given, all values
            that are smaller/larger than these values are set to min_value/max_value.
            If white_background is True, as white background is considered the minimum value of the array.
            If 'file' is given, the plot is outputed into a file of type given by 'device'. ('pdf', 'png', etc.)
            If coordinate_system is None, dataset must have self._coordinate_system defined. It is a tuple of 2 attribute names 
            that define the x and y axis, respectively.
        """
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects
        r = robjects.r
        
        tdata = self.get_2d_attribute(name, coordinate_system=coordinate_system)
        nonmaskedmin = ma.minimum(tdata)
        if max_value == None:
            max_value = ma.maximum(tdata)
        if min_value == None:
            min_value = nonmaskedmin
        data_mask = tdata.mask
        tdata = clip(ma.filled(tdata,min_value), min_value, max_value)
        value_range = max_value-min_value
        background = min_value-value_range/100
        tdata = ma.filled(ma.masked_array(tdata, mask=data_mask), background)
        data = zeros(tdata.shape, dtype=float32)
        idx = arange(tdata.shape[1]-1,-1,-1)
        for i in range(data.shape[0]):
            data[i,idx] = tdata[i,:]
        xlen = data.shape[0]
        ylen = data.shape[1]
        
        fields = importr("fields")

        if file:
            rcode = '%s("%s")' % (device, file)
            r(rcode)
        else:
            r.X11()
        if white_background:
            color = r.c('white', r.rainbow(150)[20:150])
        else:
            color = r.rainbow(150)[20:150]

        fields.image_plot(z=data, x=r.seq(1,xlen), y=r.seq(1,ylen),
                xlab=xlab, ylab=ylab, main=main, sub=name,
                col=color)
        if file:
            r['dev.off']()

    def stringToList(self, string):
        list = string.split(',')
        for i in range(list.__len__()):
            list[i] = str(list[i]).strip()
        return list

    # This function is used to create a vector-based map
    def plot_map(self, name=None, main="", xlab="x", ylab="y", min_value=None,
                 max_value=None, file=None, my_title="", filter=None, background=None,
                 color_list=None, range_list=None, label_list=None, is_animation=False,
                 year=None, resolution=96, page_dims='8.5,5.5', map_lower_left='0.5,0.5', 
                 map_upper_right='6.0,5.0', legend_lower_left='6.5,0.5', legend_upper_right='6.9,5.0', 
                 project_name=None):
        """
        Draws a vector-based map using shapefiles. Mapnik is required and can be downloaded at http://www.mapnik.org/
        Arguements:
        'name' is the name of the attribute that is to be mapped
        'xlab' is an optional label for the x-axis (not yet implemented - this was an option used for matplotlib maps)
        'ylab' is an optional label for the y-axis (not yet implemented - this was an option used for matplotlib maps)
        'min_value' is the minimum value that will be included in the color bar range (used for linear scale and replacing 'min' and 'max' keywords)
        'max_value' is the maximum value that will be included in the color bar range (used for linear scale and replacing 'min' and 'max' keywords)
        'file' is the output filename of the PNG map 
        'my_title' is the text that will be printed at the top of the map image file
        'filter' (not yet implemented - this was an option used for matplotlib maps)
        'background' (not yet implemented - this was an option used for matplotlib maps)
        'color_list' is a list of colors to use in the map
        'range_list' is a list of range boundaries that specify each bucket of values
        'label_list' is a list of labels that will be applied to the buckets of values
        'is_animation' will be set to true if plot_map is called to make a frame of an animation sequence
        'year' will be printed at the top of each frame in an animation
        'resolution' is the user's computer's DPI (for converting inches to pixels)
        'page_dims' the the measurements (in inches) of the resulting map image
        'map_lower_left' is the lower left coordinates of the map
        'map_upper_right' is the upper right coordinates of the map
        legend_lower_left' is the lower left coordinates of the legend
        legend_upper_right' is the upper right coordinates of the legend
        """

        useDefaultValues = color_list == None or range_list == None or label_list == None
        
        if (useDefaultValues):
            color_list = ['#e0eee0', '#c7e9c0', '#a1d99b', '#7ccd7c', '#74c476', '#41ab5d', '#238b45', '#006400', '#00441b', '#00340b'] # green
        else:
            if color_list.__class__ == str:
                color_list = self.stringToList(color_list)
            if range_list.__class__ == str:
                range_list = self.stringToList(range_list)
            if label_list.__class__ == str:
                label_list = self.stringToList(label_list)
        
        name = VariableName(name).get_alias()
        if name not in self.get_known_attribute_names():
            raise StandardError, "Attribute " + name + " not known."

        # Determine the column header of the attributes to be used.
        # .dbf files can only have a max of 10 chars in a single cell
        col_header = None
        if (name.__len__() > 10):
            col_header = name[name.__len__()-10:].upper()
        else:
            col_header = name.upper()
        
        # Sort the ID array elements and their corresponding attribute array elements to have the 
        #    same order as the master .dbf file and write the arrays out to a .dbf shapefile.
        from opus_core.store.dbf_storage import dbf_storage
        
        data_path = paths.OPUS_DATA_PATH
        
        if not project_name: project_name = os.environ['OPUSPROJECTNAME'] # OPUSPROJECTNAME is only defined when this function is called by the GUI
        shapefile_dir = os.path.join(data_path, project_name, 'shapefiles') 
        storage_for_dbf = dbf_storage(storage_location=shapefile_dir)
        # create the MASTER dbf if it does not exist (the resulting MASTER file is much larger than it would have been if created manually)
        master_dbf_filepath = os.path.join(shapefile_dir,'MASTER_'+self.dataset_name+'.dbf')
        if not os.path.exists(master_dbf_filepath):
            id_name = self.get_id_name()[0]
            master_dbf_data = storage_for_dbf.load_table(table_name=self.dataset_name)[id_name]
            storage_for_master_dbf = dbf_storage(storage_location=shapefile_dir)
            master_dbf_dict = {id_name:master_dbf_data}
            storage_for_master_dbf.write_table(table_name='MASTER_'+self.dataset_name, table_data=master_dbf_dict)
        
        unique_id = storage_for_dbf.get_column_names(table_name='MASTER_'+self.dataset_name)[0]
        unique_id_arr = storage_for_dbf.load_table(table_name='MASTER_'+self.dataset_name)[unique_id]

        # Check if the number of IDs in the .dbf is greater than, less than, or equal to the number of IDs in the dataset
        dataset_id_arr = self.get_id_attribute()
        if self.dataset_name == 'gridcell' and unique_id_arr.__len__() > dataset_id_arr.__len__():
            from numpy import intersect1d, zeros
            unique_id_arr_trunc = intersect1d(unique_id_arr, dataset_id_arr)
            index_arr = self.get_id_index(unique_id_arr_trunc)
            attrib_arr = self.get_attribute_by_index(name, index_arr)
            longer_arr_ptr = 0
            shorter_arr_ptr = 0
            # The zeros function is used so that all IDs that exist in the .dbf file, but not the dataset are matched to an attribute value of 0
            if attrib_arr.__len__() > 0:
                full_attrib_arr = zeros(shape=unique_id_arr.__len__(), dtype=attrib_arr[0].__class__)
            # This loop will only work for gridcells because it requires that the IDs in the shapefile be in numerical order
            while longer_arr_ptr < unique_id_arr.__len__():
                if unique_id_arr[longer_arr_ptr] == unique_id_arr_trunc[shorter_arr_ptr]:
                    full_attrib_arr[longer_arr_ptr] = attrib_arr[shorter_arr_ptr]
                    shorter_arr_ptr += 1
                longer_arr_ptr += 1 
            attrib_arr = full_attrib_arr
        elif self.dataset_name == 'gridcell' and unique_id_arr.__len__() < dataset_id_arr.__len__():
            raise Exception('Error: .dbf shapefile has too few values for ' + unique_id + '.')
        else: # unique_id_arr.__len__() == dataset_id_arr.__len__() or self.dataset_name != 'gridcell':
            index_arr = self.get_id_index(unique_id_arr)
            attrib_arr = self.get_attribute_by_index(name, index_arr)
        
        # If attrib_arr contains boolean values, it needs to be converted to type int so that the Mapnik filter can be applied
        if attrib_arr.dtype.str == '|b1':
            from numpy import empty
            equiv_int_arr = empty(shape=attrib_arr.__len__(), dtype=int)
            for i in range(attrib_arr.__len__()): 
                equiv_int_arr[i] = attrib_arr[i]
            attrib_arr = equiv_int_arr
        
        dataset_dict = {unique_id:unique_id_arr, col_header:attrib_arr}
        storage_for_dbf.write_table(table_name=self.dataset_name, table_data=dataset_dict)
        
        # determine map file dimensions
        page_dims_list = page_dims.split(',')
        
        result_file_width = int(int(resolution) * float(page_dims_list[0]))
        result_file_height = int(int(resolution) * float(page_dims_list[1]))
        
        # determine map size        
        map_lower_left_coords = map_lower_left.split(',')
        map_upper_right_coords = map_upper_right.split(',')
        
        map_width_px = int(int(resolution) * (float(map_upper_right_coords[0]) - float(map_lower_left_coords[0])))
        map_height_px = int(int(resolution) * (float(map_upper_right_coords[1]) - float(map_lower_left_coords[1])))
        
        # Use Mapnik to draw the map
        from mapnik import Map, Rule, PolygonSymbolizer, LineSymbolizer, Filter, Color, Style, Layer, Shapefile, Image, render_to_file, save_map, render
        m = Map(map_width_px,map_height_px,"+proj=latlong +datum=WGS84")
        m.background = Color('#ffffff')
        s = Style()
        
        if (max_value != None):
            max_val = min(attrib_arr.max(), max_value)
        else:
            max_val = attrib_arr.max()
        if (min_value != None):
            min_val = max(attrib_arr.min(), min_value)
        else:
            min_val = attrib_arr.min()
        num_buckets = color_list.__len__()

        if (range_list == ['equal_percentage_scale']):
            from numpy import sort
            sortedAttribs = sort(attrib_arr,kind='quicksort')
            bucket_size = sortedAttribs.__len__() / num_buckets
            # create buckets with 100/num_buckets percent of data elements in each
            range_list = []
            range_list.append(str("%.2f" % min_val))
            for i in range(1,num_buckets):
                range_list.append(str("%.2f" % sortedAttribs[i * bucket_size]))
            range_list.append(str("%.2f" % max_val)) 
        elif (useDefaultValues or range_list == ['linear_scale']):
            # convert min_val and max_val to floats
            min_val *= 1.0
            max_val*= 1.0
            # set linearly increasing ranges for the range list
            range_list = []
            range_list.append(str("%.2f" % min_val))
            bucket_range = (max_val - min_val) / num_buckets
            for i in range(1,num_buckets):
                range_list.append(str("%.2f" % (min_val + i * bucket_range)))
            range_list.append(str("%.2f" % max_val))
        else:
            if range_list[0].upper() == 'MIN':
                range_list[0] = (str("%.2f" % min_val))
            if range_list[range_list.__len__()-1].upper() == 'MAX':
                range_list[range_list.__len__()-1] = (str("%.2f" % max_val))
        
        if (useDefaultValues or label_list == ['range_labels']):
            # set linearly increasing labels for the label list
            label_list = []
            for i in range(range_list.__len__()-1):
                label_list.append(str(range_list[i]) + " to " + str(range_list[i+1]))

        # Assign rules to the style
        for i in range(num_buckets):
            r = Rule()
            r.symbols.append(PolygonSymbolizer(Color(color_list[i])))
            if (unique_id == 'grid_id' or unique_id == 'parcel_id'): # color over the lines between gridcells and parcels
                r.symbols.append(LineSymbolizer(Color(color_list[i]),0.3))
            else:
                r.symbols.append(LineSymbolizer(Color('#000000'),0.1))
            r.filter = Filter('[' + col_header + '] >= ' + str(range_list[i]) + ' and [' + col_header + '] <= ' + str(range_list[i+1]))
            s.rules.append(r)
        
        # Assign a default color to all polygons not covered by the given range
        r = Rule()
        r.symbols.append(PolygonSymbolizer(Color('#dedede')))
        r.filter = Filter('[' + col_header + '] < ' + str(range_list[0]) + ' or [' + col_header + '] > ' + str(range_list[num_buckets]))
        s.rules.append(r)
        
        m.append_style('Map Style',s)
        lyr = Layer('Map Layer')
        lyr.datasource = Shapefile(file=os.path.join(shapefile_dir,self.dataset_name))
        lyr.styles.append('Map Style')
        m.layers.append(lyr)
        m.zoom_to_box(lyr.envelope())
        
        # save the map as an XML file to the indicators folder
        if not is_animation:
            xml_filename = file.strip(".png") + ".xml"
            save_map(m, xml_filename)
        
        # Add labels and color bar to image file
        # TODO: PIL should be added as a required package.  Once this is done, change these imports to 
        #     from PIL.Image import fromstring, new
        #     from PIL.ImageDraw import Draw
        # since the fromstring and new functions are actually from PIL.Image
        from Image import fromstring, new
        from ImageDraw import Draw
        
        # render the mapnik map to a PIL image        
        map_img = Image(map_width_px, map_height_px)
        render(m, map_img)
        map_pil_img = fromstring('RGBA', (map_width_px, map_height_px), map_img.tostring())
        
        # copy map image to a larger canvas
        result_file = new('RGBA', (result_file_width,result_file_height),color='#ffffff')
        
        box = (0,0,map_width_px,map_height_px)
        
        # PIL plots (0,0) as the upper left corner, for the GUI we want (0,0) to be in the lower left corner, so convert the y coordinate
        map_lower_left_x_coord_px = int(int(resolution) * float(map_lower_left_coords[0]))
        map_lower_left_y_coord_px = int(int(resolution) * (float(page_dims_list[1]) - float(map_lower_left_coords[1])))
        
        # y value range is 'map_lower_left_y_coord_px-map_height_px' to 'map_lower_left_y_coord_px' because PIL plots (0,0) as the upper left corner and we want (0,0) to be the lower left corner
        result_file.paste(map_pil_img, (map_lower_left_x_coord_px,map_lower_left_y_coord_px-map_height_px,map_lower_left_x_coord_px+map_width_px,map_lower_left_y_coord_px))
        
        draw = Draw(result_file)
        # draw the year at the top if this image will be used in an animation
        if is_animation:
            title_horiz_spacing = map_lower_left_x_coord_px
            title_vert_spacing = (float(page_dims_list[1]) - float(map_upper_right_coords[1])) / 2
            draw.text( (title_horiz_spacing,title_vert_spacing), str(year), fill='#000000' )

        # determine color bar coords 
        legend_lower_left_coords = legend_lower_left.split(',')
        legend_upper_right_coords = legend_upper_right.split(',')
        
        # PIL plots (0,0) as the upper left corner, for the GUI we want (0,0) to be in the lower left corner, so convert the y coordinates
        legend_lower_left_coords[1] = str(float(page_dims_list[1]) - float(legend_lower_left_coords[1]))
        legend_upper_right_coords[1] = str(float(page_dims_list[1]) - float(legend_upper_right_coords[1]))
        
        # draw the color bar
        legend_lower_left_x_coord_px = int(int(resolution) * float(legend_lower_left_coords[0]))
        legend_lower_left_y_coord_px = int(int(resolution) * float(legend_lower_left_coords[1]))
        
        legend_upper_right_x_coord_px = int(int(resolution) * float(legend_upper_right_coords[0]))
        legend_upper_right_y_coord_px = int(int(resolution) * float(legend_upper_right_coords[1]))
        
        box_height = int((legend_upper_right_y_coord_px - legend_lower_left_y_coord_px) / num_buckets)
        box_width = max(25, int(legend_upper_right_x_coord_px - legend_lower_left_x_coord_px))
        label_spacing = 10

        # This only works if there is a value range for every bucket. Map will not be produced if range values are missing
        for i in range(num_buckets):
            # If label values are missing, fill them in with empty strings
            while label_list.__len__() < num_buckets:
                label_list.append('')
            # Draw a box on the color bar           
            draw.rectangle((legend_lower_left_x_coord_px, 
                            legend_lower_left_y_coord_px+i*box_height, 
                            legend_lower_left_x_coord_px+box_width, 
                            legend_lower_left_y_coord_px+(i+1)*box_height), 
                            outline='#000000', 
                            fill=color_list[i])
            draw.text((legend_lower_left_x_coord_px+box_width+label_spacing, 
                       legend_lower_left_y_coord_px+i*box_height+(box_height/2)), 
                       label_list[i], 
                       fill='#000000')
        
        del draw
        result_file.save(file, 'PNG')

    # This function will be deleted when Mapnik completely replaces Matplotlib.  It will be left here temporarily for reference while Mapnik features are still being developed
    def plot_map_matplotlib(self, name, main="", xlab="x", ylab="y", min_value=None, max_value=None, file=None,
                 my_title="", filter=None, background=None, coordinate_system=None):
        """ Plots a 2D image of attribute given by 'name'. matplotlib required.
            The dataset must have a method 'get_2d_attribute' defined that returns
            a 2D array that is to be plotted. If min_value/max_value are given, all values
            that are smaller/larger than these values are set to min_value/max_value.
            Argument background is a value to be used for background. If it is not given,
            it is considered as a 1/100 under the minimum value of the array.
            Filter can be a string in which case it is considered as attribute name, or a 2D array.
            Points where filter is > 0 are masked out (put into background).
            If 'file' is given, the plot is outputed into the file.
            If coordinate_system is None, dataset must have self._coordinate_system defined. It is a tuple of 2 attribute names 
            that define the x and y axis, respectively.
        """
    
        import matplotlib
        #matplotlib.use('Agg')  # why is this here?
        
        from matplotlib.pylab import jet,imshow,colorbar,show,axis,savefig,close,figure,title,normalize
        from matplotlib.pylab import rot90
        
        if name not in self.get_known_attribute_names():
            self.compute_variables([name])
        tdata = self.get_2d_attribute(name, coordinate_system=coordinate_system)
        data_mask = tdata.mask
        if filter is not None:
            if isinstance(filter, str):
                if filter not in self.get_known_attribute_names():
                    self.compute_variables([filter])
                filter_data = self.get_2d_attribute(filter, coordinate_system=coordinate_system)
            elif isinstance(filter, ndarray):
                if not ma.allclose(filter.shape, tdata.shape):
                    raise StandardError, "Argument filter must have the same shape as the 2d attribute."
                filter_data = filter
            else:
                raise TypeError, "The filter type is invalid. A character string or a 2D numpy array allowed."
            filter_data = where(ma.filled(filter_data,1) > 0, 1,0)
            data_mask = ma.mask_or(data_mask, filter_data)
        nonmaskedmin = ma.minimum(tdata) - .2 * (ma.maximum(tdata) - ma.minimum(tdata))
        if max_value == None:
            max_value = ma.maximum(tdata)
        if min_value == None:
            min_value = nonmaskedmin

        #tdata = clip(ma.filled(tdata,min_value), min_value, max_value)
        tdata = ma.filled(tdata,min_value)
        if background is None:
            value_range = max_value-min_value
            background = min_value-value_range/100
        tdata = ma.filled(ma.masked_array(tdata, mask=data_mask), background)

        # Our data uses NW as 0,0, while matplotlib uses SW for 0,0.
        # Rotate the data so the map is oriented correctly.
        tdata = rot90(tdata, 1)

        jet()
        figure()
        norm = normalize(min_value, max_value)
        im = imshow(tdata,
            origin='lower',
            aspect='equal',
            interpolation=None,
            norm=norm,
            )
        tickfmt = '%4d'
        if isinstance(min_value, float) or isinstance(max_value, float):
            tickfmt='%1.4f'
        colorbar(format=tickfmt)

        title(my_title)
        axis('off')
        if file is not None:
            savefig(file)
            close()
        else:
            show()

    def r_correlation_image(self, names, file=None, device='png'):
        """ Creates an image of the correlation matrix for attributes given by names. 
        If 'file' is given, the plot is outputed into a file of type given by 'device' ('pdf', 'png', etc.)
        rpy2 package and R library fields required. 
        """
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects
        r = robjects.r
        
        tdata = self.correlation_matrix(names)
        data = zeros(tdata.shape, dtype=float32)
        idx = arange(tdata.shape[1]-1,-1,-1)
        for i in range(data.shape[0]):
            data[i,idx] = tdata[i,:]
        xlen = data.shape[0]

        fields = importr("fields")

        if file:
            rcode = '%s("%s")' % (device, file)
            r(rcode)
        else:
            r.X11()
        color = asarray(r.rainbow(150))[arange(110, 0,  -1)]
        seq = arange(xlen)
        fields.image_plot(z=data, x=seq, y=seq, col=color, xlab='', ylab='', xaxt='n', yaxt='n', 
                          zlim=array([min(0, data.min()), max(1, data.max())]))
        inv_seq = arange(xlen-1, -1, -1)
        r.text(r.rep(0, xlen), inv_seq, names, cex=0.7, pos=4, offset=0)
        r.text(seq, r.rep(xlen-1, xlen), names, srt=270, cex=0.7, pos=4, offset=0)
        if file:
            r['dev.off']()

    def correlation_image(self, names, useR=False, **kwargs):
        """ Creates an image of the correlation matrix for attributes given by names. 
        It uses the matplot library.
        """
        if useR:
            self.r_correlation_image(names, **kwargs)
        else:
            from opus_core.plot_functions import plot_matplot
            data = abs(self.correlation_matrix(names))
            plot_matplot(data, xlabels = names, ylabels=names, **kwargs)
        
    ##################################################################################
    ## Other methods
    ##################################################################################
        
    def get_dataset_name(self):
        """Determines the subdirectory in which variables for the dataset are implemented.
        """
        return self.dataset_name

    def get_attribute_header(self, name):
        """ Return dictionary containing the header metadata for the attribute 'name', or None if none
        """
        return self._get_attribute_box(name).get_header()
    
    def filled_masked_attribute(self, name, filled_value=0):
        """ Removes mask from  a masked array."""
        values = self.get_attribute(name)
        self.set_values_of_one_attribute(name, values=ma.filled(values, filled_value))
        
    def get_version(self, name):
        """ Return a version number of the attribute 'name'.
        """
        return self.attribute_boxes[name].get_version()
        
    def has_attribute(self, attribute_name):
        """Returns True if this dataset has this attribute name; False otherwise."""
        return attribute_name in self.get_known_attribute_names()

    def get_coordinate_system(self):
        """Returns tuple listing attributes defining the coordinate axes for this dataset,
        e.g. ('x', 'y').

        Datasets with a coordinate system should define _coordinate_system."""
        return self._coordinate_system
    
    def empty_dataset_like_me(self, in_storage=None, resources=None):
        """Returns a new instance of the same class as this dataset object,
        but with no loaded attributes.  Otherwise, the new object will have
        the same resources as this dataset object.  Merges resources from
        argument with resources from this object.
        """
        my_resources = Resources()
        my_resources.merge(self.resources)
        my_resources.merge(resources)
        return self.__class__(in_storage=in_storage, resources=my_resources)
    
    ##################################################################################
    ## Internal methods
    ##################################################################################
    
    def _create_id_mapping(self):
        id_array=self.get_id_attribute()
        if id_array.size == 0:
            if len(self.get_id_name()) > 1:
                self.id_mapping_type="D" # dictionary
                self.id_mapping = do_id_mapping_dict_from_array(id_array)
            else:
                self.id_mapping_type="A"
                self.id_mapping_shift = 0
                self.id_mapping = array([], dtype="int32")
            return
        if id_array.ndim == 1:
            maxid = id_array.max()
            minid = id_array.min()
            if (maxid-minid+1) <= (2*self.size()+1000):
                self.id_mapping_type="A" #array
                self.id_mapping_shift = minid
                self.id_mapping = do_id_mapping_array_from_array(id_array)
                return
        self.id_mapping_type="D" # dictionary
        self.id_mapping = do_id_mapping_dict_from_array(id_array)

    def _ensure_id_attribute_is_loaded(self):
        """Ensures that the id attribute is loaded, since many of the
        dataset operations require at least one attribute, or specifically
        the id attribute, to be loaded."""
        if not self.get_attribute_names():
            self.get_id_attribute()

    def determine_stored_attribute_names(self, resources=None, in_storage=None,
                                              in_table_name=None, attribute_type=AttributeType.PRIMARY):
        raise NotImplementedError('determine_stored_attribute_names')

    def _get_one_id_index(self, id):
        if self.id_mapping_type == "A":
            if id < 0:
                raise KeyError, "No id " + str(id) + " in dataset."
            idx = self.id_mapping[id - self.id_mapping_shift]
        else:
            idx = self.id_mapping[id]
        if idx < 0:
            raise KeyError, "No id " + str(id) + " in dataset."
        return idx

    def _get_attribute_box(self, name):
        if not isinstance(name, VariableName):
            name = VariableName(name)
        short_name = name.get_alias()
        if short_name in self.attribute_boxes.keys():
            return self.attribute_boxes[short_name]
        return None

    def are_dependent_variables_up_to_date(self, variable_name, version):
        """ Return True if the version of this variable correspond to versions of all
        dependent variables, otherwise False. That is, if any of the dependent variable
        must be recomputed, the method returns False.
        """
        short_name = variable_name.get_alias()
        if short_name in self.get_primary_attribute_names():
            return True
        dataset_name = variable_name.get_dataset_name()

        if dataset_name != self.get_dataset_name():
            self._raise_mismatch_dataset_name_error(variable_name)
        attribute_box = self._get_attribute_box(variable_name)
        if attribute_box is None:
            return False
        variable = attribute_box.get_variable_instance()
        if variable is None:
            return True # if a computed attribute doesn't have a variable instance, it was created 
                        # some other way, e.g. by add_attribute or by join, and doesn't have dependent variables.
        res = variable.are_dependent_variables_up_to_date(version)
        return not(False in res)

    def _change_id_mapping(self, ids):
        """Change the class attribute 'id_mapping' according to identifiers given by 'ids'.
        'ids' is a list or an array.
        """
        if self.id_mapping_type is None:
            self._create_id_mapping()
        else:
            if self.id_mapping_type == "A":
                if ids.size > 0:
                    self.id_mapping_shift = ids.min()
                else:
                    self.id_mapping_shift = 0
                del self.id_mapping
                self.id_mapping = do_id_mapping_array_from_array(ids)
            else:
                self.id_mapping.clear()
                self.id_mapping = do_id_mapping_dict_from_array(ids)

    def _update_id_mapping(self):
        """ Perform _change_id_mapping() with its own id-attribute.
        """
        self._change_id_mapping(self.get_id_attribute())

    def update_size(self):
        """Modify self.n according to the size of the id-attribute.
        """
        self.n = self.get_id_attribute().shape[0]

    def _do_flush_attribute(self, name):
        raise NotImplementedError('_do_flush_attribute')

    def _get_in_table_name_for_cache(self):
        in_table = None
        if self.resources.is_in("in_table_name"):
            in_table = self.resources["in_table_name"]
        if in_table is None:
            in_table = self.get_dataset_name()
        return in_table
    
    def create_and_check_qualified_variable_name(self, name):
        """Convert name to a VariableName if it isn't already, and add dataset_name to
        the VariableName if it is missing.  If it already has a dataset_name, make sure
        it is the same as the name of this dataset.  Also, if the variable name has an 
        alias, check that it isn't also the alias for a different expression, and also
        that it isn't equal to a primary attribute.
        """
        if isinstance(name, VariableName):
            vname = name
        else:
            vname = VariableName(name)
        if vname.get_dataset_name() is None:
            vname.set_dataset_name(self.get_dataset_name())
        else:
            self._check_dataset_name(vname.get_dataset_name())
        # check that the alias of the variable name isn't a duplicate of an alias for a different name
        alias = vname.get_alias()
        short = vname.get_short_name()
        # if alias==short, it's not an alias for a different name -- don't check anything
        if alias!=short:
            if alias in self._aliases:
                if vname!=self._aliases[alias]:
                    raise ValueError, "same alias for two expressions: %s and %s" % (vname.get_expression(), self._aliases[alias].get_expression())
            else:
                self._aliases[alias] = vname
            # make sure the alias isn't used for a primary attribute
            if alias in self.get_primary_attribute_names():
                raise ValueError, "alias %s is also a primary attribute" % alias
        return vname

    def _check_dataset_name(self, name):
        """check that name is the name of this dataset (overridden in InteractionDataset)"""
        if name!=self.get_dataset_name():
            raise ValueError, 'different dataset names for variable and dataset'

    def _add_id_attribute(self, data, name):
        self.add_attribute(data=data.astype(int32), name=name, metadata=AttributeType.PRIMARY)
        id_array=self.get_id_attribute()
        self.n = id_array.size
        self._change_id_mapping(id_array)

    def _add_to_primary_attribute_names(self, name):
        if name not in self.get_primary_attribute_names():
            self._primary_attribute_names.append(name)

    def remove_from_primary_attribute_names(self, name):
        if name in self.get_primary_attribute_names():
            self._primary_attribute_names.remove(name)

    def _is_id_loaded(self):
        if not self._id_names:
            return False
        return all_in_list(self._id_names, self.get_attribute_names())

    def try_id_mapping(self, id, return_value_if_not_found=-1):
        try:
            return self.get_id_index(id)
        except:
            return return_value_if_not_found

    def _create_hidden_id(self):
        if not (self.hidden_id_name in self.get_attribute_names()) or not (self.attribute_boxes[self.hidden_id_name].is_in_memory()):
            self.add_attribute(data=arange(self.size())+1, name=self.hidden_id_name)
            self._id_names = [self.hidden_id_name]
            self._create_id_mapping()

    def _is_hidden_id(self):
        if not self._id_names:
            return True
        return self._id_names[0] == self.hidden_id_name

    def __set_version(self, name, version):
        self.attribute_boxes[name].set_version(version)

    def __increment_version(self, name):
        if self.get_version(name) == None:
            self.__set_version(name, 0)
        else:
            self.__set_version(name, self.get_version(name)+1)

    def is_version(self, name, version):
        if name not in self.get_attribute_names():
            return False
        return self._get_attribute_box(name).is_version(version)

    def _get_attribute_type(self, name):
        return self.attribute_boxes[name].get_type()


    def _compute_one_variable(self, variable_name, dataset_pool, resources=None, quiet=False):
        """Compute variable given by the argument 'name'. The array of computed values is added to the class
        attribute 'set'. The argument resources (of type Resources)
        is passed to the 'compute' functions of the variables. 'quiet' turns
        some warnings in get_variable on and off.
        Note that the variable class must have a method 'compute_with_dependencies'.
        dataset_pool holds available datasets.
        """
        id_name = self._id_names
        if isinstance(id_name,list):
            id_name = id_name[0]
        if variable_name.get_dataset_name() is None:
            raise StandardError, "Computing variable " + \
                  variable_name.get_expression() + ":\n" + \
                  "Unable to get its dataset_name, maybe because of it's not a fully-qualified variable_name."
        if variable_name.get_dataset_name() != self.get_dataset_name():
            self._raise_mismatch_dataset_name_error(variable_name)

        attribute_box = self._get_attribute_box(variable_name)
        variable = None
        if attribute_box is not None:
            variable = attribute_box.get_variable_instance()
        if variable is None:
            variable = self.variable_factory.get_variable(variable_name, self, quiet=quiet, debug=self.debug,
                                                index_name=id_name)
        if variable == None:
            self._raise_error(StandardError,
                              "Initialization of variable '%s' failed!"
                              % variable_name.get_expression())
        if variable.is_lag_variable():
            variable_type = AttributeType.LAG
        else:
            variable_type = AttributeType.COMPUTED

        dataset_pool, compute_resources = self._prepare_dataset_pool_for_variable(dataset_pool, resources)
        new_version = self.add_attribute(
            data=variable.compute_with_dependencies(dataset_pool, compute_resources),
            name=variable_name,
            metadata=variable_type)
        if attribute_box is None:
            attribute_box = self._get_attribute_box(variable_name)
        attribute_box.set_variable_instance(variable)
        return new_version

    def _prepare_dataset_pool_for_variable(self, dataset_pool=None, resources=None):
        """ The method puts everything from resources that is of type Dataset into dataset_pool, everything else
        from resources stays there."""
        from opus_core.datasets.dataset_pool import DatasetPool
        if dataset_pool is None:
            try:
                dataset_pool = SessionConfiguration().get_dataset_pool()
            except:
                dataset_pool = DatasetPool()
        if not isinstance(resources, Resources):
            resources = Resources(resources)
        for key, value in resources.iteritems():
            if isinstance(value, AbstractDataset) or (key == "urbansim_constant"): #TODO: the second condition should be removed
                if not dataset_pool.has_dataset(key):                              # after all variable tests are transformed to
                    dataset_pool._add_dataset(key, value)                          # using VariableTester
        return dataset_pool, resources

    def _compute_if_needed(self, name, dataset_pool, resources=None, quiet=False, version=None):
        """Compute variable given by the argument 'name' only if this variable
        has not been computed before or if any of the dependency variables changed.
        For arguments see '_compute_one_variable'.
        dataset_pool holds available datasets.
        """
        if not isinstance(name, VariableName):
            variable_name = self.create_and_check_qualified_variable_name(name)
        else:
            variable_name = name
        short_name = variable_name.get_alias()
        # Hack!  If the alias isn't a primary attribute, but the actual short name of VariableName is,
        # then use the actual short name as short_name.  Really we should use the VariableName's 
        # actual short name as the attribute name, and keep a separate dictionary of aliases.
        real_short_name = variable_name.get_short_name()
        if short_name not in self._primary_attribute_names and real_short_name in self._primary_attribute_names:
            short_name = real_short_name
        if short_name in self.get_primary_attribute_names():
            if not (short_name in self.get_attribute_names()): #not loaded yet
                self.get_attribute(short_name) #causes lazy loading
            return self.get_version(short_name)
 
        if (short_name in self.get_attribute_names()) and (self.are_dependent_variables_up_to_date(
                            variable_name, version=version)):
           #if self.attribute_boxes[short_name].is_in_memory():
           #    return version
           #elif self.attribute_boxes[short_name].is_cached():
           #if self.attribute_boxes[short_name].is_cached():
           #    self.get_attribute(short_name)
            return self.get_version(short_name)

        return self._compute_one_variable(variable_name, dataset_pool, resources=resources, quiet=quiet)

    def _check_2d_coordinates(self):
        """Complains if this dataset doesn't have those attributes in its coordinate system.
        """
        coordinate_system = self.get_coordinate_system()
        if coordinate_system == None:
            raise Exception("Dataset '%s' may not use Dataset's get_2d_attribute, since it does not have x and y axes." %
                            self.dataset_name)

        if len(coordinate_system) != 2:
            raise Exception("Dataset '%s' may not use Dataset's get_2d_attribute, since it must have x and y axes, only." %
                            self.dataset_name)

    def flatten_by_id(self, two_d_array):
        """Given a 2d array of the shape produced by get_2d_attribute(), returns the 1D version.
        """
        x_attribute_name, y_attribute_name = self.get_coordinate_system()
        # unwrap the 2D array, reverse of the 2D method
        x = self.get_attribute(x_attribute_name)
        y = self.get_attribute(y_attribute_name)
        minx = int(ma.minimum.reduce(x))
        miny = int(ma.minimum.reduce(y))
        one_d_array = zeros(shape=x.shape, dtype=two_d_array.dtype.type)
        one_d_array[:] = two_d_array[x-minx, y-miny]
        return one_d_array


        
    def _scatter(self, name_x, name_y, index=None, npoints=None):
        reg = self.correlation_coefficient(name_x, name_y, index=index)
        logger.log_status("Correlation coefficient: ", reg)
        v1 = self.get_attribute(name_x)
        v2 = self.get_attribute(name_y)
        if index is not None:
            v1 = v1[index]
            v2 = v2[index]
        if (npoints <> None) and (npoints < v1.size()):
            rindex = randint(0, v1.size(), size=npoints)
            v1 = v1[rindex]
            v2 = v2[rindex]
        return (v1, v2)
    
    def create_regression_data(self, coefficients, index=None, const = 1,
                    constant_name = "constant"):
        """ It creates a data array corresponding to specified coefficients
        (=coefficients connected to a specification).
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel". 'const' is a constant
        (single value or 1D array) that is put into spots where variable is a constant,
        i.e. variable name is equal to 'constant_name'.
        If 'index' is not None, it is considered as index (1D array) of self determining
        which individuals should be considered.
        It returns a 2D array (nobservations|len(index) x nvariables).
        """
        neqs, nvar = coefficients.getshape()
        if neqs <> 1:
            self._raise_error(StandardError, "Coefficients' shape (%d,%d) must have '1' for first number!"
                              % (neqs, nvar))

        if index <> None:
            nobs = index.size
        else:
            nobs = self.size()
            index = arange(nobs)

        variables = coefficients.get_variable_names()
        const = update_constants(const, 1)

        # Fill the x array from data array
        try:
            x = zeros((nobs,nvar), dtype=float32)
        except:    # in case it fails due to memory allocation error
            logger.log_warning("Not enough memory. Deleting not used attributes.")
            self.unload_not_used_attributes(variables)
            gc.collect()
            x = zeros((nobs,nvar), dtype=float32)
        for ivar in range(nvar): # Iterate over variables
            if variables[ivar] == constant_name:
                x[:,ivar] = const
            else:
                x[:,ivar] = ma.filled(self.get_attribute(variables[ivar]),0.0)[index,]
        return x

    def create_regression_data_for_estimation(self, coefficients, index=None):
        """Like 'create_regression_data' but does not include columns that correspond to constants."""
        x = self.create_regression_data(coefficients, index)
        if x.shape[0] > 0:
            constants_positions = coefficients.get_constants_positions()
            not_eliminate = ones((x.shape[1],), dtype="int32")
            not_eliminate[constants_positions]=0
            return compress(not_eliminate, x, axis=1)
        return x

    def __deepcopy__(self, memo):
        attr_list = ['id_mapping', '_primary_attribute_names']
        new_dataset = copy.copy(self)
        for attr in attr_list:
            exec("new_dataset." + attr + " = copy.deepcopy(self." + attr + ")")
        new_dataset.attribute_boxes = {}
        for attr in self.attribute_boxes.keys():
            new_dataset.attribute_boxes[attr] = AttributeBox(
                new_dataset,
                copy.deepcopy(self.attribute_boxes[attr].get_data()),
                variable_name=copy.deepcopy(self.attribute_boxes[attr].get_variable_name()),
                version=copy.deepcopy(self.attribute_boxes[attr].get_version()),
                is_cached=copy.deepcopy(self.attribute_boxes[attr].is_cached()),
                is_in_memory=copy.deepcopy(self.attribute_boxes[attr].is_in_memory()),
                variable_instance=copy.deepcopy(self.attribute_boxes[attr].get_variable_instance()))
        return new_dataset

    def get_dependent_datasets(self, variables, quiet=False):
        """Return a list of dataset names that the given variables depend on."""
        from opus_core.variables.variable import get_dependency_datasets # to avoid circular imports
        result = []
        for variable in variables:
            if variable.get_alias() not in self._primary_attribute_names:
                result = result + get_dependency_datasets(variables=[variable], quiet=quiet)
        return result

    def delete_variable_instance(self, name):
        self._get_attribute_box(name).delete_variable_instance()

    def _raise_mismatch_dataset_name_error(self, variable_name):
        self._raise_error(StandardError,
                          "Mismatch of dataset's name '%s' and variable's dataset name '%s' when computing variable '%s'"
                          % (self.get_dataset_name(),
                             variable_name.get_dataset_name(),
                             variable_name.get_expression()))

    def _raise_error(self, error, msg):
        raise error("In dataset '%s': %s" % (self.get_dataset_name(), msg))
    
    def createTable(self, fileh, where, name=None, description=None, *args, **kwargs):
        """
        return a table (from pyTables) created from attributes of Dataset class.
        See createTable() method of tables.File class for more information on the parameters. 
        """
        
        from numpy import rec 
        if name is None:
            name = self._get_in_table_name_for_cache()
        self.load_dataset(attributes="*")
        attr_values = []
        attr_names = []
        for attr_name in self.get_known_attribute_names():
            attr_values.append(self.get_attribute(attr_name))
            attr_names.append(attr_name.encode("ascii"))
        recarray = rec.fromarrays(attr_values, names=attr_names)
        return fileh.createTable(where, name, recarray, *args, **kwargs)
   
from opus_core.tests import opus_unittest

class DatasetTests(opus_unittest.OpusTestCase):
    def test_exceptions(self):
        raised_exception = False
        try:
            dataset = AbstractDataset()
        except StandardError, e:
            raised_exception = True
            self.assert_("Must specify 'id_name'" in e.args[0])
        self.assert_(raised_exception)

    def test_aggregate_all(self):
        data = array([1,2,3])
        class DummyDataset(AbstractDataset):
            def determine_stored_attribute_names(self, *args, **kwargs):
                return []

            def get_attribute(self, name):
                return data

        dataset = DummyDataset(id_name=['id'])
        dataset.n = 3
        dataset.add_primary_attribute(data=arange(len(data))+1, name='id')
        dataset.add_primary_attribute(data=data, name='foo')
        values = dataset.aggregate_all(function='sum', attribute_name='foo')
        self.assertEqual(array([data.sum()]), values)
        self.assertEqual(1, values.ndim)

    def test_aggregate_over_ids(self):
        from numpy import allclose

        gridcell_grid_id = array([1,2,3])
        household_grid_id = array([1,2,2,2,3,3])

        class DummyGridcellDataset(AbstractDataset):
            def determine_stored_attribute_names(self, *args, **kwargs):
                return []

            def get_attribute(self, name):
                return gridcell_grid_id

        gridcell = DummyGridcellDataset(id_name=['grid_id'])
        gridcell.n = 3
        gridcell.add_primary_attribute(data=gridcell_grid_id, name='grid_id')

        # Sum over all households
        values = gridcell.aggregate_over_ids(ids=household_grid_id, what=array([1,10,100,1000,10000,100000]), function='sum')
        self.assert_(allclose(array([1,1110,110000]), values))
        self.assertEqual(1, values.ndim)

        # Sum values over just the first 4 households
        values = gridcell.aggregate_over_ids(ids=household_grid_id, what=array([1,10,100,1000,0,0]), function='sum')
        self.assert_(allclose(array([1,1110,0]), values))

        # Ignores id valuse not in household_grid_id
        values = gridcell.aggregate_over_ids(ids=array([1,2,9,9,9,9]), what=array([1,10,100,1000,0,0]), function='sum')
        self.assert_(allclose(array([1,10,0]), values))
        

if __name__ == '__main__':
    opus_unittest.main()
