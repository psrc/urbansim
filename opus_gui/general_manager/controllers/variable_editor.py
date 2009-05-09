# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QDialog, qApp
from PyQt4.QtCore import SIGNAL, QEventLoop

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.general_manager.models.variables_table_model import batch_check_syntax
from opus_gui.general_manager.models.variables_table_model import batch_check_data

# Change to ui_variable_editor_alternative for alternative editor
from opus_gui.general_manager.views.ui_variable_editor import Ui_VariableEditor
from opus_core.variables.variable_name import VariableName
from opus_gui.util.icon_library import IconLibrary

class VariableEditor(QDialog, Ui_VariableEditor):

    def __init__(self, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.original_variable = None
        self.variable = None
        self.validator = None
        self.callback = None
        def check_data(): self.check_variable(check = 'data')
        def check_syntax(): self.check_variable(check = 'syntax')
        self.connect(self.btnCheckData, SIGNAL('released()'), check_data)
        self.connect(self.btnCheckSyntax, SIGNAL('released()'), check_syntax)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

        # self.pb_change.setIcon(IconLibrary.icon('arrow_right'))
        self.group_settings.setVisible(False)
        self._toggle_settings()
        self.layout().update()
        qApp.processEvents(QEventLoop.AllEvents)

        # give instant feedback in the information label when settings are changed
        self.connect(self.rbUseBoth, SIGNAL('clicked()'), self._update_variable_info)
        self.connect(self.rbUseIndicator, SIGNAL('clicked()'), self._update_variable_info)
        self.connect(self.rbUseModel, SIGNAL('clicked()'), self._update_variable_info)
        self.connect(self.cboVarType, SIGNAL('currentIndexChanged(int)'),
                     lambda x: self._update_variable_info())
        self.connect(self.pb_change, SIGNAL('released()'), self._toggle_settings)

    def _toggle_settings(self):
        if self.group_settings.isVisible():
            # self.pb_change.setIcon(IconLibrary.icon('arrow_right'))
            self.group_settings.setVisible(False)
            self.pb_change.setText('Show settings')
        else:
            # self.pb_change.setIcon(IconLibrary.icon('arrow_down'))
            self.group_settings.setVisible(True)
            self.pb_change.setText('Hide settings')

    def _update_variable_info(self):
        use_map = {'model variable': 'a Model Variable',
                   'indicator': 'an Indicator',
                   'both': 'both a Model Variable and an Indicator'}
        self._update_variable_from_fields()
        plural = 'an' if self.variable['source'] == 'expression' else 'a'
        msg = ('This variable is %s <b>%s</b> that will be used as <b>%s</b>' %
               (plural, self.variable['source'], use_map[self.variable['use']]))
        self.lbl_info.setText(msg)

    def init_for_variable(self, variable, validator):
        ''' Setup the variable editor for use with given variable '''
        self.original_variable = variable # keep a reference to the original node
        self.variable = variable.copy() # but manipulate a temporary variable
        self.validator = validator
        # Copy variable values into fields
        self.leVarName.setText(variable['name'])
        index = self.cboVarType.findText(variable['source'])

        if index < 0:
            msg = ('Variable "%s" has an unknown type value (%s).' %
                   (variable['name'], variable['source']))
            # raise RuntimeError(msg)

        self.cboVarType.setCurrentIndex(index)

        if variable['use'] == 'model variable':
            self.rbUseModel.setChecked(True)
        elif variable['use'] == 'indicator':
            self.rbUseIndicator.setChecked(True)
        else:
            self.rbUseBoth.setChecked(True)
        self.le_var_def.document().setPlainText(variable['definition'])
        self.leVarName.selectAll()
        self.leVarName.setFocus()

    def _update_variable_from_fields(self):
        ''' update the variable with values from the gui widgets '''
        self.variable['name'] = str(self.leVarName.text())
        self.variable['source'] = str(self.cboVarType.currentText())
        self.variable['definition'] = str(self.le_var_def.document().toPlainText())
        try:
            dataset_name = VariableName(self.variable['definition']).get_dataset_name()
        except (SyntaxError, ValueError):
            dataset_name = '<unknown>'
        self.variable['dataset'] = dataset_name
        if self.rbUseModel.isChecked():
            self.variable['use'] = 'model variable'
        elif self.rbUseIndicator.isChecked():
            self.variable['use'] = 'indicator'
        else:
            self.variable['use'] = 'both'

    def check_variable(self, check = 'syntax'):
        '''
        validate the variable and display the result in i dialog box
        if check_syntax is True a syntax check is performed, otherwise a data
        check is performed.
        '''
        if check == 'syntax':
            func = batch_check_syntax
        elif check == 'data':
            func = batch_check_data
        else:
            raise ValueError('check_variable() got an unknown value for argument "check"; "%s"' % check)

        self._update_variable_from_fields()
        dummy, result, msgs = func([self.variable,], self.validator)[0]
        if result is True:
            text = '%s check OK' % check
            MessageBox.information(mainwindow = self, text = text)
        else:
            text = 'Encountered a %s error' % check
            MessageBox.warning(mainwindow = self, text = text, detailed_text = '\n '.join(msgs))

    def on_buttonBox_accepted(self):
        # make sure to update the variable before accepting dialog
        self._update_variable_from_fields()
        for key in self.original_variable:
            if self.variable[key] != self.original_variable[key]:
                self.variable['dirty'] = True
                self.variable['inherited'] = None
                break
        self.accept()
