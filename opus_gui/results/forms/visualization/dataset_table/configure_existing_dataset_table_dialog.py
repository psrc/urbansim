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
from PyQt4.QtCore import QString, QObject, SIGNAL, QRegExp, QSize, Qt, QVariant
from PyQt4.QtGui import QDialog, QVBoxLayout, QFrame, QWidget, QHBoxLayout, QLabel, QPalette, QLineEdit

from opus_gui.results.forms.visualization.dataset_table.abstract_configure_dataset_table_dialog import AbstractConfigureDatasetTableDialog
from opus_gui.results.xml_helper_methods import get_child_values

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
        
        prev_dataset = cur_vals['dataset_name']
        prev_indicators = self._process_xml_stored_list_of_strings(value = cur_vals['indicators'])
        prev_output_type = cur_vals['output_type']

        fixed_field_specification = None
        if 'fixed_field_specification' in cur_vals:
            fixed_field_specification = cur_vals['fixed_field_specification']

        self._setup_co_dataset_name(value = prev_dataset)
        self._setup_indicators(existing_indicators = prev_indicators)
        self._setup_co_output_type(value = str(prev_output_type))
        
        if fixed_field_specification is not None:
            specs = self._process_xml_stored_list_of_strings(value = fixed_field_specification)
            self._set_column(column = 1, values = specs)
            
    def _process_xml_stored_list_of_strings(self, value):
        list_str = str(value)[1:-1]
        lst = [i.strip()[1:-1] for i in list_str.split(',')]   
        return lst     
        
    def on_buttonBox_accepted(self):
        dataset_name = self.cboDataset.currentText()        
        viz_name = str(self.leVizName.text()).replace('DATASET',dataset_name).replace(' ','_')
        output_type = self.cboOutputType.currentText()
        indicators = self._get_column_values(column = 0)
        
        viz_name = QVariant(viz_name)
        output_type = QVariant(output_type)
        indicators = QVariant(str(indicators))
        dataset_name = QVariant(dataset_name)
        
        self.model.setData(self.selected_index,viz_name,Qt.EditRole)
        
        vals = {
                'indicators': indicators,
                'output_type': output_type,
                'dataset_name': dataset_name
        }
        base_node = self.selected_index.internalPointer().node()

        node = base_node.firstChild()        
        row = 0
        while not node.isNull():
            name = str(node.nodeName())
            if name in vals:
                index = self.model.index(row, 1, self.selected_index)
                self.model.setData(index, vals[name],Qt.EditRole)
            node = node.nextSibling()
            row += 1
            
        self.close()

    def on_buttonBox_rejected(self):
        self.close()