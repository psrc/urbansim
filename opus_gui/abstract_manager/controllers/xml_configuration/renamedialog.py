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
from PyQt4.QtCore import SIGNAL, QString, Qt
from PyQt4.QtGui import QDialog, QMessageBox

from opus_gui.abstract_manager.views.ui_renamedialog import Ui_RenameDialog

class RenameDialog(QDialog, Ui_RenameDialog):
    '''
    Dialogbox for renaming objects
    '''
    def __init__(self, old_name, callback, parent_widget):
        '''
        @param old_name (String): the name to change
        @param callback (Function (String)): callback function
        @param parent_widget (QWidget): owning widget
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
