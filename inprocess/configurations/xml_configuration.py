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

class XMLConfiguration(Configuration):
    """
    An XMLConfiguration is a kind of configuration that can be stored or loaded from an XML file.
    """
    
    def __init__(self, filename):
        """initialize this configuration from the contents of the xml file named by 'filename' """
        super(XMLConfiguration, self).__init__()
        f = QtCore.QFile(filename)
        is_ok = f.open(QtCore.QIODevice.ReadOnly)
        if not is_ok:
            raise 
        doc = QtXml.QDomDocument()
        doc.setContent(f)
        configNode = doc.documentElement()
        if not configNode.isElement() or configNode.tagName()!='configuration':
            raise ValueError, "malformed xml - expected to find a root element named 'configuration'"
        changes = {}
        node = configNode.firstChild()
        while not node.isNull():
            if node.isElement() and node.toElement().tagName()=='parent':
               self._process_parent(node, filename)
            else:
                self._add_to_dict(node, changes)
            node = node.nextSibling()
        self.merge(changes)
        f.close()
        
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
        tag = children[0].toElement().tagName()
        if tag=='file':
            parentfilename = str(children[0].firstChild().toText().data())
            # dir is the path to the directory containing the xml file named by filename
            # if the parent file name is relative, find it relative to dir (join will ignore
            # dir if the parent file name is absolute)
            dir = os.path.split(os.path.abspath(filename))[0]
            fullpath = os.path.join(dir, parentfilename)
            parent = XMLConfiguration(fullpath)
            self.merge(parent)
        elif tag=='oldconfig':
            path = str(children[0].attributes().namedItem('path').nodeValue())
            class_name = str(children[0].firstChild().toText().data())
            # if the node doesn't have a 'path' attribute, the getAttribute method returns ''
            parent = self._make_instance(class_name, path)
            self.merge(parent)
        else:
            raise ValueError, "ill-formed parent node - expected either 'file' or 'oldconfig'"

    def _add_to_dict(self, node, result_dict):
        # 'node' should be an element node representing a key-value pair to be added to 
        # the dictionary 'result_dict' (unless it's a comment or whitespace)
        if self._is_good_node(node):
            # make the dictionary keys be strings 
            # (later should they be turned into unicode instead??)
            key = str(node.toElement().tagName())
            result_dict[key] = self._convert_node_to_data(self._get_single_child(node))
            
    def _convert_node_to_data(self, node):
        # convert 'node' to the corresponding Python data, and return the data
        if node.isText():
            # the data will be a QString - convert this to a regular Python string
            # (later we might want to make it unicode)
            return str(node.toText().data())
        # if it's not a text node, it needs to be an element
        if not node.isElement():
            raise ValueError, 'malformed xml - expected an element node'
        element = node.toElement()
        # branch on the element's tag to determine the type of the return data
        if element.tagName()=='None':
            return None
        elif element.tagName()=='int':
            return int(node.firstChild().toText().data())
        elif element.tagName()=='float':
            return float(node.firstChild().toText().data())
        elif element.tagName()=='str':
            return str(node.firstChild().toText().data())
        elif element.tagName()=='unicode':
            return unicode(node.firstChild().toText().data())
        elif element.tagName()=='list' or element.tagName()=='tuple':
            n = element.firstChild()
            result_list = []
            while not n.isNull():
                if self._is_good_node(n):
                    result_list.append(self._convert_node_to_data(n))
                n = n.nextSibling()
            if element.tagName()=='tuple':
                return tuple(result_list)
            else:
                return result_list
        elif element.tagName()=='bool':
            b = element.firstChild().toText().data()
            if b=='True':
                return True
            elif b=='False':
                return False
            else:
                raise ValueError, 'malformed xml - expected a string representing a boolean'
        elif element.tagName()=='array':
            # the data should be a string such as '[100, 300]'
            # use eval to turn this into a list, and then turn it into a numpy array
            return array(eval(str(node.firstChild().nodeValue())))
        elif element.tagName()=='dict':
            result_dict = {}
            child = node.firstChild()
            while not child.isNull():
                self._add_to_dict(child, result_dict)
                child = child.nextSibling()
            return result_dict
        elif element.tagName()=='class':
            class_name = str(node.attributes().namedItem('name').nodeValue())
            path = str(node.attributes().namedItem('path').nodeValue())
            keyword_args = {}
            child = node.firstChild()
            while not child.isNull():
                self._add_to_dict(child, keyword_args)
                child = child.nextSibling()
            return self._make_instance(class_name, path, keyword_args)
        else:
            raise ValueError, 'malformed xml - unknown tag name %s' % node.tagName
            
    def _is_good_node(self, node):
        """Return True if this node should be processed, False if this node should be ignored.  
        It should be ignored if it's a comment, just whitespace, or has the attribute selected=False """
        if node.isComment():
            return False
        elif node.isText() and node.toText().data().trimmed().isEmpty():
            return False
        elif node.attributes().namedItem('selected').nodeValue()=='False':
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

import os
from numpy import ma
from opus_core.tests import opus_unittest
class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        inprocessdir = __import__('inprocess').__path__[0]
        self.test_configs = os.path.join(inprocessdir, 'configurations', 'test_configurations')

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
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'strings.xml')
        config = XMLConfiguration(f)
        for k in config.keys():
            self.assert_(type(k) is str)
        self.assert_(type(config['s']) is str)
        self.assert_(type(config['u']) is unicode)

    def test_array(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'array.xml')
        config = XMLConfiguration(f)
        should_be = array([100, 300]) 
        self.assert_(ma.allclose(config['arraytest'], should_be, rtol=1e-6))
        
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
