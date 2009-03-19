# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE



##IGNORE_THIS_FILE
#
#from opus_core.tests import opus_unittest
#from PyQt4.QtCore import QString
#from PyQt4.QtGui import QApplication
#from PyQt4.QtXml import QDomDocument
#from opus_gui.main.controllers.mainwindow import OpusGui
#
#class ResultsManagerXMLHelperTests(opus_unittest.OpusTestCase):
#    modul = "opus_gui"
#
#    def setUp(self):
#        self.app = QApplication([])
#        self.mainwindow = OpusGui()
#        self.helper = ResultsManagerXMLHelper(self.mainwindow.toolboxBase)
#        self.doc = QDomDocument()
#
#    def test_set_text_child_value(self):
#        test_xml = '''
#          <no_leaf copyable="True" type="dictionary" >
#            <leaf_trunc hidden="True" type="dictionary" />
#            <leaf_empty_string hidden="True" type="dictionary" >
#            </leaf_empty_string>
#            <leaf_with_text>_template_text_string_</leaf_with_text>
#          </no_leaf>
#        '''
#        self.doc.setContent(test_xml)
#        no_leaf = self.doc.elementsByTagName(QString('no_leaf')).item(0)
#        self.assertFalse(no_leaf is None or no_leaf.isNull())
#
#        leaf_trunc = no_leaf.firstChildElement('leaf_trunc')
#        leaf_empty_string = no_leaf.firstChildElement('leaf_empty_string')
#        leaf_with_text = no_leaf.firstChildElement('leaf_with_text')
#
#        self.assertFalse(leaf_trunc.isNull())
#        self.assertFalse(leaf_empty_string.isNull())
#        self.assertFalse(leaf_with_text.isNull())
#
#        text = 'some text value'
#        self.helper.set_text_child_value(leaf_with_text, text)
#        self.helper.set_text_child_value(leaf_empty_string, text)
#        self.helper.set_text_child_value(leaf_trunc, text)
#
#        self.assertTrue(leaf_with_text.firstChild().nodeValue() == text)
#        self.assertTrue(leaf_empty_string.firstChild().nodeValue() == text)
#        self.assertTrue(leaf_trunc.firstChild().nodeValue() == text)
#
#        self.assertRaises(ValueError, self.helper.set_text_child_value, no_leaf, text)
#
#    def test_get_sub_element_by_path(self):
#        test_xml = '''
#          <root copyable="True" type="dictionary" >
#            <child_filler/>
#            <child>
#              <subchild>
#                <leaf/>
#              </subchild>
#            </child>
#          </root>
#        '''
#        self.doc.setContent(test_xml)
#
#        root = self.doc.firstChildElement('root')
#        leaf = root.firstChildElement('child').firstChildElement('subchild').firstChildElement('leaf')
#
#        self.assertFalse(root.isNull())
#        self.assertFalse(leaf.isNull())
#
#        # empty path returns root
#        self.assertTrue(self.helper.get_sub_element_by_path(root, '/') == root)
#        # invalid path returns null node
#        self.assertTrue(self.helper.get_sub_element_by_path(root, '/some/invalid/path').isNull())
#        # correct path returns correct node
#        self.assertTrue(self.helper.get_sub_element_by_path(root, '/child/subchild/leaf') == leaf)
#        # correctly handle leading and trailing slashes
#        element_wo_slashes = self.helper.get_sub_element_by_path(root, 'child/subchild/leaf')
#        element_w_leading_slash = self.helper.get_sub_element_by_path(root, '/child/subchild/leaf')
#        element_w_trailing_slash = self.helper.get_sub_element_by_path(root, '/child/subchild/leaf/')
#        self.assertFalse(element_w_leading_slash.isNull())
#        self.assertTrue(element_w_leading_slash == element_w_trailing_slash == element_wo_slashes)
#
#if __name__ == '__main__':
#    opus_unittest.main()
