# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QDialog
from opus_gui.results_manager.views.ui_get_run_info import Ui_dlgGetRunInfo

class GetRunInfo(QDialog, Ui_dlgGetRunInfo):
    def __init__(self, run_node, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.run_node = run_node
        self.changed_chache_dir = None

        #fill in existing values...
        run_name = run_node.get('name')
        start_year = run_node.find('start_year').text
        end_year = run_node.find('end_year').text
        scenario_name = run_node.find('scenario_name').text
        cache_directory = run_node.find('cache_directory').text
        self.original_cache_dir = cache_directory.strip()
        run_id = run_node.get('run_id', 'not available')

        self.lblRun_name.setText(run_name)
        self.lblYears_run.setText('%s - %s' % (start_year, end_year))

        if scenario_name is None:
            scenario_name = ''
        self.lblScenario_name.setText(scenario_name)
        self.lblCache_directory.setText(cache_directory)
        self.lblRunId.setText(run_id)
        
    def on_tb_select_cachedir_released(self):
        pass
        

    def on_buttonBox_accepted(self):
        cur_cache_dir = str(self.lblCache_directory.text()).strip()
        if self.original_cache_dir != cur_cache_dir:
            # user has changed the cache directory
            self.changed_chache_dir = cur_cache_dir
        self.accept()

    def on_buttonBox_rejected(self):
        self.reject()

