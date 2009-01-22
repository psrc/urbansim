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

from PyQt4.QtCore import QString, QObject, SIGNAL
from PyQt4.QtGui import QDialog
from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_gui.results_manager.run.opus_gui_thread import OpusGuiThread
from opus_gui.results_manager.run.batch_processor import BatchProcessor

from opus_gui.results_manager.views.ui_run_indicator_batch import Ui_runIndicatorBatch
from opus_gui.results_manager.results_manager import get_simulation_runs, get_batch_configuration

class IndicatorBatchRunForm(QDialog, Ui_runIndicatorBatch):
    def __init__(self, mainwindow, resultsManagerBase, batch_name = None,
                 run_name = None):
        QDialog.__init__(self, mainwindow)
        self.setupUi(self)

        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.resultsManagerBase = resultsManagerBase
        self.project = resultsManagerBase.project

        self.available_years_for_simulation_runs = {}

        self.batch_processor = BatchProcessor(project = self.project)

        self.batch_processor.guiElement = self

        self.run_name = run_name
        self.batch_name = batch_name

        self._setup_co__years()

    def _setup_co__years(self):
        runs = get_simulation_runs(self.project)

        for run in runs:
            if run.tag == self.run_name:
                (start, end) = (run.find('start_year').text,
                                run.find('end_year').text)
                break

        (start, end) = (int(start), int(end))
        for i in range(start, end + 1):
            yr = QString(repr(i))
            self.co_start_year.addItem(yr)
            self.co_end_year.addItem(yr)
        for i in range(1, end - start + 2):
            yr = QString(repr(i))
            self.co_every_year.addItem(yr)

    def removeElement(self):
        return True

    def on_buttonBox_accepted(self):

        self.buttonBox.setEnabled(False)

        start_year = int(self.co_start_year.currentText())
        end_year = int(self.co_end_year.currentText())
        increment = int(self.co_every_year.currentText())

        years = range(start_year, end_year + 1, increment)
        # (visualization_type, dataset_name, vals)
        visualizations = get_batch_configuration(project = self.project,
                                                 batch_name = self.batch_name)
        self.batch_processor.set_data(
            visualizations = visualizations,
            source_data_name = self.run_name,
            years = years)

        self.runThread = OpusGuiThread(
                              parentThread = self.mainwindow,
                              parentGuiElement = self,
                              thread_object = self.batch_processor)

        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)

        self.runThread.start()

    # Called when the model is finished...
    def runFinishedFromThread(self,success):
        all_visualizations = self.batch_processor.get_visualizations()
        for indicator_type, visualizations in all_visualizations:
            if indicator_type == 'matplotlib_map' or \
               indicator_type == 'matplotlib_chart':
                form_generator = self.resultsManagerBase.addViewImageIndicator
            elif indicator_type == 'tab':
                form_generator = self.resultsManagerBase.addViewTableIndicator

            if form_generator is not None:
                for visualization in visualizations:
                    form_generator(visualization = visualization,
                                   indicator_type = indicator_type)

        # Get the final logfile update after model finishes...
#        self.logFileKey = self.batch_processor._get_current_log(self.logFileKey)
        self.buttonBox.setEnabled(True)
        self.close()

    def runErrorFromThread(self,errorMessage):
        MessageBox.warning(mainwindow = self.mainwindow,
                          text = "There was a problem running the batch.",
                          detailed_text = errorMessage)
