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
            raise IOError, "couldn't process XML file"
        doc = QtXml.QDomDocument()
        doc.setContent(f)
        configNode = doc.documentElement()
        if not configNode.isElement() or configNode.tagName()!='configuration':
            raise ValueError, "malformed xml - expected to find a root element named 'configuration'"
        changes = {}
        node = configNode.firstChild()
        while not node.isNull():
            if self._is_good_node(node):
                e = node.toElement()
                if e.tagName()!='item':
                    raise ValueError, "malformed xml - expected a tag 'item' "
                p = str(e.attributes().namedItem('parser_action').nodeValue())
                if p=='parent':
                    self._process_parent(e, filename)
                elif p=='parent_old_format':
                    self._process_parent_old_format(e, filename)
                else:
                    self._add_to_dict(e, changes)
            node = node.nextSibling()
        self.merge(changes)
        f.close()
        
    def _process_parent(self, node, filename):
        # Process a node specifying the parent configuration defined using  
        # another XML file.
        # This code actually allows multiple parents, which will be merged together with 
        # parents listed later overriding ones listed earlier.  This could be disallowed - 
        # although it might be useful, and doesn't cost anything to support.
        parentfilename = str(node.firstChild().nodeValue())
        # dir is the path to the directory containing the xml file named by filename
        # if the parent file name is relative, find it relative to dir (join will ignore
        # dir if the parent file name is absolute)
        dir = os.path.split(os.path.abspath(filename))[0]
        fullpath = os.path.join(dir, parentfilename)
        parent = XMLConfiguration(fullpath)
        self.merge(parent)

    def _process_parent_old_format(self, node, filename):
        # Process a node specifying the parent configuration defined using  
        # n old-style configuration.  (This is a 
        # backward compatibility hack, and should be eventually removed.)
        d = self._convert_node_to_data(node)
        parent = self._make_instance(d['Class name'], d['Class path'])
        self.merge(parent)

    def _add_to_dict(self, node, result_dict):
        # 'node' should be an element node representing a key-value pair to be added to 
        # the dictionary 'result_dict' (unless it's a comment or whitespace)
        if self._is_good_node(node):
            # make the dictionary keys be strings 
            # (later should they be turned into unicode instead??)
            key = str(node.attributes().namedItem('name').nodeValue())
            result_dict[key] = self._convert_node_to_data(node)
            
    def _convert_node_to_data(self, node):
        # branch on the node's type attribute to determine the type of the return data
        type_name = str(node.attributes().namedItem('type').nodeValue())
        if type_name=='None':
            return None
        elif type_name=='integer':
            return int(node.firstChild().nodeValue())
        elif type_name=='float':
            return float(node.firstChild().nodeValue())
        elif type_name=='string':
            return str(node.firstChild().nodeValue())
        elif type_name=='password':
            return str(node.firstChild().nodeValue())
        elif type_name=='unicode':
            return unicode(node.firstChild().nodeValue())
        elif type_name=='list' or type_name=='tuple':
            n = node.firstChild()
            result_list = []
            while not n.isNull():
                if self._is_good_node(n):
                    result_list.append(self._convert_node_to_data(n))
                n = n.nextSibling()
            if type_name=='tuple':
                return tuple(result_list)
            else:
                return result_list
        elif type_name=='boolean':
            b = node.firstChild().nodeValue()
            if b=='True':
                return True
            elif b=='False':
                return False
            else:
                raise ValueError, 'malformed xml - expected a string representing a boolean'
        elif type_name=='array':
            # the data should be a string such as '[100, 300]'
            # use eval to turn this into a list, and then turn it into a numpy array
            s = str(node.firstChild().nodeValue()).strip()
            return array(eval(s))
        elif type_name=='dictionary':
            result_dict = {}
            child = node.firstChild()
            while not child.isNull():
                self._add_to_dict(child, result_dict)
                child = child.nextSibling()
            return result_dict
        elif type_name=='class':
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
            return self._make_instance(class_name, class_path, items)
        elif type_name=='model':
            modelname = str(node.attributes().namedItem('name').nodeValue())
            # if no children, the item name is the value; otherwise return a dictionary
            if node.hasChildNodes():
                subdict = {}
                child = node.firstChild()
                while not child.isNull():
                    self._add_to_dict(child, subdict)
                    child = child.nextSibling()
                return {modelname: subdict}
            else:
                return modelname
        else:
            raise ValueError, 'unknown type: %s' % type_name
            
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
                          'list_test': ['squid', 'clam', u'uniclam'],
                          'dicttest': {'str1': 'squid', 'str2': 'clam'},
                          'models': ['model1', 
                                     {'model2': {'group_members': 'all'}}, 
                                     {'model3': {'chooser': 'random', 'sampler': 'fussy'}}],
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
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')
            
    def test_error_handling(self):
        self.assertRaises(IOError, XMLConfiguration, 'badname.xml')
        f = os.path.join(self.test_configs, 'badconfig.xml')
        self.assertRaises(ValueError, XMLConfiguration, f)

if __name__ == '__main__':
    opus_unittest.main()
