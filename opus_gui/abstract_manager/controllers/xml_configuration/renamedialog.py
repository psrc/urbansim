# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import SIGNAL, QString, Qt
from PyQt4.QtGui import QDialog, QMessageBox

from opus_gui.abstract_manager.views.ui_renamedialog import Ui_RenameDialog

class RenameDialog(QDialog, Ui_RenameDialog):
    '''
    Dialog box for renaming objects
    '''
    def __init__(self, old_name, callback, parent_widget):
        '''
        @param old_name (String) the name to change from
        @param callback (Function (String)) callback function
        @param parent_widget (QWidget) parent widget for dialog
        '''
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        self.callback = callback

        self.leName.setText(old_name)
        self.leName.setFocus()
        self.leName.selectAll()

        self.setModal(True)

    def on_buttonBox_accepted(self):
        ''' User clicked OK button '''
        # Call the callback with the users choice of name
        self.callback(self.leName.text())
        self.close()

    def on_buttonBox_rejected(self):
        ''' User clicked cancel '''
        # Ignore changes and close
        self.close()
