# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.tests import opus_unittest

from opus_gui.main.opus_project import OpusProject

from opus_gui.main.controllers.dialogs.new_project_dialog_functions import *

class TestNewProjectDialogFunctions(opus_unittest.OpusTestCase):

    def setUp(self):
        # Validate that the test data is present
        self.testdatapath = os.path.split(__file__)[0]
        self.testdatapath = os.path.join(self.testdatapath, 'testdata')


    def _open(self, fn):
        fn = os.path.join(self.testdatapath, fn)
        p = OpusProject()
        ok, msg = p.open(fn)
        if not ok:
            print msg
        self.assertTrue(p.is_open(), 'Project file could not be opened')
        return p


    def test_merge_templated_nodes_with_project(self):
        ''' 
        Test that merging in templated nodes from a parent project into a new project creates the correct
        node paths with the correct values
        '''
        new_project = self._open('new_project_dialog_thin.xml')
        parent_project = self._open('new_project_dialog_based_on.xml')
        
        templated_nodes = parent_project.get_template_nodes()
        
        # pull in the templated nodes (by name in this case) from the parent so we can change their values
        single_level_node = [node for node in templated_nodes if 
                             node.get('field_identifier') == 'template_single_level'][0]
                             
        multi_level_node = [node for node in templated_nodes if 
                            node.get('field_identifier') == 'template_multi_level'][0]
        
        customized_value = 'value from new project'
        
        single_level_node.text = customized_value
        multi_level_node.text = customized_value
        
        # merge the templated nodes with their updated values into the new project
        merge_templated_nodes_with_project(templated_nodes, new_project)

        # validate that the expected nodes are in the new project
        self.assert_(new_project.find('single_level') is not None)
        self.assert_(new_project.find('multi_level_1/multi_level_2/multi_level_3') is not None)
        
        # check that the parent nodes that should have been left in the parent are left there
        self.assert_(new_project.find('multi_level_1/multi_level_2/multi_level_3/multi_level_4') is None)
        self.assert_(new_project.find('parent_exclusive') is None)
        
        # check that the values have been overwritten by our modified values
        self.assertEqual(new_project.find('single_level').text, customized_value)
        self.assertEqual(new_project.find('multi_level_1/multi_level_2/multi_level_3').text, customized_value)
        
        # TODO test merging nodes at multiple places in the same hierarcy
        
