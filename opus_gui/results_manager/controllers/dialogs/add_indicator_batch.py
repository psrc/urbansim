# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_gui.results_manager.views.ui_add_indicator_batch import Ui_dlgAddIndicatorBatch
from PyQt5.QtWidgets import QDialog

class AddIndicatorBatch(Ui_dlgAddIndicatorBatch, QDialog):

    def __init__(self, callback = None, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setModal(True)
        self.setupUi(self)
        self.callback = callback

    def on_buttonBox_accepted(self):
        batch_name = str(self.leBatchName.text())
        self.callback(batch_name)
        self.close()
