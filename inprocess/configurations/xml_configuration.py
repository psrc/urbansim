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
import xml.dom.minidom
from opus_core.configuration import Configuration

class XMLConfiguration(Configuration):
    """
    An XMLConfiguration is a kind of configuration that can be stored or loaded from an XML file.
    """
    
    def __init__(self, filename):
        """initialize this configuration from the contents of the xml file named by 'filename' """
        super(XMLConfiguration, self).__init__()
        root = xml.dom.minidom.parse(filename)
        configNode = root.documentElement
        if configNode.nodeType!=configNode.ELEMENT_NODE or configNode.tagName!='configuration':
            raise ValueError, "malformed xml - expected to find a root element named 'configuration'"
        changes = {}
        for node in configNode.childNodes:
            if node.nodeType==node.ELEMENT_NODE and node.tagName=='parent':
                self._process_parent(node, filename)
            else:
                self._add_to_dict(node, changes)
        self.merge(changes)
        
    def _process_parent(self, node, filename):
        # Process a node specifying the parent configuration.  This may be defined using either 
        # another XML file or with an old-style configuration.  (The latter possibility is a 
        # backward compatibility hack, and should be eventually removed.)
        # This code actually allows multiple parents, which will be merged together with 
        # parents listed later overriding ones listed earlier.  This could be disallowed - 
        # although it might be useful, and doesn't cost anything to support.
        # Precondition: node should be an element node with the tag 'parent'
        children = self._get_good_children(node)
        if len(children)!=1:
            raise ValueError, 'ill-formed parent node - should have just one child'
        if children[0].tagName=='file':
            parentfilename = children[0].firstChild.data
            # dir is the path to the directory containing the xml file named by filename
            # if the parent file name is relative, find it relative to dir (join will ignore
            # dir if the parent file name is absolute)
            dir = os.path.split(os.path.abspath(filename))[0]
            fullpath = os.path.join(dir, parentfilename)
            parent = XMLConfiguration(fullpath)
            self.merge(parent)
        elif children[0].tagName=='oldconfig':
            path = children[0].getAttribute('path')
            class_name = children[0].firstChild.data
            # if the node doesn't have a 'path' attribute, the getAttribute method returns ''
            parent = self._make_instance(class_name, path)
            self.merge(parent)
        else:
            raise ValueError, "ill-formed parent node - expected either 'file' or 'oldconfig'"

    def _add_to_dict(self, node, result_dict):
        # 'node' should be an element node representing a key-value pair to be added to 
        # the dictionary 'result_dict' (unless it's a comment or whitespace)
        if self._is_node_to_ignore(node):
            return
        if node.nodeType!=node.ELEMENT_NODE:
            raise ValueError, 'internal error - argument is not an element node'
        result_dict[node.tagName] = self._convert_node_to_data(self._get_single_child(node))
            
    def _convert_node_to_data(self, node):
        # convert 'node' to the corresponding Python data, and return the data
        if node.nodeType==node.TEXT_NODE:
            return node.data
        # if it's not a text node, it needs to be an element
        if node.nodeType!=node.ELEMENT_NODE:
            raise ValueError, 'malformed xml - expected an element node'
        # branch on the element's tag to determine the type of the return data
        if node.tagName=='None':
            return None
        elif node.tagName=='int':
            return int(node.firstChild.data)
        elif node.tagName=='float':
            return float(node.firstChild.data)
        elif node.tagName=='str':
            return str(node.firstChild.data)
        elif node.tagName=='unicode':
            return unicode(node.firstChild.data)
        elif node.tagName=='list' or node.tagName=='tuple':
            goodnodes = filter(lambda n: not self._is_node_to_ignore(n), node.childNodes)
            result_list = map(lambda n: self._convert_node_to_data(n), goodnodes)
            if node.tagName=='tuple':
                return tuple(result_list)
            else:
                return result_list
        elif node.tagName=='bool':
            b = node.firstChild.data
            if b=='True':
                return True
            elif b=='False':
                return False
            else:
                raise ValueError, 'malformed xml - expected a string representing a boolean'
        elif node.tagName=='dict':
            result_dict = {}
            for child in node.childNodes:
                self._add_to_dict(child, result_dict)
            return result_dict
        elif node.tagName=='class':
            class_name = node.getAttribute('name')
            path = node.getAttribute('path')
            unicode_keyword_args = {}
            for child in node.childNodes:
                self._add_to_dict(child, unicode_keyword_args)
            keyword_args = {}
            for k, v in unicode_keyword_args.items():
                keyword_args[str(k)] = v
            return self._make_instance(class_name, path, keyword_args)
        else:
            raise ValueError, 'malformed xml - unknown tag name %s' % node.tagName
            
    def _is_node_to_ignore(self, node):
        """return True if this node should be ignored"""
        return node.nodeType==node.COMMENT_NODE \
          or (node.nodeType==node.TEXT_NODE and node.data.strip()=='') \
          or (node.nodeType==node.ELEMENT_NODE and node.getAttribute('selected')=='False') 

    def _get_good_children(self, node):
        # return the children of 'node', skipping comments and whitespace
        return filter(lambda n: not self._is_node_to_ignore(n), node.childNodes)

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

