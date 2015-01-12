# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from attribute_type import AttributeType

class AttributeBox(object):
    """A container for a single attribute and meta-data about that attribute.
    """

    def __init__(self, parent, data, variable_name=None, type=None, version=None,
                 is_cached=False, is_in_memory=True, variable_instance=None, header=None):
        self._parent = parent
        self._data = data
        self._variable_name = variable_name
        self._type = type
        self._version = version
        self._is_cached = is_cached
        self._is_in_memory = is_in_memory
        self._variable_instance = variable_instance
        self._header = header

    def get_data(self, index = None):
        """Return an array which this attribute represents"""
        if index <> None:
            return self._data[index]
        return self._data

    def set_data(self, values, index = None):
        """Set 'values' as values of this attribute. Optional 'index' specifies indices
        of 'values' within the data array. Both arguments should be numpy arrays.
        """
        if index is not None:
            self._data[index] = values.astype(self._data.dtype)
        else:
            self._data = values

    def is_cached(self):
        return self._is_cached

    def set_is_cached(self, is_cached):
        self._is_cached = is_cached

    def is_in_memory(self):
        return self._is_in_memory

    def set_is_in_memory(self, is_in_memory):
        self._is_in_memory = is_in_memory

    def get_variable_name(self):
        return self._variable_name

    def get_type(self):
        return self._type

    def is_primary(self):
        return self.get_type() == AttributeType.PRIMARY

    def is_computed(self):
        return self.get_type() == AttributeType.COMPUTED

    def is_lag(self):
        return self.get_type() == AttributeType.LAG

    def set_type(self, type):
        self._type = type

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def is_version(self, version):
        return (self.get_version() == version)

    def get_full_name(self):
        return self.get_variable_name().get_expression()

    def set_variable_instance(self, variable_instance):
        self._variable_instance = variable_instance

    def get_variable_instance(self):
        return self._variable_instance

    def delete_variable_instance(self):
        self.set_variable_instance(None)

    def set_header(self, header):
        self._header = header

    def get_header(self):
        return self._header
