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

from PyQt4.QtGui import QDialog, QMenu, QCursor
from PyQt4.QtCore import Qt, SIGNAL

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.general_manager.models.variables_table_model import \
    variable_to_validator_format, create_empty_variable

from opus_gui.general_manager.views.ui_variable_editor import Ui_VariableEditor

from opus_core.variables.variable_name import VariableName

class VariableEditor(QDialog, Ui_VariableEditor):

    def __init__(self, variable, validator, callback = None, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.original_variable = variable # keep a reference to the orig obj
        self.variable = variable.copy() # don't manipulate the original object
        self.validator = validator
        self.callback = callback
        # Copy variable values into fields
        self.leVarName.setText(variable['name'])
        index = self.cboVarType.findText(variable['source'])

        if index < 0:
            msg = ('Variable "%s" has an unknown type value (%s).' %
                   (variable['name'], variable['source']))
            raise RuntimeError(msg)

        self.cboVarType.setCurrentIndex(index)

        if variable['use'] == 'model variable':
            self.rbUseModel.setChecked(True)
        elif variable['use'] == 'indicator':
            self.rbUseIndicator.setChecked(True)
        else:
            self.rbUseBoth.setChecked(True)
        self.txtVarDef.setText(variable['definition'])
        self.leVarName.selectAll()
        self.leVarName.setFocus()

    def _update_variable_from_fields(self):
        ''' update the variable with values from the gui widgets '''
        self.variable['name'] = str(self.leVarName.text())
        self.variable['source'] = str(self.cboVarType.currentText())
        self.variable['definition'] = str(self.txtVarDef.document().toPlainText())
        if self.rbUseModel.isChecked():
            self.variable['use'] = 'model variable'
        elif self.rbUseIndicator.isChecked():
            self.variable['use'] = 'indicator'
        else:
            self.variable['use'] = 'both'

    def on_buttonBox_accepted(self):
        ''' event handler for when user clicks OK '''
        self._update_variable_from_fields()
        if self.callback:
            self.callback(self.variable, self.original_variable)
        self.close()

    def on_buttonBox_rejected(self):
        ''' event handler for when the user rejects the dialog '''
        self.close()

