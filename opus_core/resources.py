# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configuration import Configuration
from opus_core.session_configuration import SessionConfiguration

class Resources(Configuration):
    """In addition to everything in GeneralResources it has an access to SessionConfiguration."""
    def __init__(self, data={}):
        """The argument 'data' is a python native dictionary (class 'dict').
        """ 
        Configuration.__init__(self, data)
                
    def __getitem__(self, key):
        """First check for key in my configuration; then check in Session configuration"""
        try:
            return Configuration.__getitem__(self, key)
        except KeyError:
            return SessionConfiguration().get_dataset_from_pool(key)
            
    def is_in(self, key):
        """Return True if 'key' is in the dictionary or session configuration, otherwise False.
        """ 
        return (key in self or key in SessionConfiguration())
        
    def copy(self):
        c = Resources()
        c.merge(self)
        return c 
        
# Functions
############
def merge_resources_if_not_None(resources=None, pairs=[]):
    """Wrapper for the method merge_if_not_None."""
    if isinstance(resources, dict):
        resources = Resources(resources)
    if not isinstance(resources, Resources):
        resources = Resources()
    return resources.merge_if_not_None(pairs_to_dict(pairs))
    
def merge_resources_with_defaults(resources=None, pairs=[]):
    """Wrapper for the method merge_with_defaults."""
    if isinstance(resources, dict):
        resources = Resources(resources)
    if not isinstance(resources, Resources):
        resources = Resources()
    return resources.merge_with_defaults(pairs_to_dict(pairs))
    
def pairs_to_dict(pairs):
    """Convert list of tuples into dictionary."""
    result = {}
    for pair in pairs:
        result[pair[0]]=pair[1]
    return result 