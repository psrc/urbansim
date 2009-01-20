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


from opus_gui.results_manager.views.ui_add_indicator_batch import Ui_dlgAddIndicatorBatch
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog

class AddIndicatorBatch(Ui_dlgAddIndicatorBatch, QDialog):

    def __init__(self, callback = None, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setModal(True)
        self.setupUi(self)
        self.callback = callback

    def on_buttonBox_accepted(self):
        batch_name = str(self.leBatchName.text()).replace(' ', '_')
        self.callback(batch_name)
        self.close()
