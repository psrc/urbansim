# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.models_manager.controllers.dialogs.dynamic_template_dialog import * #@UnusedWildImport
from opus_core.tests.opus_gui_unittest import OpusGUITestCase
from opus_gui.tests.mockup_project import MockupOpusProject

class TestDynamicTemplateDialog(OpusGUITestCase):

    def setUp(self):
        xml = self.get_data_from_test_files('dynamic_templates.xml', __file__)
        project = MockupOpusProject(xml)
        self.instance = DynamicTemplateDialog(project.find('model_template'), project)

    def test_map_fields_to_nodes(self):
        # A and D are 'orange fields'
        # B is 'apple field'
        root = self.instance.project.root_node()
        a_node = root.find('model_template/A')
        d_node = root.find('model_template/C/buried/deep/inside/D')
        b_node = root.find('model_template/B')
        e_node = root.find('model_template/E')
        should_be = {'orange field': [a_node.tag, d_node.tag],
                     'apple field': [b_node.tag,],
                     'use checkbox?': [e_node.tag,]}
        node_tag_dict = {}
        for field_id, node_list in self.instance.fields_to_nodes.items():
            node_tag_dict[field_id] = [node.tag for node in node_list]
        self.assertDictsEqual(node_tag_dict, should_be)

    def test_generate_widgets(self):
        self.assertEqual(len(self.instance.widgets), 3)

        lbl_orange, generated_orange, _ = self.instance.widgets[0]
        lbl_apple, generated_apple, apple_desc = self.instance.widgets[1]
        lbl_checkbox, generated_checkbox, _ = self.instance.widgets[2]
        # check that the labels got the correct text
        self.assertEqual(lbl_orange.text(), 'orange field')
        self.assertEqual(lbl_apple.text(), 'apple field')
        self.assertEqual(lbl_checkbox.text(), 'use checkbox?')
        # the tooltip of the description should get the correct formatting
        self.assertEqual(apple_desc.toolTip(), '<qt><b>apple field</b><br/>Apples are red</qt>')
        # check that the correct widget types was generated
        self.assertTrue(isinstance(generated_orange, QtGui.QLineEdit))
        self.assertTrue(isinstance(generated_apple, QtGui.QSpinBox))
        self.assertTrue(isinstance(generated_checkbox, QtGui.QCheckBox))
        # check that the field methods return the correct values
        self.assertEqual(self.instance.fields_to_data_methods['orange field'](), 'mandarin')
        self.assertEqual(self.instance.fields_to_data_methods['apple field'](), '42')
        # no default value should mean unchecked
        self.assertEqual(self.instance.fields_to_data_methods['use checkbox?'](), 'False')

        # change all widgets values
        self.instance.widgets[0][1].setText('clementine')
        self.instance.widgets[1][1].setValue(4000)
        self.instance.widgets[2][1].setChecked(True)

        # check that the field methods return the correctly changed values
        self.assertEqual(self.instance.fields_to_data_methods['orange field'](), 'clementine')
        self.assertEqual(self.instance.fields_to_data_methods['apple field'](), '4000')
        self.assertEqual(self.instance.fields_to_data_methods['use checkbox?'](), 'True')

    def test_apply_data_methods(self):
        # change all widgets values
        self.instance.widgets[0][1].setText('clementine')
        self.instance.widgets[1][1].setValue(4000)
        self.instance.widgets[2][1].setChecked(True)

        self.instance._apply_data_methods()

        # make sure that the values of the node after applying them are the changed ones fetched
        # from the widgets
        node = self.instance.model_node
        self.assertEqual(node.find('A').text, 'clementine')
        self.assertEqual(node.find('B').text, '4000')
        self.assertEqual(node.find('C/buried/deep/inside/D').text, 'clementine')
        self.assertEqual(node.find('E').text, 'True')

    def test_validate_name(self):
        name_ok = 'unique'
        name_taken = 'taken'
        name_to_short = 'bo'
        self.instance.le_model_name.setText(name_ok)
        self.assertEqual(self.instance._get_valid_model_name(), name_ok)

        self.instance.le_model_name.setText(name_taken)
        self.assertRaises(ValueError, self.instance._get_valid_model_name)

        self.instance.le_model_name.setText(name_to_short)
        self.assertRaises(ValueError, self.instance._get_valid_model_name)

