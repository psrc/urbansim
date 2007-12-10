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
import os, shutil, sys, tempfile, time

try:
    from opus_core.tools.start_run import StartRunOptionGroup
    from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed, SimulationRunError
    from inprocess.travis.opus_gui.configurations.xml_configuration import XMLConfiguration
    WithOpus = True
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class RunModelThread(QThread):
    def __init__(self, parentThread,parent,xml_file):
        QThread.__init__(self, parentThread)
        self.parent = parent
        self.xml_file = xml_file
        
    def run(self):
        self.parent.progressBar.setRange(0,100)
        #self.model = OpusModel(self,self.xml_file)
        #self.model.run()
        self.parent.model.progressCallback = self.progressCallback
        self.parent.model.finishedCallback = self.finishedCallback
        self.parent.model.run()
        
    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)
            

class OpusModel(object):
    def __init__(self,parent,xml_path):
        self.parent = parent
        self.xml_path = xml_path
        #self.thread = RunModelThread(self.parent.parent,self.xml_path)
        self.progressCallback = None
        self.finishedCallback = None
        self.guiElement = None
        self.config = None
        self.statusfile = None

    def run(self):
        if WithOpus:
            # Run the Eugene model using the XML version of the Eugene configuration.
            # This code adapted from opus_core/tools/start_run.py
            # statusdir is a temporary directory into which to write a status file
            # regarding the progress of the simulation - the progress bar reads this file
            statusdir = None
            try:
                option_group = StartRunOptionGroup()
                parser = option_group.parser
                # simulate 0 command line arguments by passing in []
                (options, args) = parser.parse_args([])
                run_manager = option_group.get_run_manager(options)
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                #print fileNameAbsolute
                config = XMLConfiguration(str(fileNameAbsolute))
                insert_auto_generated_cache_directory_if_needed(config)
                (self.start_year, self.end_year) = config['years']

                run_manager.setup_new_run(run_name = config['cache_directory'])
                #statusdir = tempfile.mkdtemp()
                statusdir = run_manager.get_current_cache_directory()
                statusfile = os.path.join(statusdir, 'status.txt')
                self.statusfile = statusfile
                self.config = config
                config['status_file_for_gui'] = statusfile
                run_manager.run_run(config)
                succeeded = True
            except SimulationRunError:
                succeeded = False
            if statusdir is not None:
                shutil.rmtree(statusdir, ignore_errors=True)
            self.finishedCallback(succeeded)
        else:
            pass
        
    def _compute_progress(self, statusfile):
        if statusfile is None:
            return {"percentage":0,"message":"Model initializing..."}
        if WithOpus:
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

    def _get_current_log(self, key):
        newKey = key
        if WithOpus:
            # We attempt to keep up on the current progress of the model run.  We pass into this
            # function an intial "key" value of 0 and expect to get back a new "key" after the
            # function returns.  It is up to us in this function to use this key to determine
            # what has happened since last time this function was called.
            # In this example we use the key to indicate where in a logfile we last stopped reading
            # and seek into that file point and read to the end of the file and append to the
            # log text edit field in the GUI.
            if self.config is not None and 'cache_directory' in self.config:
                try:
                    f = open(os.path.join(self.config['cache_directory'],'year_1981_log.txt'))
                    f.seek(key)
                    lines = f.read()
                    newKey = f.tell()
                    if newKey != key:
                        self.guiElement.logText.append(lines)
                    f.close()
                except IOError:
                    self.guiElement.logText.append("No logfile yet")
                #self.guiElement.logText.append("ping")
        return newKey
