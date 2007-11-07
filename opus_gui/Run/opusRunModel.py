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

    def run(self):
        # Run the Eugene model using the XML version of the Eugene configuration.
        # This code hacked together based on opus_core/tools/start_run.py
        # No progress bar indicator yet ...
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
            config = XMLConfiguration(xml_path)
            insert_auto_generated_cache_directory_if_needed(config)
            cache_dir = config['cache_directory']
            statusfile = os.path.join(cache_dir, 'status.txt')
            config['status_file_for_gui'] = statusfile
            run_manager.run_run(config)
            succeeded = True
        except SimulationRunError:
            succeeded = False
        if statusfile is not None and os.path.exists(statusfile):
            os.remove(statusfile)
        self.parent.finishedCallback(succeeded)
        #
        # statement to signal i % progress:
        # self.parent.progressCallback(i)
        
    def _compute_progress(self, statusfile):
        # Stub method to compute percent progress for the progress bar
        # the statusfile is written by the _write_status_for_gui method
        # in class ModelSystem in urbansim.model_coordinators.model_system
        # The file is ascii, with the following format (1 item per line):
        #   start year
        #   end year
        #   current year
        #   total number of models
        #   number of current model that is about to run
        #   message to display in the progress bar widget
        f = open(statusfile)
        lines = f.readlines()
        f.close()
        # use float for all numbers to help with percent computation
        start_year = float(lines[0])
        end_year = float(lines[1])
        current_year = float(lines[2])
        total_models = float(lines[3])
        current_model = float(lines[4])
        message = lines[5].strip()
        total_years = end_year - start_year + 1
        # For each year, we need to run all of the models.
        # year_fraction_completed is the fraction completed (ignoring the currently running year)
        # model_fraction_completed is the additional fraction completed for the current year
        year_fraction_completed = (current_year - start_year) / total_years
        model_fraction_completed = (current_model / total_models) / total_years
        percentage = 100.0* (year_fraction_completed + model_fraction_completed)
        print percentage
        print message
        
    
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
        self.progressBar.reset()

    def on_pbnStartModel_released(self):
        # Fire up a new thread and run the model
        print "Start Model Pressed"
        self.runThread = RunModelThread(self)
        QObject.connect(self.runThread, SIGNAL("runPing(PyQt_PyObject)"),
                        self.runPingFromThread)
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        self.runThread.start()
            
    def on_pbnCancel_released(self):
        self.close()

    def runPingFromThread(self,value):
        self.progressBar.setValue(value)
        print "Ping from thread!"

    def runFinishedFromThread(self,success):
        print "Model Finished!"

