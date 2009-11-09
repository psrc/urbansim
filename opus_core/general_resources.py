# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger

class GeneralResources(dict):
    """
    General class for Resources.
    Contains the resources that act as inputs to, and outputs from, our
    model components.  This class extends Python's native dictionary class."""
    def __init__(self, data={}):
        """The argument 'data' is a python native dictionary (class 'dict').
        """ 
        self.initiate()
        self.merge(data)
        
    def initiate(self):
        """Initialize the dictionary."""
        self.clear()
        self = {}
        
    def merge(self, data):
        """Merge dictionary with the given data. The argument 'data' is an object of class 'dict'. 
        This method is a synonym for the 'update' method."""
        if isinstance(data, dict):
            self.update(data)
        
    def check_obligatory_keys(self, keys):
        """    'keys' is a list of strings. Checks if all given keys are contained in the dictionary.
            If not, an exception is raised. It is meant to be used for checking obligatory keys.
        """
        def check_and_raise_exception(self, key):
            if not self.is_in(key):
                raise StandardError, "Key '" + key + "' not contained in the resources."
            if self[key] == None:
                raise StandardError, "None value for key '" + key + "' not allowed."
            
        map(lambda(x): check_and_raise_exception(self, x), keys)

    def add(self, key, value):
        """Add a key-value pair into dictionary."""
        self[key] = value

    def remove(self, key):
        """Remove an entry 'key' from the dictionary.
        """ 
        if self.has_key(key):
            del self[key]
        else:
            logger.log_warning("Key " + key + " not contained in the dictionary!",
                                tags=["configuration"])
    
    def is_in(self, key):
        """Return True if 'key' is in the dictionary, otherwise False. It is a synonym for 'has_key'.
        """ 
        return self.has_key(key) 
        
    def is_None(self, key):
        """Return 1 if value of key is None, otherwise 0."""
        return (self[key] == None)
        
    def merge_if_not_None(self, data):
        """Adds data into self only if the corresponding value in 'data' is not None.
        'data' is a dictionary.
        The updated Resources object is returned.
        """
        resources = self
        for key in data.iterkeys():
            if data[key] is not None:
                resources.add(key, data[key])
        return resources
            
    def merge_with_defaults(self, data):
        """Adds data into self only if self does not contain the given key and 
        if the corresponding value in 'data' is not None.
        'data' is a dictionary.
        The updated Resources object is returned.
        """
        resources = self
        for key in data.iterkeys():
            if (key not in self.keys()) and (data[key] is not None):
                resources.add(key, data[key])
        return resources
        