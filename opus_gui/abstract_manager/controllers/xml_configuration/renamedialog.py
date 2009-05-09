# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE



# PyQt4 includes for python bindings to QT
from PyQt4.QtGui import QDialog

from opus_gui.abstract_manager.views.ui_renamedialog import Ui_RenameDialog

class RenameDialog(QDialog, Ui_RenameDialog):
    '''
    Dialog box for renaming objects
    '''
    def __init__(self, old_name, parent_widget):
        '''
        If accepted, the changed name is stored in self.accepted_name.
        @param old_name (String) the name to change from
        @param parent_widget (QWidget) parent widget for dialog
        '''
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        self.accepted_name = ''

        self.leName.setText(old_name)
        self.leName.setFocus()
        self.leName.selectAll()

        self.setModal(True)

    def on_buttonBox_accepted(self):
        ''' User clicked OK button '''
        # Call the callback with the users choice of name
        self.accepted_name = str(self.leName.text())
        self.accept()

    def on_buttonBox_rejected(self):
        ''' User clicked cancel '''
        self.accepted_name = ''
        self.reject()


