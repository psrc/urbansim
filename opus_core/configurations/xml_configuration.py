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
    
    def __init__(self, filename, default_directory=None):
        """Initialize this configuration from the contents of the xml file named by 'filename'.
        Look first in the default directory if present; otherwise in the directory in which
        the Opus code is stored."""
        self._filepath = None
        if default_directory is not None:
            f = os.path.join(default_directory, filename)
            if os.path.exists(f):
                self._filepath = f
        if self._filepath is None:
            opus_core_dir = __import__('opus_core').__path__[0]
            workspace_dir = os.path.split(opus_core_dir)[0]
            self._filepath = os.path.join(workspace_dir, filename)
        # if self._filepath doesn't exist, ElementTree will raise an IOError
        self.root = ElementTree(file=self._filepath).getroot()
        if self.root.tag!='opus_project':
            raise ValueError, "malformed xml - expected to find a root element named 'opus_project'"
        
    def get_section(self, name):
        """Extract the section named 'name' from this xml project, convert it to a dictionary,
        put in default values from parent configuration (if any), and return the dictionary.
        Return None if there isn't such a section.  If there are multiple sections with the 
        given name, return the first one."""
        parentnode = self.root.find('parent')
        if parentnode is None:
            parentconfig = None
        else:
            # try looking for the parent in the same directory that this XML project is located
            default_dir = os.path.split(self._filepath)[0]
            parentconfig = XMLConfiguration(parentnode.text, default_directory=default_dir).get_section(name)
        x = self.root.find(name)
        if x is None:
            return parentconfig
        section = Configuration(self._node_to_config(x))
        if parentconfig is None:
            return section
        else:
            parentconfig.merge(section)
            return parentconfig

    def get_run_configuration(self, name, merge_controllers=True):
        """Extract the run configuration named 'name' from this xml project and return it.
        Note that one run configuration can inherit from another (in addition to the usual
        project-wide inheritance).  If merge_controllers is True, merge in the controller
        section into the run configuration."""
        config = self.get_section('scenario_manager/%s' % name)
        if config is None:
            raise ValueError, "didn't find a scenario named %s" % name
        if merge_controllers:
            # merge in the controllers in the model_manager/model_system portion of the project (if any)
            self._merge_controllers(config)
        if 'parent' in config:
            parent_config = self.get_run_configuration(config['parent'], merge_controllers=False)
            del config['parent']
            parent_config.merge(config)
            return parent_config
        elif 'parent_old_format' in config:
            d = config['parent_old_format']
            parent_config = self._make_instance(d['Class_name'], d['Class_path'])
            del config['parent_old_format']
            parent_config.merge(config)
            return parent_config
        else:
            return config

    def get_estimation_specification(self, model_name):
        estimation_section = self.get_section('model_manager/estimation')
        model = estimation_section[model_name]
        result = {}
        result['_definition_'] = model['all_variables'].values()
        for submodel_name in model.keys():
            if submodel_name!='all_variables':
                submodel = model[submodel_name]
                result[submodel['submodel_id']] = submodel['variables']
        self._merge_controllers(result)
        return result
    
    def _merge_controllers(self, config):
        # merge in the controllers in the model_manager/model_system portion of the project (if any) into config
        my_controller_configuration = self.get_section('model_manager/model_system')
        if my_controller_configuration is not None:
            if "models_configuration" not in config:
                config["models_configuration"] = {}
            for model in my_controller_configuration.keys():
                if model not in config["models_configuration"].keys():
                    config["models_configuration"][model] = {}
                config['models_configuration'][model]['controller'] = my_controller_configuration[model]

    def _node_to_config(self, node):
        config = {}
        for child in node:
            self._add_to_dict(child, config)    
        return config
    
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
            included = self.root.findall(node.text)
            if len(included)!=1:
                raise ValueError, "didn't find a unique match for included name %s" % node.text
            for child in included[0]:
                self._add_to_dict(child, result_dict)
        elif action=='only_for_includes':
            pass
        else:
            if 'config_name' in node.attrib:
                key = node.get('config_name')
            else:
                key = node.tag
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
        elif type_name=='string' or type_name=='password' or type_name=='variable_definition':
            return self._convert_string_to_data(node)
        elif type_name=='scenario_name':
            return node.text
        elif type_name=='unicode':
            return unicode(node.text)
        elif type_name=='selectable_list':
            return self._convert_list_to_data(node)
        elif type_name=='tuple':
            return self._convert_tuple_to_data(node)
        elif type_name=='list':
            return eval(node.text)
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
        elif type_name=='dictionary' or type_name=='submodel':
            return self._convert_dictionary_to_data(node)
        elif type_name=='class':
            return self._convert_class_to_data(node)
        elif type_name=='db_connection_hook':
            return node.text
        elif type_name=='model':
            # "skip" is the value used to indicate models to skip
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='table':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='dataset':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='variable':
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
        
    def _convert_list_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node)
        result_list = filter(lambda n: n is not None, r)
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
        
    def _convert_tuple_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node)
        return tuple(r)
        
    def _convert_file_or_directory_to_data(self, node):
        if node.get('parser_action', '')=='prefix_with_opus_data_path':
            prefix = os.environ.get('OPUS_DATA_PATH', '')
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
        name = node.tag
        children = node.getchildren()
        if len(children)==0:
            return name
        else:
            subdict = {}
            for child in children:
                self._add_to_dict(child, subdict)
            return {name: subdict}

