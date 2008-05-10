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

import copy, os, pprint
from numpy import array
from xml.etree.cElementTree import ElementTree
from opus_core.configuration import Configuration

class XMLConfiguration(object):
    """
    An XMLConfiguration is a kind of configuration that represents a project 
    and that can be stored or loaded from an XML file.
    """
    
    def __init__(self, filename, default_directory=None, is_parent=False):
        """Initialize this configuration from the contents of the xml file named by 'filename'.
        Look first in the default directory if present; otherwise in the directory in which
        the Opus code is stored.  If is_parent is true, mark all of the nodes as inherited
        (either from this configuration or a grandparent)."""
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
        # self.tree is the xml tree (without any inherited nodes); 
        # self.full_tree is the xml tree with all the inherited nodes as well
        # parent_map is a dictionary that can be used to work back up the XML tree
        # these are all set by the _initialize method
        self.tree = None
        self.full_tree = None
        self.parent_map = None
        self.name = os.path.basename(self._filepath).split('.')[0]
        self.pp = pprint.PrettyPrinter(indent=4)
        self._initialize(ElementTree(file=self._filepath), is_parent)
        
    def update(self, newconfig_str):
        """Update the contents of this configuration from the string newconfig_str 
        (a string representing an xml configuration).  Ignore any inherited nodes in newconfig_str."""
        # Note that this doesn't change the name of this configuration, or the _filepath
        str_io = StringIO.StringIO(newconfig_str)
        etree = ElementTree(file=str_io)
        self._remove_inherited_nodes(etree.getroot())
        self._initialize(etree, False)
        
    def get_section(self, name):
        """Extract the section named 'name' from this xml project, convert it to a dictionary,
        and return the dictionary.  Return None if there isn't such a section.  If there are 
        multiple sections with the given name, return the first one."""
        x = self._find(name)
        if x is None:
            return None
        else:
            return Configuration(self._node_to_config(x))

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
        # sort the list of values to make it easier to test the results
        vals = model['all_variables'].values()
        vals.sort()
        result['_definition_'] = vals
        for submodel_name in model.keys():
            if submodel_name!='all_variables':
                submodel = model[submodel_name]
                result[submodel['submodel_id']] = submodel['variables']
        return result
    
    def save(self):
        """save this configuration in a file with the same name as the original"""
        self.save_as(self._filepath)
        
    def save_as(self, name):
        """save this configuration under a new name"""
        # TODO: change name???
        self.tree.write(name)
        
    def get_opus_data_path(self):
        """return the path to the opus_data directory.  This is found in the environment variable
        OPUS_DATA_PATH, or if that environment variable doesn't exist, as the contents of the 
        environment variable OPUS_HOME followed by 'data' """
        path = os.environ.get('OPUS_DATA_PATH')
        if path is None:
            return os.path.join(os.environ.get('OPUS_HOME'), 'data')
        else:
            return path
        
    def _initialize(self, elementtree, is_parent):
        self.tree = elementtree
        self.full_tree = copy.deepcopy(self.tree)
        full_root = self.full_tree.getroot()
        if full_root.tag!='opus_project':
            raise ValueError, "malformed xml - expected to find a root element named 'opus_project'"
        parent_nodes = full_root.findall('general/parent')
        default_dir = os.path.split(self._filepath)[0]
        for p in parent_nodes:
            x = XMLConfiguration(p.text, default_directory=default_dir, is_parent=True)
            self._merge_parent_elements(x.full_tree.getroot(), '')
        if is_parent:
            for n in full_root.getiterator():
                if n.get('inherited') is None:
                    n.set('inherited', self.name)
        # Parent map... can be used for working back up the XML tree
        self.parent_map = dict((c, p) for p in self.full_tree.getiterator() for c in p)        

    def _find(self, path):
        # find path in my xml tree
        # this is like the 'find' provided by ElementTree, except that it also works with an empty path
        if path=='':
            return self.full_tree.getroot()
        else:
            return self.full_tree.getroot().find(path)
        
    def _merge_parent_elements(self, parent_node, path):
        # parent_node is a node someplace in a parent tree, and path is a path
        # from the root to that node.  Merge in parent_node into this configuration's
        # tree.  We are allowed to reuse bits of the xml from parent_node (the xml
        # for it is created on demand, so we don't need to make a copy).
        # Precondition: path gives a unique element in this configuration's xml tree.
        prev_child = None
        for child in parent_node.getchildren():
            if path=='':
                extended_path = child.tag
            else:
                extended_path = path + '/' + child.tag
            if self._find(extended_path) is None:
                # c doesn't exist in this tree, so we can just add it and
                # all its children.  We want to insert it at a sensible place in the
                # tree.  In the parent child is right after prev_child, and so in
                # the new tree we put child right after the local version of prev-child.
                if prev_child is None:
                    self._find(path).insert(0,child)
                else:
                    i = 1
                    if path=='':
                        children = self.full_tree.getroot().getchildren()
                    else:
                        children = self._find(path).getchildren()
                    for c in children:
                        if c.tag==prev_child.tag:
                            break  
                        i = i+1
                    self._find(path).insert(i,child)
            else:
                # c does exist in this tree.  Keep going further with
                # its children, in case some of them don't exist in this tree
                self._merge_parent_elements(child, extended_path)
            prev_child = child
            
    def _remove_inherited_nodes(self, etree):
        # remove any nodes with the 'inherited' attribute from etree
        i = 0
        while i<len(etree):
            if etree[i].get('inherited') is not None:
                del etree[i]
            else:
                self._remove_inherited_nodes(etree[i])
                i = i+1
    
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
            included = self._find(node.text)
            for child in included:
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
            return self._convert_string_to_data(node, int)
        elif type_name=='float':
            return self._convert_string_to_data(node, float)
        elif type_name=='string' or type_name=='password' or type_name=='variable_definition' or type_name=='path':
            return self._convert_string_to_data(node, str)
        elif type_name=='quoted_string':
            return "'%s'" % node.text
        elif type_name=='scenario_name':
            return node.text
        elif type_name=='unicode':
            return self._convert_string_to_data(node, unicode)
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
        elif type_name=='database_library':
            return ''
        elif type_name=='db_connection':
            return ''
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
        elif type_name=='python_code':
            return eval(node.text)
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
    
    def _convert_string_to_data(self, node, func):
        if node.text is None:
            if node.get('parser_action', '')=='blank_to_None':
                return None
            elif func==str:
                return ''
            else:
                raise ValueError, "found empty string in xml node but no parser action to convert it to None"
        else:
            return func(node.text)
        
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
            return os.path.join(self.get_opus_data_path(), node.text)
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
        # Special case database configs as they may contain a database_connection which
        # references another part of the XML.  We need to add those elements to the
        # dictionary if they are defined in that config before calling _make_instance
        if class_name == 'DatabaseConfiguration':
            # Look for a database_connection element...
            if items.has_key('database_connection'):
                database_hook = items['database_connection']
                #print "Found a database_hook = %s" % (database_hook)
                # Next, since we have a connection we must go find it in the data manager
                the_database = self.get_section('general/database_library/%s' %
                                                (database_hook))
                if the_database:
                    #print "Converting a database connection into a class"
                    #self.pp.pprint(the_database)
                    items.update(the_database)
                    #self.pp.pprint(items)
                # Get rid of the database_connection element since we just replaced it
                # with the real connection info
                del items['database_connection']
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
import StringIO
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
                          'quotedthing': r"'test\test'",
                          'empty1': '',
                          'empty2': None,
                          'emptypassword': None,
                          'year': 1980,
                          'mybool': True,
                          'ten': 10.0,
                          'emptyint': None,
                          'emptyfloat': None,
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
        # if the OPUS_HOME environment variable isn't set, temporarily set it so that
        # the prefix_with_opus_data_path parser command can be tested
        if 'OPUS_HOME' not in os.environ:
            os.environ['OPUS_HOME'] = os.path.expanduser('~/opus')
        f = os.path.join(self.test_configs, 'files_directories.xml')
        x = XMLConfiguration(f)
        config = x.get_run_configuration('test_scenario')
        prefix = x.get_opus_data_path()
        self.assertEqual(config, {'file1': 'testfile', 
                                  'file2': os.path.join(prefix, 'testfile'),
                                  'dir1': 'testdir', 
                                  'dir2': os.path.join(prefix, 'testdir')})
        
    def test_scenario_inheritance(self):
        # test inheritance of scenarios with a chain of xml configurations
        f = os.path.join(self.test_configs, 'child_scenarios.xml')
        config = XMLConfiguration(f).get_run_configuration('child_scenario')
        self.assertEqual(config, 
            {'description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def test_scenario_inheritance_external_parent(self):
        # test inheritance of scenarios with an external_parent (one with original name, one renamed)
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
        # 'squidcount' is new in the child
        self.assertEqual(config['squidcount'], 12)
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
        
    def test_get_section_of_child(self):
        f = os.path.join(self.test_configs, 'estimation_child.xml')
        config = XMLConfiguration(f).get_section('model_manager/estimation')
        should_be = {
          'real_estate_price_model': {
            'all_variables': {'ln_cost': 'ln_cost=ln(psrc.parcel.cost+10)',
                              'tax': 'tax=urbansim_parcel.parcel.tax',
                              'unit_price': 'unit_price=urbansim_parcel.parcel.unit_price'},
            'single_family_residential': {'submodel_id': 240, 'variables': ['ln_cost']}},
          'models_to_estimate': ['real_estate_price_model', 'household_location_choice_model']}
        self.assertEqual(config, should_be)
        
    def test_inherited_attributes(self):
        # make sure that inherited attributes are tagged as 'inherited'
        f = os.path.join(self.test_configs, 'estimation_child.xml')
        all_variables_node = XMLConfiguration(f).full_tree.find('model_manager/estimation/real_estate_price_model/all_variables')
        # the ln_cost variable is redefined in estimation_child, so it shouldn't have the 'inherited' attribute
        ln_cost_node = all_variables_node.find('ln_cost')
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is new, so also shouldn't have the 'inherited' attribute
        tax_node = all_variables_node.find('tax')
        self.assertEqual(tax_node.get('inherited'), None)
        # the unit_price variable is inherited and not overridden, so it should have 'inherited' set to the name of the parent
        unit_price_node = all_variables_node.find('unit_price')
        self.assertEqual(unit_price_node.get('inherited'), 'estimate')
        
    def test_grandchild_inherited_attributes(self):
        # test two levels of inheritance, with multiple inheritance as well
        f = os.path.join(self.test_configs, 'estimation_grandchild.xml')
        all_variables_node = XMLConfiguration(f).full_tree.find('model_manager/estimation/real_estate_price_model/all_variables')
        # the ln_cost variable is redefined in estimation_grandchild, so it shouldn't have the 'inherited' attribute
        ln_cost_node = all_variables_node.find('ln_cost')
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is inherited from estimation_child (there is also a definition in estimation_child2 but that 
        # shouldn't be used)
        tax_node = all_variables_node.find('tax')
        self.assertEqual(tax_node.get('inherited'), 'estimation_child')
        # the extratax variable is inherited from estimation_child2
        extratax_node = all_variables_node.find('extratax')
        self.assertEqual(extratax_node.get('inherited'), 'estimation_child2')
        # the unit_price variable is inherited from estimate
        unit_price_node = all_variables_node.find('unit_price')
        self.assertEqual(unit_price_node.get('inherited'), 'estimate')
        
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
        should_be = {'_definition_': ['ln_cost=ln(psrc.parcel.cost)', 'unit_price=urbansim_parcel.parcel.unit_price'],
          24: ['ln_cost']}
        self.assertEqual(config, should_be)
        
    def test_get_estimation_specification_of_child(self):
        f = os.path.join(self.test_configs, 'estimation_child.xml')
        config = XMLConfiguration(f).get_estimation_specification('real_estate_price_model')
        should_be = {'_definition_': ['ln_cost=ln(psrc.parcel.cost+10)', 'tax=urbansim_parcel.parcel.tax', 'unit_price=urbansim_parcel.parcel.unit_price'],
          240: ['ln_cost']}
        self.assertEqual(config, should_be)
        
    def test_save_as(self):
        # test saving as a new file name - this should also test save()
        f = os.path.join(self.test_configs, 'estimation_grandchild.xml')
        c = XMLConfiguration(f)
        str_io = StringIO.StringIO()
        c.save_as(str_io)
        # compare the strings removing white space
        squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        # rather than typing it in here, just read the value from the file
        est_file = open(f)
        should_be = est_file.read().replace(' ', '').replace('\n', '')
        self.assertEqual(squished_result, should_be)
        str_io.close()
        est_file.close()
        
    def test_update_1(self):
        # try update with a completely different project - make sure stuff gets replaced
        f = os.path.join(self.test_configs, 'estimation_grandchild.xml')
        config = XMLConfiguration(f)
        update_str = """<?xml version='1.0' encoding='UTF-8'?>
            <opus_project>
              <scenario_manager>
                <test_scenario type="scenario">
                  <i type="integer">42</i>
                  </test_scenario>
              </scenario_manager>
            </opus_project>"""
        config.update(update_str)
        run_config = config.get_run_configuration('test_scenario')
        self.assertEqual(run_config, {'i': 42})

    def test_update_2(self):
        # make sure nodes marked as inherited are filtered out when doing the update
        f = os.path.join(self.test_configs, 'estimation_grandchild.xml')
        config = XMLConfiguration(f)
        update_str = """<opus_project>
            <general>
              <parent type="file">estimation_child.xml</parent>
              <parent type="file">estimation_child2.xml</parent>
            </general>
            <data_manager inherited="someplace">
            </data_manager>
            <model_manager>
              <estimation type="dictionary" >
                <real_estate_price_model type="dictionary" >
                  <all_variables type="dictionary" >
                    <ln_cost type="variable_definition" >ln_cost=ln(psrc.parcel.cost+100)</ln_cost>
                    <tax type="variable_definition" inherited="estimation_child">tax=urbansim_parcel.parcel.tax</tax>
                  </all_variables>
                 </real_estate_price_model>
               </estimation>
            </model_manager>
           <scenario_manager/>
          </opus_project>"""
        config.update(update_str)
        str_io = StringIO.StringIO()
        config.save_as(str_io)
        # compare the strings removing white space
        squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        # rather than typing it in here, just read the value from the file
        est_file = open(f)
        should_be = est_file.read().replace(' ', '').replace('\n', '')
        self.assertEqual(squished_result, should_be)
        str_io.close()
        est_file.close()

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
        # badconfig5 has an empty string for an integer value, but no parser directive to turn it to None
        f5 = os.path.join(self.test_configs, 'badconfig5.xml')
        config5 = XMLConfiguration(f5)
        self.assertRaises(ValueError, config5.get_run_configuration, 'test_scenario')
        
if __name__ == '__main__':
    opus_unittest.main()
