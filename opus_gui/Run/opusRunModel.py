# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opusRunModel_ui import *
import os, sys, time

from opus_core.tools.start_run import StartRunOptionGroup
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed, SimulationRunError
from inprocess.configurations.xml_configuration import XMLConfiguration

class OpusModelTest(object):
    def __init__(self,parent):
        self.parent = parent
        self.progressCallback = parent.progressCallback
        self.finishedCallback = parent.finishedCallback

    def run(self):
        # Run the Eugene model using the XML version of the Eugene configuration.
        # This code adapted from opus_core/tools/start_run.py
        statusfile = None
        try:
            option_group = StartRunOptionGroup()
            parser = option_group.parser
            # simulate 0 command line arguments by passing in []
            (options, args) = parser.parse_args([])
            run_manager = option_group.get_run_manager(options)
            # find the directory containing the eugene xml configurations
            xml_dir = __import__('opus_gui').__path__[0]
            xml_path = os.path.join(xml_dir, 'projects', 'eugene', 'baseline.xml')
            # xml_dir = __import__('inprocess').__path__[0]
            # xml_path = os.path.join(xml_dir, 'configurations', 'projects', 'eugene', 'baseline.xml')
            config = XMLConfiguration(xml_path)
            insert_auto_generated_cache_directory_if_needed(config)
            (self.start_year, self.end_year) = config['years']
            cache_dir = config['cache_directory']
            statusfile = os.path.join(cache_dir, 'status.txt')
            self.statusfile = statusfile
            config['status_file_for_gui'] = statusfile
            run_manager.run_run(config)
            succeeded = True
        except SimulationRunError:
            succeeded = False
        if statusfile is not None and os.path.exists(statusfile):
            os.remove(statusfile)
        self.parent.finishedCallback(succeeded)
        
        # statement to signal i % progress:
        # self.parent.progressCallback(i)
        
    def _compute_progress(self, statusfile):
        # Compute percent progress for the progress bar.
        # The statusfile is written by the _write_status_for_gui method
        # in class ModelSystem in urbansim.model_coordinators.model_system
        # The file is ascii, with the following format (1 item per line):
        #   current year
        #   total number of models
        #   number of current model that is about to run (starting with 0)
        #   message to display in the progress bar widget
        try:
            f = open(statusfile)
            lines = f.readlines()
            f.close()
            # use float for all numbers to help with percent computation
            current_year = float(lines[0])
            total_models = float(lines[1])
            current_model = float(lines[2])
            message = lines[3].strip()
            total_years = float(self.end_year - self.start_year + 1)
            # For each year, we need to run all of the models.
            # year_fraction_completed is the fraction completed (ignoring the currently running year)
            # model_fraction_completed is the additional fraction completed for the current year
            year_fraction_completed = (current_year - self.start_year) / total_years
            model_fraction_completed = (current_model / total_models) / total_years
            percentage = 100.0* (year_fraction_completed + model_fraction_completed)
            return {"percentage":percentage,"message":message}
        except IOError:
            return {"percentage":0,"message":"Model initializing..."}

class RunModelThread(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        
    def run(self):
        self.parent.progressBar.setRange(0,100)
        self.model = OpusModelTest(self)
        self.model.run()

    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)
            

class RunModelGui(QDialog, Ui_OpusRunModel):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
        self.parent = parent
        self.progressBar = self.runProgressBar
        self.statusLabel = self.runStatusLabel
        self.progressBar.reset()
        self.statusLabel.setText(QString("Press Start to run the model..."))

    def on_pbnStartModel_released(self):
        # Fire up a new thread and run the model
        print "Start Model Pressed"
        self.pbnStartModel.setEnabled(False)
        self.progressBar.setValue(0)
        self.statusLabel.setText(QString("Model initializing..."))
        self.runThread = RunModelThread(self)
        # Use this signal from the thread if it is capable of producing its own status signal
        #QObject.connect(self.runThread, SIGNAL("runPing(PyQt_PyObject)"),
        #                self.runPingFromThread)
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runStatusFromThread)
        self.timer.start(1000)
        self.runThread.start()
            
    def on_pbnCancel_released(self):
        self.close()

    # This is not used currently since the model can not return status... instead we use a timer to
    # check the status from a log file.
    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        #print "Ping from thread!"

    # Called when the model is finished... peg the percentage to 100% and stop the timer.
    def runFinishedFromThread(self,success):
        print "Model Finished with sucess = ", success
        self.progressBar.setValue(100)
        self.statusLabel.setText(QString("Model finished with status = %s" % (success)))
        self.timer.stop()
        self.pbnStartModel.setEnabled(True)

    def runStatusFromThread(self):
        status = self.runThread.model._compute_progress(self.runThread.model.statusfile)
        self.progressBar.setValue(status["percentage"])
        self.statusLabel.setText(status["message"])
        print "runStatusFromThread from timer with percentage = %d and message = %s" % (status["percentage"],
                                                                                        status["message"])
