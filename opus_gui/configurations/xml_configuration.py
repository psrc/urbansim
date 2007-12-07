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
from PyQt4 import QtCore, QtXml
from opus_core.configuration import Configuration

class XMLConfiguration(object):
    """
    An XMLConfiguration is a kind of configuration that represents a project 
    and that can be stored or loaded from an XML file.
    """
    
    def __init__(self, filename):
        """initialize this configuration from the contents of the xml file named by 'filename' """
        super(XMLConfiguration, self).__init__()
        f = QtCore.QFile(filename)
        is_ok = f.open(QtCore.QIODevice.ReadOnly)
        if not is_ok:
            raise IOError, "couldn't process XML file"
        doc = QtXml.QDomDocument()
        doc.setContent(f)
        self.project_node = doc.documentElement()
        if not self.project_node.isElement() or self.project_node.tagName()!='opus_project':
            raise ValueError, "malformed xml - expected to find a root element named 'opus_project'"
        f.close()
        
    def get_run_configuration(self, name):
        """extract the run configuration named 'name' from this xml project and return it"""
        scenario_section = self._get_section('scenario_manager')
        scenario = self._get_item_named(name, scenario_section)
        return self._node_to_config(scenario)

    def _get_section(self, section_name):
        # convert the named section to a dictionary and return the dictionary
        node = self.project_node.firstChild()
        while not node.isNull():
            element = node.toElement()
            if element.tagName()==section_name:
                return element
            node = node.nextSibling()
        raise ValueError, "didn't find an xml section named %s" % section_name
    
    def _get_item_named(self, name, section):
        # get the element named 'name'
        node = section.firstChild()
        while not node.isNull():
            node_name = node.attributes().namedItem('name').nodeValue()
            if node_name==name:
                return node
            node = node.nextSibling()
        raise ValueError, "didn't find an xml item named %s" % name
    
    def _node_to_config(self, node):
        changes = {}
        parent = None
        child = node.firstChild()
        while not child.isNull():
            if self._is_good_node(child):
                e = child.toElement()
                if e.tagName()!='item':
                    raise ValueError, "malformed xml - expected a tag 'item' "
                p = str(e.attributes().namedItem('parser_action').nodeValue())
                if p=='parent':
                    if parent is not None:
                        raise ValueError, 'multiple parent declarations'
                    parent = self._get_parent(e)
                elif p=='parent_old_format':
                    if parent is not None:
                        raise ValueError, 'multiple parent declarations'
                    parent = self._get_parent_old_format(e)
                else:
                    self._add_to_dict(e, changes)
            child = child.nextSibling()
        if parent is None:
            parent = Configuration()
        parent.merge(changes)
        return parent
    
    def _get_parent(self, node):
        # Process a node specifying the parent configuration defined using  
        # another scenario.
        parent_name = str(node.firstChild().nodeValue())
        return self.get_run_configuration(parent_name)

    def _get_parent_old_format(self, node):
        # Process a node specifying the parent configuration defined using  
        # n old-style configuration.  (This is a 
        # backward compatibility hack, and should be eventually removed.)
        d = self._convert_node_to_data(node)
        return self._make_instance(d['Class name'], d['Class path'])

    def _add_to_dict(self, node, result_dict):
        # 'node' should be an element node representing a key-value pair to be added to 
        # the dictionary 'result_dict' (unless it's a comment or whitespace)
        if self._is_good_node(node):
            # If this is a dictionary node that's just a category, add the children to result_dict;
            # otherwise add an entry to the dict with the item name as the key.
            p = str(node.attributes().namedItem('parser_action').nodeValue())
            if p=='category':
                # todo: check that type=dictionary
                child = node.firstChild()
                while not child.isNull():
                    self._add_to_dict(child, result_dict)
                    child = child.nextSibling()
            else:
                # make the dictionary keys be strings 
                # (later should they be turned into unicode instead??)
                config_name = str(node.attributes().namedItem('config_name').nodeValue())
                if config_name!='':
                    key = config_name
                else:
                    key = str(node.attributes().namedItem('name').nodeValue())
                result_dict[key] = self._convert_node_to_data(node)
            
    def _convert_node_to_data(self, node):
        # convert the information under node into the appropriate Python datatype.
        # To do this, branch on the node's type attribute.  For some kinds of data,
        # return None if the node should be skipped.  For example, for type="model"
        # return None if that is a model that isn't selected to be run
        type_name = str(node.attributes().namedItem('type').nodeValue())
        if type_name=='integer':
            return int(node.firstChild().nodeValue())
        elif type_name=='float':
            return float(node.firstChild().nodeValue())
        elif type_name=='string' or type_name=='password':
            return self._convert_string_to_data(node)
        elif type_name=='unicode':
            return unicode(node.firstChild().nodeValue())
        elif type_name=='list' or type_name=='tuple':
            return self._convert_list_or_tuple_to_data(node, type_name)
        elif type_name=='boolean':
            return self._convert_boolean_to_data(node)
        elif type_name=='file':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='directory':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='array':
            # the data should be a string such as '[100, 300]'
            # use eval to turn this into a list, and then turn it into a numpy array
            s = str(node.firstChild().nodeValue()).strip()
            return array(eval(s))
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
            
    def _is_good_node(self, node):
        """Return True if this node should be processed, False if this node should be ignored.  
        It should be ignored if it's a comment or just whitespace."""
        if node.isComment():
            return False
        elif node.isText() and node.toText().data().trimmed().isEmpty():
            return False
        else:
            return True

    def _get_good_children(self, node):
        # return the children of 'node', skipping comments and whitespace
        good = []
        n = node.firstChild()
        while not n.isNull():
            if self._is_good_node(n):
                good.append(n)
            n = n.nextSibling()
        return good

    def _get_single_child(self, node):
        # node should have exactly one child other than comments or whitespace.  Return that child.
        goodnodes = self._get_good_children(node)
        if len(goodnodes)!=1:
            raise ValueError, 'expected to find only one child node'
        return goodnodes[0]
    
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
        action = str(node.attributes().namedItem('parser_action').nodeValue())
        value = str(node.firstChild().nodeValue())
        if action=='empty_string_to_None' and value=='':
            return None
        else:
            return value
        
    def _convert_list_or_tuple_to_data(self, node, type_name):
        n = node.firstChild()
        result_list = []
        while not n.isNull():
            if self._is_good_node(n):
                d = self._convert_node_to_data(n)
                if d is not None:
                    result_list.append(d)
            n = n.nextSibling()
        if type_name=='tuple':
            return tuple(result_list)
        # type_name should be 'list'
        p = str(node.attributes().namedItem('parser_action').nodeValue())
        if p=='list_to_dictionary':
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
        
    def _convert_boolean_to_data(self, node):
        b = node.firstChild().nodeValue()
        if b=='True':
            return True
        elif b=='False':
            return False
        else:
            raise ValueError, 'malformed xml - expected a string representing a boolean'
        
    def _convert_file_or_directory_to_data(self, node):
        name = str(node.firstChild().nodeValue())
        action = str(node.attributes().namedItem('parser_action').nodeValue())
        if action=='prefix_with_urbansim_cache':
            prefix = os.environ.get('URBANSIM_CACHE', '')
            return os.path.join(prefix, name)
        else:
            return name
        
    def _convert_dictionary_to_data(self, node):
        result_dict = {}
        child = node.firstChild()
        while not child.isNull():
            self._add_to_dict(child, result_dict)
            child = child.nextSibling()
        return result_dict
        
    def _convert_class_to_data(self, node):
        items = {}
        child = node.firstChild()
        while not child.isNull():
            self._add_to_dict(child, items)
            child = child.nextSibling()
        class_name = items['Class name']
        class_path = items['Class path']
        # delete the class name and class path from the dictionary -- the remaining items 
        # will be the keyword arguments to use to create the instance
        del items['Class name']
        del items['Class path']
        i = self._make_instance(class_name, class_path, items)
        if node.attributes().namedItem('parser_action').nodeValue()=='execute':
            return i.execute()
        else:
            return i

    def _convert_custom_type_to_data(self, node, skip):
        # skip is a string that is the value when this node should be skipped
        child = node.firstChild()
        if child.nodeValue()==skip:
            return None
        name = str(node.attributes().namedItem('name').nodeValue())
        child = child.nextSibling()
        # if no more children, the item name is the value; otherwise return a dictionary
        if child.isNull():
            return name
        else:
            subdict = {}
            while not child.isNull():
                self._add_to_dict(child, subdict)
                child = child.nextSibling()
            return {name: subdict}

