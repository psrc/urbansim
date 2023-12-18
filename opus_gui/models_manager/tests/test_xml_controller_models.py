# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from lxml import etree

from opus_core.configurations.xml_configuration import XMLConfiguration
import opus_gui.models_manager.controllers.xml_configuration.xml_controller_models as xcm
from opus_core.tests.opus_gui_unittest import OpusGUITestCase
from opus_gui.tests.mockup_manager import MockupManager
from opus_gui.tests.mockup_project import MockupOpusProject

class TestXmlControllerModels(OpusGUITestCase):

    def test_update_submodel(self):
        filename = os.path.join(self.get_test_data_dir(__file__), 'model_child.xml')
        p = MockupOpusProject()
        p.open(filename)
        xml = etree.tostring(p._root_node)
        manager = MockupManager(xml='', manager_node_path='model_manager', opus_project=p)
        controller = xcm.XmlController_Models(manager)

        local_node = p.find('model_manager/model/submodel', name='local node')
        shadowing_node = p.find('model_manager/model/submodel', name='shadow node')

        self.assertTrue(local_node is not None)
        self.assertTrue(shadowing_node is not None)

        # created an edited version of local node
        edited_node = etree.Element('submodel', {'name': 'edited local node'})
        vlist_node = etree.SubElement(edited_node, 'variable_list', {'type': 'variable_list'})
        variable_spec_node = etree.SubElement(vlist_node, 'variable_spec', {'name': '.edited_var'})

        controller._update_submodel(local_node, edited_node)
        # the decription should be gone and the variables and named should have changed
        self.assertTrue(local_node.find('description') is None)
        self.assertEqual(local_node.find('variable_list/variable_spec').get('name'), '.edited_var')
        self.assertEqual(local_node.get('name'), 'edited local node')
        # make sure no new nodes was added
        self.assertEqual(len(p.findall('model_manager/model/submodel')), 3)

        # renaming a shadowing node should insert a new local copy and reinsert the shadowed node
        self.assertTrue(shadowing_node.get('inherited') is None)
        edited_node.set('name', 'new copy')
        controller._update_submodel(shadowing_node, edited_node)
        shadowing_node = p.find('model_manager/model/submodel', name='shadow node')
        self.assertTrue(shadowing_node.get('inherited') is not None) # this should now be inherited
        new_copy_node = p.find('model_manager/model/submodel', name='new copy')
        self.assertTrue(new_copy_node is not None)
        # make sure only one node was added
        self.assertEqual(len(p.findall('model_manager/model/submodel')), 4)

    def test_remove_variables_from_specification(self):
        filename = os.path.join(self.get_test_data_dir(__file__), 'model_child2.xml')
        p = MockupOpusProject()
        p.open(filename)
        xml = etree.tostring(p._root_node)
        manager = MockupManager(xml='', manager_node_path='model_manager', opus_project=p)
        controller = xcm.XmlController_Models(manager)
        shadowing_node = p.find('model_manager/model/submodel', name='shadow node')
        self.assertTrue(shadowing_node.get('inherit_parent_values') == 'False')
        self.assertEqual(len(shadowing_node.findall('variable_list/variable_spec')), 1)
 
#from opus_core.tests import opus_unittest
#if __name__ == "__main__":
#    opus_unittest.main()