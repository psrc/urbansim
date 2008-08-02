# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QDialog


from opus_gui.results.forms.get_run_info_ui import Ui_dlgGetRunInfo
from opus_gui.results.xml_helper_methods import get_child_values

class GetRunInfo(QDialog, Ui_dlgGetRunInfo):
    def __init__(self, opusxmlaction, selected_index):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        QDialog.__init__(self, opusxmlaction.mainwindow, flags)
        self.setupUi(self)
        self.selected_index = selected_index
        #fill in existing values...
        if self.selected_index is not None:
            base_node = self.selected_index.internalPointer().node()
            cur_vals = get_child_values(parent = base_node,
                                        child_names = ['run_name','end_year',
                                                       'start_year', 'cache_directory',
                                                       'scenario_name', 'run_id'])
            
            self.lblRun_name.setText(cur_vals['run_name'])
            self.lblYears_run.setText(
                  QString('%s - %s'%(str(cur_vals['start_year']),str(cur_vals['end_year']))))
            self.lblScenario_name.setText(cur_vals['scenario_name'])
            self.lblCache_directory.setText(cur_vals['cache_directory'])
            if 'run_id' in cur_vals:
                self.lblRunId.setText(cur_vals['run_id'])
        
    def on_btnDone_released(self):
        self.close()
