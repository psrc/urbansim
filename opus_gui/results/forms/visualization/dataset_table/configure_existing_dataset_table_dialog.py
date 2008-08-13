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
from PyQt4.QtCore import QString, QObject, SIGNAL, QRegExp, QSize, Qt, QVariant
from PyQt4.QtGui import QDialog, QVBoxLayout, QFrame, QWidget, QHBoxLayout, QLabel, QPalette, QLineEdit

from opus_gui.results.forms.visualization.dataset_table.abstract_configure_dataset_table_dialog import AbstractConfigureDatasetTableDialog
from opus_gui.results.xml_helper_methods import get_child_values, ResultsManagerXMLHelper

class ConfigureExistingDatasetTableDialog(AbstractConfigureDatasetTableDialog):
    def __init__(self, resultManagerBase, selected_index):
        AbstractConfigureDatasetTableDialog.__init__(self,resultManagerBase)
        
        self.selected_index = selected_index
        
        base_node = selected_index.internalPointer().node()
        cur_vals = get_child_values(
                        parent = base_node,
                        all = True)
#                        child_names = ['dataset_name','indicators', 'output_type'])
        
        self.leVizName.setText(base_node.nodeName())
        
        prev_dataset = str(cur_vals['dataset_name'])
        prev_indicators = self._process_xml_stored_list_of_strings(value = cur_vals['indicators'])
        prev_output_type = str(cur_vals['output_type'])
            
        self._setup_co_dataset_name(value = prev_dataset)
        self._setup_indicators(existing_indicators = prev_indicators)
        self._setup_co_output_type(value = prev_output_type)

        fixed_field_specification = None
        if prev_output_type == 'fixed_field':
            fixed_field_specification = cur_vals['fixed_field_specification']
            id_format = cur_vals['id_format']
            specs = self._process_xml_stored_list_of_strings(value = fixed_field_specification)
            self._set_column(column = 1, values = specs)
            self.leOption1.setText(QString(id_format))
        elif prev_output_type == 'esri':
            storage_location = cur_vals['storage_location']
            self.leOption1.setText(QString(storage_location))
        elif prev_output_type == 'sql':
            database_name = cur_vals['database_name']
            self.leOption1.setText(QString(database_name))

            
    def _process_xml_stored_list_of_strings(self, value):
        list_str = str(value)[1:-1]
        lst = [i.strip()[1:-1] for i in list_str.split(',')]   
        return lst     
        
    def on_buttonBox_accepted(self):    
        viz_params = self._get_viz_spec(convert_to_node_dictionary = False)
        viz_name = str(self.leVizName.text()).replace('DATASET',viz_params['dataset_name']).replace(' ','_')
        
        xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxStuff)
        xml_helper.update_dom_node(index = self.selected_index, 
                                   new_base_node_name = viz_name, 
                                   children_to_update = viz_params)
            
        self.close()

    def on_buttonBox_rejected(self):
        self.close()