# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QDialog, qApp
from PyQt4.QtCore import SIGNAL, QEventLoop

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.general_manager.models.variables_table_model import batch_check_syntax
from opus_gui.general_manager.models.variables_table_model import batch_check_data
from opus_gui.general_manager.general_manager_functions import get_available_dataset_names

# Change to ui_variable_editor_alternative for alternative editor
from opus_gui.general_manager.views.ui_variable_editor import Ui_VariableEditor
from opus_core.variables.variable_name import VariableName
from opus_gui.util.convenience import hide_widget_on_value_change

class VariableEditor(QDialog, Ui_VariableEditor):

    '''
    Editor dialog for variable definitions.
    Variables that are passed to the editor are expected to be in the dictionary format specified
    in VariableTableModel.
    '''

    def __init__(self, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.original_variable = None
        self.variable = None
        self.validator = None
        self.callback = None
        def check_data(): self.check_variable(check = 'data')
        def check_syntax(): self.check_variable(check = 'syntax')
        self.connect(self.btnCheckData, SIGNAL("clicked()"), check_data)
        self.connect(self.btnCheckSyntax, SIGNAL("clicked()"), check_syntax)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

        self.frame_name_warning.setVisible(False)
        hide_widget_on_value_change(self.frame_name_warning, self.leVarName)

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
        self.connect(self.pb_change, SIGNAL("clicked()"), self._toggle_settings)

    def init_for_variable(self, variable, validator, existing_variables):
        ''' Prepare the editor to edit a variable.
        @param variable The variable to edit (dict)
        @param validator A VariableValidator object used for data/syntax checking
        @param existing_variables a list of tuples with (dataset, variable name) for all existing
                                  variables. Used for checking for unique names.
        '''
        self.original_variable = variable # keep a reference to the original node...
        self.variable = variable.copy() # ...but manipulate a temporary variable
        self.validator = validator
        self.existing_variables = existing_variables or []

        self.leVarName.setText(variable['name'])
        self.le_var_def.document().setPlainText(variable['definition'])
        index = self.cboVarType.findText(variable['source'])
        if index < 0: # variable source was not in the combo box
            text = 'Failed to edit variable %s' % variable['name']
            details = ('Variable "%s" (dataset: %s) has an unknown type value (%s).\n'
                       'Please select a new type and update/save the variable.' %
                       (variable['name'], variable['dataset'], variable['source']))
            MessageBox.warning(self, text, details)
            
        # This triggers _update_variable_from_fields and hence requires
        # name and definition to be set already
        self.cboVarType.setCurrentIndex(index)

        if variable['use'] == 'model variable':
            self.rbUseModel.setChecked(True)
        elif variable['use'] == 'indicator':
            self.rbUseIndicator.setChecked(True)
        else:
            self.rbUseBoth.setChecked(True)
        self.leVarName.selectAll()
        self.leVarName.setFocus()

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

    def _name_warning(self, text):
        self.lbl_name_warning.setText(text)
        self.frame_name_warning.setVisible(True)
        self.leVarName.selectAll()
        self.leVarName.setFocus()

    def _update_variable_from_fields(self):
        ''' update the variable with values from the gui widgets '''
        self.variable['name'] = str(self.leVarName.text())
        self.variable['source'] = str(self.cboVarType.currentText())
        self.variable['definition'] = str(self.le_var_def.document().toPlainText())
        try:
            v = VariableName(self.variable['definition'])
            dataset_name = v.get_dataset_name()
            interaction_set_names = v.get_interaction_set_names()
        except (SyntaxError, ValueError):
            MessageBox.error(mainwindow = self,
                text = 'parse error for variable',
                detailed_text = 'setting dataset name for this variable to <unknown>')
            dataset_name = '<unknown>'
            interaction_set_names = None
        if dataset_name is None and interaction_set_names is not None:
            # It's an interaction set.  Look up possible names in available_datasets
            names = get_available_dataset_names(self.validator.project)
            n1 = interaction_set_names[0] + '_x_' + interaction_set_names[1]
            if n1 in names:
                dataset_name = n1
            else:
                n2 = interaction_set_names[1] + '_x_' + interaction_set_names[0]
                if n2 in names:
                    dataset_name = n2
                else:
                    MessageBox.error(mainwindow = self,
                        text = 'unable to find an interaction set in available_datasets for this variable',
                        detailed_text = "tried %s and %s \nbut couldn't find either name in available_datasets \nsetting dataset_name to <unknown>" % (n1,n2) )
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
        # update the variable before accepting dialog
        self._update_variable_from_fields()
        # make sure the name is unique and not a reserved word
        if self.variable['name'].strip() == 'constant':
            self._name_warning('The name "constant" is a reserved keyword.\n'
                               'Please choose another name')
            return
        if self.variable['name'].strip() == 'None':
            self._name_warning('The name "None" is a reserved keyword.\n'
                               'Please choose another name')
            return
        if self.variable['name'].strip() == '':
            self._name_warning('The variable must have a name.\n'
                               'Please enter a name')
            return
        # if the user changed the variable name we need to make sure it's unique
        if self.original_variable['name'] != self.variable['name']:
            for dataset, taken_name in self.existing_variables:
                if self.variable['dataset'] == dataset and self.variable['name'] == taken_name:
                    self._name_warning('The variable name "%s" (for dataset "%s") is already taken.\n'
                                       'Please choose another name.' %(taken_name, dataset))
                    self.leVarName.selectAll()
                    self.leVarName.setFocus()
                    return
        # only mark the variable as dirty if we changed anything
        for key in self.original_variable:
            if self.variable[key] != self.original_variable[key]:
                self.variable['dirty'] = True
                self.variable['inherited'] = None
                break
        self.accept()
