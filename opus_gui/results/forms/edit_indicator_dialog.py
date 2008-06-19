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


from opus_gui.results.forms.edit_indicator_ui import Ui_dlgEditIndicator
from opus_gui.results.xml_helper_methods import get_child_values, ResultsManagerXMLHelper

class EditIndicatorDialog(QDialog, Ui_dlgEditIndicator):
    def __init__(self, resultManagerBase, selected_index, flags):
        QDialog.__init__(self, resultManagerBase.mainwindow, flags)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.model = resultManagerBase.toolboxStuff.resultsManagerTree.model
        self.selected_index = selected_index
        #fill in existing values...
        if self.selected_index is not None:
            base_node = self.selected_index.internalPointer().node()
            cur_vals = get_child_values(parent = base_node,
                                        child_names = ['package','expression'])
            self.txtIndicator_name.setText(base_node.nodeName())
            self.txtPackage_name.setText(cur_vals['package'])
            self.txtExpression.setText(cur_vals['expression'])
    
        
    def on_buttonBox_accepted(self):
        indicator_name = self.txtIndicator_name.text()
        package_name = self.txtPackage_name.text()
        expression = self.txtExpression.text()
        
        if self.selected_index is not None:
            indicator_name = QVariant(indicator_name)
            package_name = QVariant(package_name)
            expression = QVariant(expression)
            
            self.model.setData(self.selected_index,indicator_name,Qt.EditRole)
            
            vals = {
                    'package': package_name,
                    'expression': expression
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
        else:
            xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxStuff)
            xml_helper.addNewIndicator(indicator_name = indicator_name, 
                                       package_name = package_name, 
                                       expression = expression)
            
        self.close()

    def on_buttonBox_rejected(self):
        self.close()

