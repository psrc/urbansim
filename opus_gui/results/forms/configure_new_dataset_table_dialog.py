# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_gui.results.forms.abstract_configure_dataset_table_dialog import AbstractConfigureDatasetTableDialog

class ConfigureNewDatasetTableDialog(AbstractConfigureDatasetTableDialog):
    def __init__(self, resultManagerBase, batch_name):
        AbstractConfigureDatasetTableDialog.__init__(self,resultManagerBase)
    
        self._setup_co_dataset_name()
        self._setup_indicators()
        self._setup_co_viz_type()
        self._setup_co_output_type()
        
        self.batch_name = batch_name
                               
    def on_buttonBox_accepted(self):
        viz_params = self._get_viz_spec()
        viz_name = str(self.leVizName.text()).replace(' ','_')
        
        viz_type = str(self.cboVizType.currentText())
        
        self.xml_helper.addNewVisualizationToBatch(
                            viz_name = viz_name,
                            batch_name = self.batch_name,
                            viz_type = self._get_type_mapper()[viz_type],
                            viz_params = viz_params)
        
        self.close()