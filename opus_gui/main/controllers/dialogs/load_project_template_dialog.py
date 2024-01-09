# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from opus_gui.main.opus_project import OpusProject
from opus_gui.main.built_in_project_templates import get_builtin_project_templates
from opus_gui.main.views.dialogs.ui_load_project_template_dialog import Ui_LoadProjectTemplateDialog


class LoadProjectTemplateDialog(QDialog, Ui_LoadProjectTemplateDialog):
    '''
    Dialog box that lets the user select a base project to create a new project from.
    The selected project becomes the parent of the new project.
    The new project is passed on to the NewProjectDialog so the user can setup project specific options.
    '''
    
    
    def __init__(self, parent_widget = None):
            '''
            @param parent_widget (QObject): parent widget for this dialog
            '''
            # parent window for the dialog box
            flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
            QtWidgets.QDialog.__init__(self, parent_widget, flags)
            self.setupUi(self)
            
            self.template_project = None
            
            self._hide_error()
            
            # visual tweaks
            self.buttonBox.button(self.buttonBox.Ok).setText('Load')
            
            # list the built in projects
            self._builtin_templates = get_builtin_project_templates()
            for title in sorted(self._builtin_templates):
                self.lst_builtin_templates.addItem(title)
            # select the first entry by default
            self.lst_builtin_templates.setCurrentRow(0)
           
            
    def _hide_error(self):
        ''' Hide the error text '''
        self.lbl_error.setVisible(False)
       
        
    def _show_error(self, msg):
        ''' Show an error text to the user '''
        msg = '<qt><strong style="color: darkred;">Error</strong>&nbsp;' + msg + '</qt>'
        self.lbl_error.setText(msg)
        self.lbl_error.setVisible(True)


    def _selected_filname(self):
        ''' Resolve the filename, either from the builtin options or from a user specified value '''
        if self.rb_use_builtin.isChecked():
            selected_item = self.lst_builtin_templates.currentItem()
            if selected_item is None:
                self._show_error('Please select a template to load')
                return False
            if selected_item.text() in list(self._builtin_templates.keys()):
                return self._builtin_templates[str(selected_item.text())]
            else:
                self._show_error('Something unexpected happened.<br/>Could not find the selected builtin template')
                return False
        else: # use custom
            if len(str(self.le_custom_filename.text())) == 0:
                self.le_custom_filename.setFocus()
                self._show_error('Please select a custom project template or select one of the builtins')
                return False
            # validate that the selected file can be opened
            filename = str(self.le_custom_filename.text())
            try:
                file = open(filename, 'r')
                return filename
            except Exception as e:
                self._show_error('Could not load the custom project template.<br/>' + 
                                 'Please revise the entered filename.<br/>' + 
                                 'The error was:<br/><strong>' + str(e) + '</strong>')
        return False 
    
    
    def _load_project(self, filename):
        ''' 
        Load the project from the given filename and return it. 
        None is returned if the project could not be loaded. 
        '''
        try:
            project = OpusProject()
            flag, message = project.open(filename)
            if flag is not True:
                raise Exception(message)
            return project
        except Exception as ex:
            self._show_error('There was a problem loading the specified project template<br/>' + 
                             'The error was:<br/>'+
                             '<strong>' + str(ex) + '</strong>')
        return None


# =================
# AUTO WIRED EVENTS
# =================
    
    def on_le_custom_filename_textEdited(self, text):
        # check the use custom radio button when the user starts entering a custom filename
        if not self.rb_use_custom.isChecked():
            self.rb_use_custom.setChecked(True)
    
    def on_lst_builtin_templates_itemClicked(self, item):
        # check the use builtin radio button when the user selects a builtin
        self.rb_use_builtin.setChecked(True)
    
    @pyqtSlot()
    def on_tb_custom_browse_clicked(self):
        # let the user browse for a custom template project to load
        self.rb_use_custom.setChecked(True)
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Something', '', "OPUS Project (*.xml)")
        if len(str(filename)) == 0: # user canceled dialog
            return
        self.le_custom_filename.setText(filename)
    
    def on_buttonBox_accepted(self):
        # the user clicked 'Load'
        # resolve filename and ensure that it's a valid opus project
        selected_filename = self._selected_filname()
        if selected_filename is False:
            return
        
        project = self._load_project(selected_filename)
        if project is None:
            return
        
        # QtWidgets.QMessageBox.information(self, '', 'Loading project: ' + project.name)
        # Got a reference to a valid project to load. Setup the expected response property of the dialog.
        self.template_project = project
        self.accept()
        
    def on_buttonBox_rejected(self):
        self.template_project = None
        self.reject()

    
    
