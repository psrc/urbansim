# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml import etree

from opus_gui.models_manager.controllers.submodel_editor import * #@UnusedWildImport
from opus_core.tests.opus_gui_unittest import OpusGUITestCase
from opus_gui.tests.mockup_project import MockupOpusProject

class TestSubmodelEditor(OpusGUITestCase):

    def test_name_collision_test(self):
        xml = self.get_data_from_test_files('submodels.xml', __file__)
        p = MockupOpusProject(xml)
        instance = SubModelEditor(p)
        sub1 = p.find('submodel', name='submodel1')
        instance.init_for_submodel_node(sub1)
        instance.le_name.setText('taken name')
        self.assertEqual(instance.validate_submodel_and_accept(), 'name collision')
        instance.le_name.setText('unique name')
        self.assert_(instance.validate_submodel_and_accept() is None)

    def test_get_nested_structure(self):
        xml = self.get_data_from_test_files('nested_structures.xml', __file__)
        p = MockupOpusProject(xml)
        instance = SubModelEditor(p)
        # fetch the nested_structure for a given submodel, convert it from XML to dict and make
        # sure that it is the same as the should_be_dict
        def test_nested_structure(name, should_be_dict):
            submodel_node = p.find('model/specification/submodel', name=name)
            nest_struct_node = instance.update_model_nested_structure(submodel_node)
            if should_be_dict is None:
                self.assertEqual(nest_struct_node, None)
            else:
                node_data = p.xml_config._convert_node_to_data(nest_struct_node)
                print etree.tostring(nest_struct_node)
                self.assertDictsEqual(node_data, should_be_dict)

        should_be_dict = None
        test_nested_structure('no nests', should_be_dict)

        should_be_dict = {42: [5, 10]}
        test_nested_structure('one level nest', should_be_dict)

        should_be_dict = {1: {11: [5, 10], 12: [99, 100]} }
        test_nested_structure('multi level nest', should_be_dict)

        should_be_dict = {77: [1, 2, 3, 4], 33: [5, 6] }
        test_nested_structure('nest with # of samples', should_be_dict)

        submodel_node = p.find('malplaced_submodel')
        self.assertRaises(RuntimeError, instance.update_model_nested_structure, submodel_node)