import os
from numpy import ma
from opus_core.tests import opus_unittest
class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        opus_gui_dir = __import__('opus_gui').__path__[0]
        self.test_configs = os.path.join(opus_gui_dir, 'configurations', 'test_configurations')

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
                          'list_test': ['squid', 'clam', u'uniclam'],
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
        prefix = os.environ.get('URBANSIM_CACHE', '')
        self.assertEqual(config, {'file1': 'testfile', 
                                  'file2': os.path.join(prefix, 'testfile'),
                                  'dir1': 'testdir', 
                                  'dir2': os.path.join(prefix, 'testdir')})
        
    def test_xml_inheritance(self):
        # test inheritance with a chain of xml configurations
        f = os.path.join(self.test_configs, 'childconfig.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, 
            {'description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def test_old_config_inheritance(self):
        # test inheriting from an old-style configuration 
        # (backward compatibility functionality - may be removed later)
        f = os.path.join(self.test_configs, 'childconfig_oldparent.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        # 'years' is overridden in the child
        self.assertEqual(config['years'], (1980, 1990))
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
            
    def test_error_handling(self):
        # there isn't an xml configuration named badname.xml
        self.assertRaises(IOError, XMLConfiguration, 'badname.xml')
        # badconfig1 doesn't have a root element called project
        f1 = os.path.join(self.test_configs, 'badconfig1.xml')
        self.assertRaises(ValueError, XMLConfiguration, f1)
        # badconfig2 is well-formed, but doesn't have a scenario_manager section 
        # (so getting the run configuration from it doesn't work)
        f2 = os.path.join(self.test_configs, 'badconfig2.xml')
        config2 = XMLConfiguration(f2)
        self.assertRaises(ValueError, config2.get_run_configuration, 'test_scenario')
        # badconfig3 is well-formed, with a scenario_manager section,
        # but there isn't a scenario named test_scenario
        f3 = os.path.join(self.test_configs, 'badconfig3.xml')
        config3 = XMLConfiguration(f2)
        self.assertRaises(ValueError, config3.get_run_configuration, 'test_scenario')
        
if __name__ == '__main__':
    opus_unittest.main()
