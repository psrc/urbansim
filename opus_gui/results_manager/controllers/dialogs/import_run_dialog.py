# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE



# PyQt4 includes for python bindings to QT
import os

from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QFileDialog

from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_gui.results_manager.views.ui_import_run_dialog import Ui_dlgImportRun
from opus_gui.results_manager.results_manager_functions import sync_available_runs
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_core import paths

class ImportRunDialog(QDialog, Ui_dlgImportRun):
    def __init__(self, resultManagerBase, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.project = resultManagerBase.project

    def on_buttonBox_accepted(self):
        path = str(self.lePath.text())
        if not os.path.exists(path):
            msg = 'Cannot import run from %s: path does not exist' % path
            logger.log_warning(msg)
            MessageBox.warning(mainwindow = self,
                            text = msg,
                            detailed_text = '')
        else:
            self.resultManagerBase.import_run(path)
        self.close()
            #self.resultManagerBase.add_run_to_servicesdb(cache_directory=path)
        #self.close()

    def on_buttonBox_rejected(self):
        self.close()

    def on_pbn_set_run_directory_released(self):
        start_dir = paths.get_opus_home_path('runs', os.environ['OPUSPROJECTNAME'])

        fd = QFileDialog.getExistingDirectory(self,
                    QString("Please select a run directory..."), #, *.sde, *.mdb)..."),
                    QString(start_dir), QFileDialog.ShowDirsOnly)
        if len(fd) != 0:
            fileName = QString(fd)
            self.lePath.setText(fileName)
#        if self.twIndicatorsToVisualize.rowCount() == 0:
#            self.dataset_name = None


