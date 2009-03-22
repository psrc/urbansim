# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


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
