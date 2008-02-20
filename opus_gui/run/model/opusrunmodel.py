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
import os, sys


try:
    from opus_core.tools.start_run import StartRunOptionGroup
    from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed, SimulationRunError
    #from opus_gui.configurations.xml_configuration import XMLConfiguration
    from opus_core.configurations.xml_configuration import XMLConfiguration
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
        self.parent.model.errorCallback = self.errorCallback
        self.parent.model.run()
        
    def pause(self):
        self.parent.model.pause()

    def resume(self):
        self.parent.model.resume()

    def cancel(self):
        self.parent.model.cancel()

    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)

    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("runError(PyQt_PyObject)"),errorMessage)


class OpusModel(object):
    def __init__(self,parent,xml_path,modeltorun):
        self.parent = parent
        self.xml_path = xml_path
        self.modeltorun = modeltorun
        self.run_manager = None
        self.progressCallback = None
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.statusfile = None
        self.firstRead = True
        self.running = False
        self.paused = False
    
    def formatExceptionInfo(self,maxTBlevel=5):
        import traceback
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try:
            excArgs = exc.__dict__["args"]
        except KeyError:
            excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)
    
    def pause(self):
        self.paused = True
        print "Pause pressed"
        # Can access the run manager via self.run_manager
    
    def resume(self):
        self.paused = False
        print "Resume pressed"
        # Can access the run manager via self.run_manager
    
    def cancel(self):
        self.running = False
        self.paused = False
        print "Cancel pressed"
        # Can access the run manager via self.run_manager
    
    def run(self):
        if WithOpus:
            # Run the Eugene model using the XML version of the Eugene configuration.
            # This code adapted from opus_core/tools/start_run.py
            # statusdir is a temporary directory into which to write a status file
            # regarding the progress of the simulation - the progress bar reads this file
            statusdir = None
            statusfile = None
            succeeded = False
            try:
                option_group = StartRunOptionGroup()
                parser = option_group.parser
                # simulate 0 command line arguments by passing in []
                (options, args) = parser.parse_args([])
                self.run_manager = option_group.get_run_manager(options)
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                print fileNameAbsolute
                print self.modeltorun
                config = XMLConfiguration(str(fileNameAbsolute)).get_run_configuration(str(self.modeltorun))
                insert_auto_generated_cache_directory_if_needed(config)
                (self.start_year, self.end_year) = config['years']

                self.run_manager.setup_new_run(run_name = config['cache_directory'])
                #statusdir = tempfile.mkdtemp()
                statusdir = self.run_manager.get_current_cache_directory()
                statusfile = os.path.join(statusdir, 'status.txt')
                self.statusfile = statusfile
                self.config = config
                config['status_file_for_gui'] = statusfile
                self.commandfile = os.path.join(statusdir, 'command.txt')
                config['command_file_for_gui'] = self.commandfile
                # To test delay in writing the first log file entry...
                # time.sleep(5)
                self.running = True
                self.run_manager.run_run(config)
                self.running = False
                succeeded = True
            except SimulationRunError:
                self.running = False
                succeeded = False
            except:
                self.running = False
                succeeded = False
                errorInfo = self.formatExceptionInfo()
                errorString = "Unexpected Error From Model :: " + str(errorInfo)
                print errorInfo
                self.errorCallback(errorString)
            if statusfile is not None:
                os.remove(statusfile)
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
            #   name of current model
            #   total number of pieces of current model (could be 1)
            #   number of current piece
            #   description of current piece (empty string if no description)
            try:
                f = open(statusfile)
                lines = f.readlines()
                f.close()
                # use float for all numbers to help with percent computation
                current_year = float(lines[0])
                total_models = float(lines[1])
                current_model = float(lines[2])
                model_name = lines[3].strip()
                total_pieces = float(lines[4])
                current_piece = float(lines[5])
                piece_description = lines[6].strip()
                total_years = float(self.end_year - self.start_year + 1)
                # For each year, we need to run all of the models.
                # year_fraction_completed is the fraction completed (ignoring the currently running year)
                # model_fraction_completed is the additional fraction of the models completed for the current year
                # piece_fraction_completed is the additional fraction of the pieces of the current model completed for the current year
                year_fraction_completed = (current_year - self.start_year) / total_years
                model_fraction_completed = (current_model / total_models) / total_years
                piece_fraction_completed = (current_piece / total_pieces) / (total_years*total_models)
                percentage = 100.0* (year_fraction_completed + model_fraction_completed + piece_fraction_completed)
                message = 'year: %d  model: %s %s' % (current_year, model_name, piece_description)
                return {"percentage": percentage, "message": message}
            except IOError:
                return {"percentage": 0, "message":" Model initializing..."}

    def _get_current_log(self, key):
        newKey = key
        if WithOpus:
            # We attempt to keep up on the current progress of the model run.  We pass into this
            # function an initial "key" value of 0 and expect to get back a new "key" after the
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
                    else:
                        self.guiElement.logText.insertPlainText(QString("."))
                    f.close()
                except IOError:
                    if self.firstRead == True:
                        self.guiElement.logText.append("No logfile yet")
                        self.firstRead = False
                    else:
                        self.guiElement.logText.insertPlainText(QString("."))
                #self.guiElement.logText.append("ping")
        return newKey
