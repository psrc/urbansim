# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from lxml import etree

from opus_core.tools.converter import * #@UnusedWildImport
from opus_core.tests.opus_unittest import OpusTestCase


class Test_(OpusTestCase):

    def setUp(self):
        self.instance = Converter(quiet=True)
        self.instance.open_xml_file(self._full_path('convert_me.xml'))
        self.root = self.instance.root

    def _full_path(self, filename):
        return os.path.join(os.path.split(__file__)[0], 'test_files', filename)

    def test_tag_name_fix(self):
        node = self.root.find('xml_version')
        self.instance.tag_name_fix(node, 'new_tag')
        self.instance.execute()
        self.assertTrue(self.root.find('new_tag') is not None)
        self.assertEqual(self.root.find('new_tag').get('name'), 'xml_version')

    def test_action_change_node_attrib(self):
        node = self.root.find('general/project_name')
        # add one attribute, change one, and leave one (the 'hidden' argument is left)
        self.instance.action_change_node_attrib(node, {'type': 'changed type', 'guppy': 'puppy'})
        self.assertDictsEqual(dict(node.attrib), {'type': 'changed type', 'guppy': 'puppy', 'hidden': 'True'})

    def test_action_update_version(self):
        version_node = self.root.find('xml_version')
        # set the version if it exists
        self.instance.action_update_version(version_node)
        self.assertTrue(version_node.text == '2.0')
        # create the version if it doesn't exist
        self.root.remove(version_node)
        self.assertTrue(self.root.find('xml_version') is None)
        self.instance.action_update_version(None)
        self.assertEqual(self.root.find('xml_version').text, '2.0')

    def test_set_node_text_and_tag(self):
        node = self.root.find('general/parent')
        text = 'change to text'
        tag = 'change_to_tag'
        self.assertNotEqual(node.text, text)
        self.assertNotEqual(node.tag, tag)
        self.instance.action_change_node_tag(node, tag)
        self.instance.action_change_node_text(node, text)
        self.assertEqual(node.text, text)
        self.assertEqual(node.tag, tag)

    def test_fix_submodel_node(self):
        path = 'model_manager/model_system/residential_land_share_model/specification/regression_submodel'
        submodel_node = self.root.find(path)
        self.instance.action_change_submodel_id(submodel_node)
        self.assertTrue(submodel_node.find('submodel_id') is None)
        self.assertTrue(submodel_node.get('submodel_id') == '-2')

    def test_move_node(self):
        node_to_move = self.root.find('general/project_name')
        path_to_move_to = 'model_manager/model_system'
        self.assertTrue(self.root.find('%s/%s' %(path_to_move_to, 'project_name')) is None)
        self.instance.action_move_node(node_to_move, path_to_move_to)
        self.assertTrue(self.root.find('%s/%s' %(path_to_move_to, 'project_name')) is node_to_move)
        node_to_move_to = self.root.find('results_manager')
        self.instance.action_move_node(node_to_move, node_to_move_to)
        self.assertTrue(node_to_move_to.find('project_name') is node_to_move)
        # move using an extended path
        self.instance.action_move_node(node_to_move, node_to_move_to, 'Simulation_runs')
        self.assertTrue(node_to_move_to.find('Simulation_runs/project_name') is node_to_move)

    def test_convert_selectable_list_node(self):
        node = self.root.find('scenario_manager/Eugene_baseline/models_to_run')
        for selectable_node in node:
            tag_before = selectable_node.tag
            self.instance.action_convert_selectable_list_node(selectable_node)
            self.assertTrue(selectable_node.tag == selectable_node.get('type') == 'selectable')
            self.assertTrue(selectable_node.text in ['True', 'False'])
            self.assertTrue(selectable_node.get('name') == tag_before)
        self.assertEqual(node[0].text, 'True')
        self.assertEqual(node[1].text, 'False')
        self.assertEqual(node[2].text, 'False')

    def test_indicator_batches(self):
        node = self.root.find('results_manager')
        self.instance.check_results_manager_indicator_batches(node)
        self.instance.execute()

        image_viz = node.find("indicator_batches/indicator_batch/batch_visualization[@name='image_viz']")
        table_viz = node.find("indicator_batches/indicator_batch/batch_visualization[@name='table_viz']")
        # make sure that only allowed nodes are outside of settings, and that settings are preserved
        allowed_outside = ['dataset_name', 'output_type', 'indicators', 'visualization_type']
        for node in [image_viz, table_viz]:
            for child_node in node:
                if child_node.tag != 'settings':
                    self.assertTrue(child_node.tag in allowed_outside)
            for setting_node in child_node.findall('settings'):
                self.assertTrue(setting_node.tag == 'setting')

    def test_check_variables_nodes(self):
        test_node_before = self.root.find('model_manager/model_system/residential_land_share_model/specification/regression_submodel/variables')
        self.assertEqual(test_node_before.text.strip(), 'constant,lru,nrs')
        self.instance.check_variables_nodes()
        self.instance.execute()
        test_node_after = self.root.find("model_manager/model_system/residential_land_share_model/specification/regression_submodel/variable_list")
        self.assertTrue(test_node_after is not None)
        self.assertTrue(test_node_after.find("variable_spec[@name='constant']") is not None)
        self.assertTrue(test_node_after.find("variable_spec[@name='.lru']") is not None)
        nrs_node = test_node_after.find("variable_spec[@name='.nrs']")
        self.assertTrue(nrs_node is not None)

        self.assertEqual(len(test_node_after), 3)
        self.assertTrue(test_node_after.text is None)
        print(etree.tostring(test_node_after))



