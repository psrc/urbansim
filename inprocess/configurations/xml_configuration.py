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

import os
from numpy import array
from xml.etree.cElementTree import ElementTree
from opus_core.configuration import Configuration

class XMLConfiguration(object):
    """
    An XMLConfiguration is a kind of configuration that represents a project 
    and that can be stored or loaded from an XML file.
    """
    
    def __init__(self, filename):
        """initialize this configuration from the contents of the xml file named by 'filename' """
        self.filename = filename
        self.root = ElementTree(file=filename).getroot()
        if self.root.tag!='opus_project':
            raise ValueError, "malformed xml - expected to find a root element named 'opus_project'"
        
    def get_run_configuration(self, name):
        """extract the run configuration named 'name' from this xml project and return it.  If there are
        multiple configurations with that name, return the first one."""
        for scenario in self.root.findall('scenario_manager/item'):
            if scenario.get('name')==name:
                return self._node_to_config(scenario)
        raise ValueError, "didn't find a scenario named %s" % name

    def _node_to_config(self, node):
        changes = {}
        parent = None
        # iterate over the children, skipping comments and whitespace (by only 
        # examining elements with the 'item' tag)
        for child in node.findall('item'):
            parser_action = child.get('parser_action', '')
            if parser_action.startswith('parent'):
                if parent is not None:
                    raise ValueError, 'multiple parent declarations'
                parent = self._get_parent(child, parser_action)
            else:
                self._add_to_dict(child, changes)    
        if parent is None:
            parent = Configuration()
        parent.merge(changes)
        return parent
    
    def _get_parent(self, node, parser_action):
        if parser_action=='parent':
            return self.get_run_configuration(node.text)
        elif parser_action=='parent_external':
            # find the path to the external configuration and load it
            data = self._convert_node_to_data(node)
            dir = os.path.dirname(self.filename)
            file = os.path.join(dir, data['path'])
            return XMLConfiguration(file).get_run_configuration(data['name'])
        elif parser_action=='parent_old_format':
            data = self._convert_node_to_data(node)
            return self._make_instance(data['Class_name'], data['Class_path'])
        else:
            raise ValueError, "unknown parser action %s" % parser_action
    
    def _get_node(self, path):
        # Return the node indicated by path.  We ought to be able to just use
        # the 'find' method; but we are using 'item' as the tag for all nodes.
        # So this path uses names after the top-level selection.
        names = path.split('/')
        node = self.root.find(names[0])
        for name in names[1:]:
            children = node.getchildren()
            i = 0
            while i<len(children) and children[i].get('name')!=name:
                i = i+1
            if i<len(children):
                node = children[i]
            else:
                raise ValueError, "invalid path: %s" % path
        return node

    def _add_to_dict(self, node, result_dict):
        # 'node' should be an element node representing a key-value pair to be added to 
        # the dictionary 'result_dict'.
        # If this is a dictionary node that's just a category, add the children to result_dict;
        # if it's an 'include', find the referenced node and add its children to result_dict;
        # otherwise add an entry to the dict with the item name as the key.
        action = node.get('parser_action', '')
        if action=='category':
            # todo: check that type=dictionary
            for child in node:
                self._add_to_dict(child, result_dict)
        elif action=='include':
            included_node = self._get_node(node.text)
            for child in included_node:
                self._add_to_dict(child, result_dict)
        elif action=='only_for_includes':
            pass
        else:
            if 'config_name' in node.attrib:
                key = node.get('config_name')
            else:
                key = node.get('name')
            result_dict[key] = self._convert_node_to_data(node)
            
    def _convert_node_to_data(self, node):
        # convert the information under node into the appropriate Python datatype.
        # To do this, branch on the node's type attribute.  For some kinds of data,
        # return None if the node should be skipped.  For example, for type="model"
        # return None if that is a model that isn't selected to be run
        type_name = node.get('type')
        if type_name=='integer':
            return int(node.text)
        elif type_name=='float':
            return float(node.text)
        elif type_name=='string' or type_name=='password':
            return self._convert_string_to_data(node)
        elif type_name=='unicode':
            return unicode(node.text)
        elif type_name=='list' or type_name=='tuple':
            return self._convert_list_or_tuple_to_data(node, type_name)
        elif type_name=='boolean':
            return eval(node.text)
        elif type_name=='file':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='directory':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='array':
            # the data should be a string such as '[100, 300]'
            # use eval to turn this into a list, and then turn it into a numpy array
            return array(eval(node.text))
        elif type_name=='dictionary':
            return self._convert_dictionary_to_data(node)
        elif type_name=='class':
            return self._convert_class_to_data(node)
        elif type_name=='model':
            # "skip" is the value used to indicate models to skip
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='table':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='dataset':
            return self._convert_custom_type_to_data(node, "Skip")
        else:
            raise ValueError, 'unknown type: %s' % type_name
            
    def _make_instance(self, class_name, path, keyword_args={}):
        # return an instance of the class named class_name.  path is the path to import it.
        if path=='':
            cls = eval('%s()' % class_name)
        else:
            # use the fully-qualified class name rather than a 'from pkg import classname' 
            # to avoid cluttering up the local name space
            # TODO: can this be replaced with __import__(path)
            exec('import %s' % path)
            cls = eval('%s.%s' % (path, class_name))
        inst = cls.__new__(cls)
        inst.__init__(**keyword_args)
        return inst
    
    def _convert_string_to_data(self, node):
        if node.text is None:
            if node.get('parser_action', '')=='empty_string_to_None':
                return None
            else:
                return ''
        else:
            return node.text
        
    def _convert_list_or_tuple_to_data(self, node, type_name):
        r = map(lambda n: self._convert_node_to_data(n), node)
        result_list = filter(lambda n: n is not None, r)
        if type_name=='tuple':
            return tuple(result_list)
        # type_name should be 'list'
        if node.get('parser_action', '')=='list_to_dictionary':
            result_dict = {}
            for x in result_list:
                if isinstance(x, str):
                    result_dict[x] = {}
                else:
                    # x should be a dictionary with one entry
                    result_dict.update(x)
            return result_dict
        else:
            return result_list
        
    def _convert_file_or_directory_to_data(self, node):
        if node.get('parser_action', '')=='prefix_with_urbansim_cache':
            prefix = os.environ.get('URBANSIM_CACHE', '')
            return os.path.join(prefix, node.text)
        else:
            return node.text
        
    def _convert_dictionary_to_data(self, node):
        result_dict = {}
        for child in node:
            self._add_to_dict(child, result_dict)
        return result_dict
        
    def _convert_class_to_data(self, node):
        items = {}
        for child in node:
            self._add_to_dict(child, items)
        class_name = items['Class_name']
        class_path = items['Class_path']
        # delete the class name and class path from the dictionary -- the remaining items 
        # will be the keyword arguments to use to create the instance
        del items['Class_name']
        del items['Class_path']
        i = self._make_instance(class_name, class_path, items)
        if node.get('parser_action', '')=='execute':
            return i.execute()
        else:
            return i

    def _convert_custom_type_to_data(self, node, skip):
        # skip is a string that is the value when this node should be skipped
        if node.text==skip:
            return None
        name = node.get('name')
        children = node.getchildren()
        if len(children)==0:
            return name
        else:
            subdict = {}
            for child in children:
                self._add_to_dict(child, subdict)
            return {name: subdict}

