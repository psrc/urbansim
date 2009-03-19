# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import pickle

from opus_core.opus_error import OpusError
from opus_core.general_resources import GeneralResources

class Configuration(GeneralResources):
    """
    An Opus configuration is a hierarchical representation of the user-specified
    parameters and settings (the configuration) to use for the hierarchy of
    components required for part or all of a simulation run.  Typically, the 
    user-specified aspects are defined in a static dictionary of dictionaries,
    that are then converted into a tree of Configuration objects.  Each
    Configuration object contains a dictionary of the parameters and settings
    for a particular scope.  In addition, it may access the parameters and
    settings for enclosing scopes via the standard dictionary access mechanism
    ['key_name'].
    """
    def __init__(self, data={}, parent=None):
        """The hierarchical configuration information is in the python dictionary 'data'.
        The _scope in this is indicated by the path given by '_scope'.
        """
        self._parent = parent
        if data is not None:
            for key in data.keys():
                self[key] = data[key]
                
    def add_item(self, key, value):
        if type(value) in [dict, Configuration]:
            # Recursively convert dictionary into Configuration.
            super(Configuration, self).__setitem__(key, Configuration(value, parent=self))
        else:
            super(Configuration, self).__setitem__(key, value)
        
    def __getitem__(self, key):
        """If the key is not found at this level, look up thru the enclosing scope"""
        if key in self:
            return dict.__getitem__(self, key)
        try:
            return self._parent.__getitem__(key)
        except:
            raise KeyError("Key '%s' not found in this configuration" % key)
    
    def set_parent(self, parent):
        self._parent = parent
        
    def get(self, key, default=None):
        """If the key is not found at this level, look up thru the enclosing scope"""
        if key in self:
            return dict.get(self, key, default)
        try:
            return self._parent.get(key, default)
        except:
            return default
    
    def __getstate__(self):
        """Don't try to copy the parent reference.
        """
        return self
    
    def __setitem__(self, key, value):
        self.add_item(key, value)
    
    #def __delitem__(self, key):
        #return dict.__delitem__(key)
        
    def copy(self):
        """Return a new instance of same class populated with copy of the same data."""
        ev = 'from %s import %s as my_class' % (self.__module__, self.__class__.__name__)
        exec(ev)
        new_copy = my_class()
        
        # Remove any data created by the import
        for key in new_copy.keys():
            del new_copy[key]
            
        # Copy my data into this copy
        new_copy.merge(self)
        
        return new_copy
        
    def update(self, config):
        raise OpusError('Update method no longer supported for Configurations; use merge instead.')

    def merge(self, config):
        """Insert config's leaf values into this configuration. 
        
        'config' is a Configuration.
        """
        if config is None:
            return
        for key, value in config.iteritems():
            if key in self.keys():
                if isinstance(value, dict) or isinstance(value, Configuration):
                    self[key].merge(value)
                else:
                    self[key] = value
            else:
                if isinstance(value, dict) or isinstance(value, Configuration):
                    self[key] = Configuration(value, parent=self)
                else:
                    self[key] = value

    def replace(self, config):
        """Replace config's values into this configuration. 
        
        'config' is a Configuration.
        """
        if config is None:
            return
        for key, value in config.iteritems():
            self[key] = value
        
    def merge_defaults_with_arguments_and_config(self, config, **kwargs):
        if config is None:
            config = Configuration({})
        for arg in self:
            if (arg in kwargs): # and (kwargs[arg] is not None):
                config[arg]=kwargs[arg]
            elif (arg not in config) and ("default" in self[arg]):
                config[arg]=self[arg]["default"]
        return config
    
