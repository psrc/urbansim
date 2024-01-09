# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#IGNORE_THIS_FILE

import os
# from xml.etree.cElementTree import ElementTree
from lxml.etree import ElementTree

from PyQt5.QtWidgets import * #@UnusedWildImport
from PyQt5.QtCore import * #@UnusedWildImport

from opus_core.tests import opus_unittest
from opus_gui.abstract_manager.models.xml_model import XmlModel

class TestXmlModel(opus_unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.testdatapath = os.path.split(__file__)[0]
        self.testdatapath = os.path.join(self.testdatapath, 'testdata')
        manager_xml_file = os.path.join(self.testdatapath, 'model_manager.xml')
        self.xml = ElementTree(file=manager_xml_file).getroot()
        self.instance = XmlModel(self.xml)

    def skip_test_iconFromType(self):
        # just test some of the icons
        expected_results = {
            'dir_path': self.instance.folderIcon,
            'path': self.instance.folderDatabaseIcon,
            '-- NOT IN DICT --.': QVariant(),
            'defValue': QVariant()
            }

        for key, value in list(expected_results.items()):
            self.assertEqual(self.instance.iconFromType(key), value)

    def test_columnCount(self):
        self.assertEqual(self.instance.columnCount(None), len(self.instance._headers))

    def test_rebuild_tree(self):
        pass

    def test_index_and_parent(self):
        idx_child1 = self.instance.index(0, 0, QModelIndex())
        idx_child2 = self.instance.index(1, 0, QModelIndex())
        idx_child21 = self.instance.index(0, 0, idx_child2)

        node_child1 = self.instance.root_node().find('child_1')
        node_child2 = self.instance.root_node().find('child_2')
        node_child21 = self.instance.root_node().find('child_2/child_21')

        # Make sure the nodes are actually there
        self.assertFalse(node_child1 is None)
        self.assertFalse(node_child2 is None)
        self.assertFalse(node_child21 is None)

        # Check to see if the indexes contain the actual nodes
        self.assertTrue(idx_child1.internalPointer().node is node_child1)
        self.assertTrue(idx_child21.internalPointer().node is node_child21)

        # Check parent lookups
        self.assertEqual(self.instance.parent(idx_child21), idx_child2)
        self.assertEqual(self.instance.parent(idx_child2), QModelIndex())
        self.assertNotEqual(self.instance.parent(idx_child21),
                            self.instance.parent(idx_child2))

    def test_data(self):
        # test that the tag name is returned as display
        # test that the correct icon is returned for the types
        # test that QVariant() is returned for bogus values
        idx_child1 = self.instance.index(0, 1, QModelIndex())
        idx_child2 = self.instance.index(1, 0, QModelIndex())
        idx_child21 = self.instance.index(0, 0, idx_child2)
        idx_child21_value = self.instance.index(0, 1, idx_child2)

        node_child2 = self.instance.root_node().find('child_2')
        node_child21 = self.instance.root_node().find('child_2/child_21')

        self.assertEqual(str(self.instance.data(idx_child1, Qt.DisplayRole).value()),
                         '*********') # password values should be secret

        self.assertEqual(str(self.instance.data(idx_child2, Qt.DisplayRole).value()),
                 node_child2.tag)

        self.assertTrue(node_child21.text is not None)
        self.assertEqual(str(self.instance.data(idx_child21_value, Qt.DisplayRole).value()),
                 node_child21.text.strip())

        self.assertTrue(self.instance.data(idx_child21, Qt.DecorationRole) is not None)
        #self.assertEqual(self.instance.data(idx_child21, Qt.DecorationRole),
        #                 QVariant(self.instance.iconFromType(node_child21.get('type'))))

    def test_rowCount(self):
        idx_child1 = self.instance.index(0, 1, QModelIndex())
        idx_child2 = self.instance.index(1, 0, QModelIndex())

        self.assertEqual(self.instance.rowCount(QModelIndex()), 2)
        self.assertEqual(self.instance.rowCount(idx_child2), 1)
        self.assertEqual(self.instance.rowCount(idx_child1), 0)

    def test_remove_node(self):
        pass

    def test_removeRow(self):
        pass

    def test_index_for_item(self):
        pass

    def test_update_node(self):
        pass

    def test_item_for_node(self):
        pass

    def test_index_for_node(self):
        pass

    def test_add_node(self):
        pass

    def test_insert_node(self):
        pass

    def test_index(self):
        pass

    def test_make_item_local(self):
        pass

    def test_insertRow(self):
        pass

    def test_insert_sibling(self):
        pass

    def test_move_up(self):
        pass

    def test_move_down(self):
        pass

    def test_root_node(self):
        self.assertTrue(self.instance.root_node() is self.instance._root_node and
                        self.instance._root_node is not None)

    def test_root_item(self):
        self.assertTrue(self.instance.root_item() is self.instance._root_item and
                        self.instance._root_item is not None)

if __name__ == '__main__':
    print('Running test')
    opus_unittest.main()