import os
from opus_core.tests import opus_unittest
class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        sandboxdir = __import__('sandbox').__path__[0]
        self.test_configs = os.path.join(sandboxdir, 'borning', 'configurations', 'test_configurations')

    def test_types(self):
        f = os.path.join(self.test_configs, 'manytypes.xml')
        config = XMLConfiguration(f)
        self.assertEqual(config, 
                         {'description': 'a test configuration',
                          'year': 1980,
                          'mybool': True,
                          'ten': 10.0,
                          'mynone': None,
                          'years': (1980, 1981),
                          'years_with_spaces': (1980, 1981),
                          'listofstrings': ['squid', 'clam'],
                          'models': ['model_name1', 
                                     {'model_name2': 'all'}, 
                                     {'model_name3': {'chooser': 'random'}},
                                     {'model_name4': {'chooser': 'random', 'sampler': 'fussy'}}],
                          'selectionstest': ['good name 1', 'good name 2']
                          })
            
    def test_whitespace_and_comments(self):
        f = os.path.join(self.test_configs, 'whitespace.xml')
        config = XMLConfiguration(f)
        self.assertEqual(config, {'description': 'a test configuration'})
        
    def test_str_and_unicode(self):
        # check that the keys in the config dictionary are unicode, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'strings.xml')
        config = XMLConfiguration(f)
        for k in config.keys():
            self.assert_(type(k) is unicode)
        self.assert_(type(config['s']) is str)
        self.assert_(type(config['u']) is unicode)
        
    def test_xml_inheritance(self):
        # test inheritance with a chain of xml configurations
        f = os.path.join(self.test_configs, 'childconfig.xml')
        config = XMLConfiguration(f)
        self.assertEqual(config, 
            {'description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})
            
    def test_old_config_inheritance(self):
        # test inheriting from an old-style configuration 
        # (backward compatibility functionality - may be removed later)
        f = os.path.join(self.test_configs, 'childconfig_oldparent.xml')
        config = XMLConfiguration(f)
        # 'years' is overridden in the child
        self.assertEqual(config['years'], (1980, 1990))
        # 'models' is inherited
        self.assert_('models' in config)
        self.assert_('random_nonexistant_key' not in config)
            
    def test_class_element(self):
        # test a configuration element that is a specified class
        f = os.path.join(self.test_configs, 'database_configuration.xml')
        config = XMLConfiguration(f)
        db_config = config['input_configuration']
        expected_host_name = os.environ.get('MYSQLHOSTNAME','localhost')
        expected_password = os.environ.get('MYSQLPASSWORD','')
        self.assertEqual(db_config.host_name, expected_host_name)
        self.assertEqual(db_config.user_name, 'Fred')
        self.assertEqual(db_config.password, expected_password)
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
if __name__ == '__main__':
    opus_unittest.main()
            