from opus_core.tests import opus_unittest
class ConfigurationTests(opus_unittest.OpusTestCase):
    class extended_dict(dict):
        def __init__(self):
            self['v1'] = 10
            self['v2'] = 20
        def has_new_method(self):
            return True
        
    def test_merging_None(self):
        data = {
            'keep':{
                'user':'user c',
            }
        }
        a = Configuration(data)
        a.merge(None)
        self.assertEqual(a, data)

    def test_merge(self):
        a = Configuration({
            'keep':{
                'user':'user c',
                }
            })
        b = Configuration({
            'input':{
                'user':'user b',
                },
            'output':{
                'user':'user c',
                }
            })
        a.merge(b)
        self.assertEqual(a['input']['user'], 'user b')
        self.assertEqual(len(a['input']), 1)

    def test_merge_replaces_only_leaves(self):
        config = Configuration({
            'in_config':{
                'db_host':'local',
                'db_user':'tester',
                },
            'foo':True,
            'bar':12,
            })
        my_config = Configuration({
            'in_config':{
                'db_name':'test',
                },
            'foo':False,
            })
        config.merge(my_config)
        self.assertEqual(config['in_config']['db_host'], 'local')
        self.assertEqual(config['in_config']['db_name'], 'test')
        self.assertEqual(config['foo'], False)
        self.assertEqual(config['bar'], 12)
    
    def test_insert_configuration_containing_a_dict(self):
        ext = {
            'a':self.extended_dict()
            }
        self.assert_(ext['a'].has_new_method())
        d = Configuration(ext)
        self.assert_(d['a'].has_new_method())
                     
    def test_insert(self):
        a = Configuration({
            'a':{
                'b':10,
                }
            })
        a['c'] = Configuration({
            'd':20,
            })
        self.assertEqual(a['c']['a']['b'], 10)
            
    def test_one_level(self):
        c = Configuration({'a':10,'b':20})
        self.assertEqual(c['a'], 10)
        raised_exception = False
        try:
            c['not a key']
        except KeyError:
            raised_exception = True
        self.assert_(raised_exception)
     
    def test_one_level_get(self):
        c = Configuration({'a':10,'b':20})
        self.assertEqual(c.get('a'), 10)
        raised_exception = False
        self.assertEqual(c.get('not a key', 30), 30)
   
    def test_two_levels(self):
        data = {
            'top_1':{
                'middle_a':{
                    'leaf 1.a':10,
                    },
                'middle_b':{
                    },
                },
            'top_2':{
                'middle_a':100
                }
            }
        c = Configuration(data)
        top_1 = c['top_1']
        top_2 = c['top_2']
        middle_1_a = top_1['middle_a']
        self.assertEqual(middle_1_a['top_2'], top_2)
        self.assertEqual(middle_1_a['top_2']['middle_a'], 100)
        
    def test_pickling(self):
        data = {
            'top_1':{
                'middle_a':{
                    'leaf 1.a':10,
                    },
                'middle_b':{
                    },
                },
            'top_2':{
                'middle_a':100
                }
            }
        c = Configuration(data)
        f = open('c.pickle', 'w')
        pickle.dump(c, f)
        f.close()
        f = open('c.pickle', 'r')
        d = Configuration(pickle.load(f))
        f.close()
        self.assertEqual(c['top_2']['middle_a'], d['top_2']['middle_a'])
        self.assertEqual(d['top_1']['top_2']['middle_a'], d['top_2']['middle_a'])
        import os
        os.remove('c.pickle')
        
    def test_copy_when_created_from_dictionary(self):
        data = {
            'a': {
                'b': 10,
                }
            }
        config = Configuration()
        config.merge(data)
        config2 = config.copy()
        self.assertDictsEqual(config, config2)
        
    def test_copy_when_created_from_class(self):
        config = _TestConfiguration()
        config["a"] = {}
        new_config = config.copy()
        self.assertDictsEqual(new_config['a'], Configuration({}))
        
class _TestConfiguration(Configuration):
    """
    A configuration used by the tests, above.
    """
    def __init__(self):
        data = {
            'a': {
                'b': 10,
                }
            }
        self.merge(data)

            
if __name__ == '__main__':
    opus_unittest.main()
            
