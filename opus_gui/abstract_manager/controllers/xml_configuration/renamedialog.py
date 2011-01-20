# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE



# PyQt4 includes for python bindings to QT
from PyQt4.QtGui import QDialog
from PyQt4.Qt import SIGNAL

from opus_gui.abstract_manager.views.ui_renamedialog import Ui_RenameDialog
from opus_gui.util.convenience import hide_widget_on_value_change

class RenameDialog(QDialog, Ui_RenameDialog):
    '''
    Dialog box for renaming objects
    '''
    def __init__(self, old_name, taken_names, parent_widget):
        '''
        If accepted, the changed name is stored in self.accepted_name.
        @param old_name (str) the name to change from
        @param parent_widget (QWidget) parent widget for dialog
        '''
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        self.accepted_name = ''
        self.taken_names = map(lambda x: x.strip(), taken_names)

        self.lbl_name_warning.setVisible(False)
        hide_widget_on_value_change(self.lbl_name_warning, self.leName)

        self.leName.setText(old_name.strip())
        self.leName.setFocus()
        self.leName.selectAll()

        self.setModal(True)

    def on_buttonBox_accepted(self):
        ''' User clicked OK button '''
        # make sure that there is no naming conflict
        entered_name = str(self.leName.text()).strip()
        if entered_name in self.taken_names:
            self.lbl_name_warning.setText('There is already another node with the name "%s."\n'
                                          'Please enter another name.' % entered_name)
            self.lbl_name_warning.setVisible(True)
        else:
            self.accepted_name = entered_name
            self.accept()

    def on_buttonBox_rejected(self):
        ''' User clicked cancel '''
        self.accepted_name = ''
        self.reject()