from numpy import ma
from opus_core.tests import opus_unittest
class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        opus_core_dir = __import__('opus_core').__path__[0]
        self.test_configs = os.path.join(opus_core_dir, 'configurations', 'test_configurations')

    def test_types(self):
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
                          'list_test': [10, 20, 30],
                          'dicttest': {'str1': 'squid', 'str2': 'clam'},
                          'models': ['model1', 
                                     {'model2': {'group_members': 'all'}}, 
                                     {'model3': {'chooser': 'random', 'sampler': 'fussy'}}],
                          'mytables': ['gridcells', 'jobs'],
                          'mydatasets': ['gridcell', 'job']
                          })
            
    def test_whitespace_and_comments(self):
        f = os.path.join(self.test_configs, 'whitespace.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, {'description': 'a test configuration'})
        
    def test_str_and_unicode(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'strings.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        for k in config.keys():
            self.assert_(type(k) is str)
        self.assert_(type(config['s']) is str)
        self.assert_(type(config['u']) is unicode)

    def test_array(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'array.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        should_be = array([100, 300]) 
        self.assert_(ma.allclose(config['arraytest'], should_be, rtol=1e-6))
        
    def test_files_directories(self):
        f = os.path.join(self.test_configs, 'files_directories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        prefix = os.environ.get('OPUS_DATA_PATH', '')
        self.assertEqual(config, {'file1': 'testfile', 
                                  'file2': os.path.join(prefix, 'testfile'),
                                  'dir1': 'testdir', 
                                  'dir2': os.path.join(prefix, 'testdir')})
        
    def test_inheritance(self):
        # test inheritance with a chain of xml configurations
        f = os.path.join(self.test_configs, 'child_scenarios.xml')
        config = XMLConfiguration(f).get_run_configuration('child_scenario')
        self.assertEqual(config, 
            {'description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def test_inheritance_external_parent(self):
        # test inheritance with an external_parent (one with original name, one renamed)
        f = os.path.join(self.test_configs, 'grandchild_scenario_external_parent.xml')
        config1 = XMLConfiguration(f).get_run_configuration('grandchild')
        self.assertEqual(config1, 
            {'description': 'this is the grandchild', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def test_old_config_inheritance(self):
        # test inheriting from an old-style configuration 
        # (backward compatibility functionality - may be removed later)
        f = os.path.join(self.test_configs, 'child_scenario_oldparent.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        # 'years' is overridden in the child
        self.assertEqual(config['years'], (1980, 1981))
        # 'models' is inherited
        self.assert_('models' in config)
        self.assert_('random_nonexistant_key' not in config)
            
    def test_categories(self):
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

    def test_list_to_dict(self):
        f = os.path.join(self.test_configs, 'list_to_dict.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'datasets_to_preload': {'job': {}, 'gridcell': {'nchunks': 4}}})

    def test_include(self):
        f = os.path.join(self.test_configs, 'include_test.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
                         {'description': 'a test scenario',
                          'startyear': 2000,
                          'endyear': 2020,
                          'x': 10,
                          'y': 20,
                          'morestuff': {'x': 10, 'y': 20}})

    def test_class_element(self):
        # test a configuration element that is a specified class
        f = os.path.join(self.test_configs, 'database_configuration.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['input_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
    def test_class_element_with_categories(self):
        # like test_class_element, but with an additional layer of categorization in the xml
        f = os.path.join(self.test_configs, 'database_configuration_with_categories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['input_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
    def test_get_section(self):
        f = os.path.join(self.test_configs, 'estimate.xml')
        config = XMLConfiguration(f).get_section('model_manager/estimation')
        should_be = {
          'real_estate_price_model': {
            'all_variables': {'ln_cost': 'ln_cost=ln(psrc.parcel.cost)', 'unit_price': 'unit_price=urbansim_parcel.parcel.unit_price'},
            'single_family_residential': {'submodel_id': 24, 'variables': ['ln_cost']}},
          'models_to_estimate': ['real_estate_price_model']}
        self.assertEqual(config, should_be)
        
    def test_get_controller(self):
        # test getting a run specification that includes a controller in the xml
        f = os.path.join(self.test_configs, 'controller_test.xml')
        config = XMLConfiguration(f).get_run_configuration('baseline')
        should_be = {'models_configuration': {'real_estate_price_model': {'controller': {'prepare_for_run': {
          'name': 'prepare_for_run', 
          'arguments': {'specification_storage': 'base_cache_storage', 'specification_table': 'real_estate_price_model_specification'}
          }}}}}
        self.assertEqual(config, should_be)
        
    def test_get_estimation_specification(self):
        f = os.path.join(self.test_configs, 'estimate.xml')
        config = XMLConfiguration(f).get_estimation_specification('real_estate_price_model')
        should_be = {'models_configuration': {'real_estate_price_model': {'controller': {'prepare_for_run': {
              'name': 'prepare_for_run', 
              'arguments': {'specification_storage': 'base_cache_storage', 'specification_table': 'real_estate_price_model_specification'}
              }}}},
          '_definition_': ['ln_cost=ln(psrc.parcel.cost)', 'unit_price=urbansim_parcel.parcel.unit_price'],
          24: ['ln_cost']}
        self.assertEqual(config, should_be)
        
    def test_error_handling(self):
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
