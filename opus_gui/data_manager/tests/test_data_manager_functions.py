# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.data_manager.data_manager_functions import * #@UnusedWildImport
from opus_core.tests.opus_gui_unittest import OpusGUITestCase
from opus_gui.tests.mockup_project import MockupOpusProject
import os

class TestDataManagerFunctions(OpusGUITestCase):

    def test_get_tool_nodes(self):
        xml = self.get_data_from_test_files('tool_nodes.xml', __file__)
        project = MockupOpusProject(xml)
        lib_node = get_tool_library_node(project)
        self.assertTrue(lib_node is not None)
        self.assertEqual(lib_node.tag, 'tool_library')
        tool_nodes = get_tool_nodes(project)
        names_should_be = set(['a tool', 'another tool', 'a third tool'])
        names_are = set([tool_node.get('name') for tool_node in tool_nodes])
        self.assertEqual(names_are, names_should_be)

    def test_get_tool_node_by_name(self):
        xml = self.get_data_from_test_files('tool_nodes.xml', __file__)
        project = MockupOpusProject(xml)
        another_tool = get_tool_node_by_name(project, 'another tool')
        another_tool_node = project.find("data_manager/tool_library/tool_group/tool[@name='another tool']")
        no_tool = get_tool_node_by_name(project, 'no tool')
        self.assertEqual(another_tool_node.find('class_module').text, 'correct_tool')
        self.assertEqual(another_tool, another_tool_node)
        self.assertTrue(no_tool is None)

    def test_get_tool_library_node(self):
        xml = self.get_data_from_test_files('tool_nodes.xml', __file__)
        project = MockupOpusProject(xml)
        lib_node = get_tool_library_node(project)
        self.assertTrue(lib_node is not None)
        self.assertEqual(lib_node.tag, 'tool_library')

        project = MockupOpusProject('<opus_project />')
        lib_node = get_tool_library_node(project)
        self.assertTrue(lib_node is None)

