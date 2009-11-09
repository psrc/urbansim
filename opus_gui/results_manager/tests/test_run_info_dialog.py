# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml import etree
from opus_core.tests.opus_gui_unittest import OpusGUITestCase
from opus_gui.results_manager.controllers.dialogs.get_run_info import GetRunInfo

class TestGetRunInfo(OpusGUITestCase):

    def test_all_values_set(self):
        run_node = etree.fromstring(self.get_data_from_test_files('sample_run.xml', __file__))
        w = GetRunInfo(run_node)
        expected_values = { w.lblRun_name.text: 'sample run node',
                           w.lblYears_run.text: '2000 - 2009',
                           w.lblScenario_name.text: 'sample scenario',
                           w.lblRunId.text: '1',
                           w.lblCache_directory.text: '/sample/path' }
        for func, value in expected_values.items():
            self.assertEqual(str(func()), value)

    def test_changed_dir(self):
        run_node = etree.fromstring(self.get_data_from_test_files('sample_run.xml', __file__))
        w = GetRunInfo(run_node)
        w.on_buttonBox_accepted()
        self.assert_(w.changed_chache_dir is None)
        new_cache_dir = 'this is not the same as the original'
        w.lblCache_directory.setText(new_cache_dir)
        w.on_buttonBox_accepted()
        self.assert_(w.changed_chache_dir == new_cache_dir)