import os
from numpy import ma
from opus_core.tests import opus_unittest
class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        inprocess_dir = __import__('inprocess').__path__[0]
        self.test_configs = os.path.join(inprocess_dir, 'configurations', 'test_configurations')

    def skip_test_types(self):
        f = os.path.join(self.test_configs, 'manytypes.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'description': 'a test configuration',
                          'empty1': '',
                          'empty2': None,
                          'emptypassword': None,
                          'year': 1980,
                          'mybool': True,
                          'ten': 10.0,
                          'years': (1980, 1981),
                          'list_test': ['squid', 'clam', u'uniclam'],
                          'dicttest': {'str1': 'squid', 'str2': 'clam'},
                          'models': ['model1', 
                                     {'model2': {'group_members': 'all'}}, 
                                     {'model3': {'chooser': 'random', 'sampler': 'fussy'}}],
                          'mytables': ['gridcells', 'jobs'],
                          'mydatasets': ['gridcell', 'job']
                          })
            
    def skip_test_whitespace_and_comments(self):
        f = os.path.join(self.test_configs, 'whitespace.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, {'description': 'a test configuration'})
        
    def skip_test_str_and_unicode(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'strings.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        for k in config.keys():
            self.assert_(type(k) is str)
        self.assert_(type(config['s']) is str)
        self.assert_(type(config['u']) is unicode)

    def skip_test_array(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'array.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        should_be = array([100, 300]) 
        self.assert_(ma.allclose(config['arraytest'], should_be, rtol=1e-6))
        
    def skip_test_files_directories(self):
        f = os.path.join(self.test_configs, 'files_directories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        prefix = os.environ.get('URBANSIM_CACHE', '')
        self.assertEqual(config, {'file1': 'testfile', 
                                  'file2': os.path.join(prefix, 'testfile'),
                                  'dir1': 'testdir', 
                                  'dir2': os.path.join(prefix, 'testdir')})
        
    def skip_test_xml_inheritance(self):
        # test inheritance with a chain of xml configurations
        f = os.path.join(self.test_configs, 'childconfig.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
            {'description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def skip_test_xml_inheritance_external_parent(self):
        # test inheritance with an external_parent
        f = os.path.join(self.test_configs, 'childconfig_external_parent.xml')
        config = XMLConfiguration(f).get_run_configuration('grandchild_scenario')
        self.assertEqual(config, 
            {'description': 'this is the grandchild', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def skip_test_old_config_inheritance(self):
        # test inheriting from an old-style configuration 
        # (backward compatibility functionality - may be removed later)
        f = os.path.join(self.test_configs, 'childconfig_oldparent.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        # 'years' is overridden in the child
        self.assertEqual(config['years'], (1980, 1990))
        # 'models' is inherited
        self.assert_('models' in config)
        self.assert_('random_nonexistant_key' not in config)
            
    def skip_test_categories(self):
        f = os.path.join(self.test_configs, 'categories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'description': 'category test',
                          'real_name': 'config name test',
                          'precache': True,
                          'chunksize': 12,
                          'years': (1980, 1981),
                          'bool2': False,
                          'int2': 13})

    def skip_test_list_to_dict(self):
        f = os.path.join(self.test_configs, 'list_to_dict.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'datasets_to_preload': {'job': {}, 'gridcell': {'nchunks': 4}}})

    def skip_test_include(self):
        f = os.path.join(self.test_configs, 'include_test.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'description': 'a test scenario',
                          'startyear': 2000,
                          'endyear': 2020,
                          'x': 10,
                          'y': 20,
                          'morestuff': {'x': 10, 'y': 20}})

    def skip_test_class_element(self):
        # test a configuration element that is a specified class
        f = os.path.join(self.test_configs, 'database_configuration.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['input_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
    def skip_test_class_element_with_categories(self):
        # like skip_test_class_element, but with an additional layer of categorization in the xml
        f = os.path.join(self.test_configs, 'database_configuration_with_categories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['input_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
    def skip_test_error_handling(self):
        # there isn't an xml configuration named badname.xml
        self.assertRaises(IOError, XMLConfiguration, 'badname.xml')
        # badconfig1 has a syntax error in the xml
        f1 = os.path.join(self.test_configs, 'badconfig1.xml')
        self.assertRaises(SyntaxError, XMLConfiguration, f1)
        # badconfig2 doesn't have a root element called project
        f2 = os.path.join(self.test_configs, 'badconfig2.xml')
        self.assertRaises(ValueError, XMLConfiguration, f2)
        # badconfig3 is well-formed, but doesn't have a scenario_manager section 
        # (so getting the run configuration from it doesn't work)
        f3 = os.path.join(self.test_configs, 'badconfig3.xml')
        config3 = XMLConfiguration(f3)
        self.assertRaises(ValueError, config3.get_run_configuration, 'test_scenario')
        # badconfig4 is well-formed, with a scenario_manager section,
        # but there isn't a scenario named test_scenario
        f4 = os.path.join(self.test_configs, 'badconfig4.xml')
        config4 = XMLConfiguration(f4)
        self.assertRaises(ValueError, config4.get_run_configuration, 'test_scenario')
        
if __name__ == '__main__':
    opus_unittest.main()
