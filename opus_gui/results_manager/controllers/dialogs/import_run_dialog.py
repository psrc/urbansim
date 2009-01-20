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
import os

from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QDialog, QFileDialog

from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_gui.results_manager.views.ui_import_run_dialog import Ui_dlgImportRun
from opus_gui.results_manager.results_manager import update_available_runs
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.util.exception_formatter import formatExceptionInfo

class ImportRunDialog(QDialog, Ui_dlgImportRun):
    def __init__(self, resultManagerBase, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.project = resultManagerBase.project

    def on_buttonBox_accepted(self):
        path = str(self.lePath.text())
        if not os.path.exists(path):
            msg = 'Cannot import, %s does not exist' % path
            logger.log_warning(msg)
            MessageBox.warning(mainwindow = self,
                            text = msg,
                            detailed_text = '')
        else:
            cache_directory = path
            years = []

            for dir in os.listdir(cache_directory):
                if len(dir) == 4 and dir.isdigit():
                    years.append(int(dir))
            if years == []:
                msg = 'Cannot import, %s has no run data'%path
                logger.log_warning(msg)
                MessageBox.warning(mainwindow = self,
                                text = msg,
                                detailed_text = '')

            else:
                start_year = min(years)
                end_year = max(years)
                project_name = os.environ['OPUSPROJECTNAME']
                run_name = os.path.basename(path)

                server_config = ServicesDatabaseConfiguration()
                run_manager = RunManager(server_config)

                run_id = run_manager._get_new_run_id()
                resources = {
                     'cache_directory': cache_directory,
                     'description': '',
                     'years': (start_year, end_year),
                     'project_name': project_name
                }

                try:
                    run_manager.add_row_to_history(run_id = run_id,
                                                   resources = resources,
                                                   status = 'done',
                                                   run_name = run_name)
                    update_available_runs(self.project)
                    logger.log_status('Added run %s of project %s to run_activity table'%(run_name, project_name))
                except:
                    errorInfo = formatExceptionInfo()
                    logger.log_error(errorInfo)
                    MessageBox.error(mainwindow = self,
                                    text = 'Could not add run %s of project %s to run_activity table'%(run_name, project_name),
                                    detailed_text = errorInfo)
        self.close()

    def on_buttonBox_rejected(self):
        self.close()

    def on_pbn_set_run_directory_released(self):
        start_dir = os.path.join(os.environ['OPUS_HOME'], 'runs', os.environ['OPUSPROJECTNAME'])

        fd = QFileDialog.getExistingDirectory(self,
                    QString("Please select a run directory..."), #, *.sde, *.mdb)..."),
                    QString(start_dir), QFileDialog.ShowDirsOnly)
        if len(fd) != 0:
            fileName = QString(fd)
            self.lePath.setText(fileName)
#        if self.twIndicatorsToVisualize.rowCount() == 0:
#            self.dataset_name = None


