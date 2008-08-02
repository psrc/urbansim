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
#

# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys
from opus_gui.exceptions.formatter import formatExceptionInfo

try:
    from opus_core.tools.start_run import StartRunOptionGroup
    from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed, SimulationRunError
    #from opus_gui.configurations.xml_configuration import XMLConfiguration
    from opus_core.configurations.xml_configuration import XMLConfiguration
    from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper
    from opus_gui.results.gui_result_interface.batch_processor import BatchProcessor
    from opus_core.services.run_server.run_manager import RunManager

    WithOpus = True
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class RunModelThread(QThread):
    def __init__(self, mainwindow, modelguielement, xml_file, batch_name = None, run_name = None):
        QThread.__init__(self, mainwindow)
        self.run_name = run_name
        self.modelguielement = modelguielement
        self.modelguielement.model.run_name = run_name
        self.xml_file = xml_file
        self.batch_name = batch_name
        self.toolboxStuff = self.modelguielement.mainwindow.toolboxStuff
        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = self.toolboxStuff)

    def run(self):
        self.modelguielement.model.progressCallback = self.progressCallback
        self.modelguielement.model.finishedCallback = self.finishedCallback
        self.modelguielement.model.errorCallback = self.errorCallback
        self.modelguielement.model.run()

    def pause(self):
        self.modelguielement.model.pause()

    def resume(self):
        self.modelguielement.model.resume()

    def cancel(self):
        self.modelguielement.model.cancel()

    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
            self.add_run_to_run_manager_xml()
            if self.batch_name is not None:
                self.runIndicatorBatch()
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)

    def add_run_to_run_manager_xml(self):
        '''add this completed run to the run manager section of the results manager'''
        self.xml_helper.update_available_runs()
        
    def get_run_name(self):
        if self.run_name is None:
            cache_directory = self.modelguielement.model.config['cache_directory']
            self.run_name = 'Run_%s'%os.path.basename(cache_directory)
            
        return self.run_name
    
    def get_years(self):
        return self.modelguielement.model.config['years']
    
    def runIndicatorBatch(self):
        visualizations = self.xml_helper.get_batch_configuration(
                            batch_name =  self.batch_name) 
        start, end = self.get_years()
        
        self.batch_processor = BatchProcessor(toolboxStuff = self.toolboxStuff)           
        self.batch_processor.errorCallback = self.errorCallback
        self.batch_processor.finishedCallback = self.indicatorBatchFinishedCallback
        
        self.batch_processor.set_data(
            visualizations = visualizations, 
            source_data_name = self.get_run_name(),
            years = range(start, end + 1))
        
        self.batch_processor.run()
                
    def indicatorBatchFinishedCallback(self, success):
        return 
    
    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("runError(PyQt_PyObject)"),errorMessage)


class OpusModel(object):
    def __init__(self,xmltreeobject,xml_path,modeltorun):
        self.xmltreeobject = xmltreeobject
        self.xml_path = xml_path
        self.modeltorun = modeltorun
        self.progressCallback = None
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.statusfile = None
        self.firstRead = True
        self.running = False
        self.paused = False
        self.start_year = None
        self.currentLogfileYear = None
        self.currentLogfileKey = None
        option_group = StartRunOptionGroup()
        parser = option_group.parser
        # simulate 0 command line arguments by passing in []
        (options, args) = parser.parse_args([])
        
        self.run_manager = RunManager(options)
        
    def pause(self):
        self.paused = True
        self._write_command_file('pause')

    def resume(self):
        self.paused = False
        self._write_command_file('resume')

    def cancel(self):
        self.running = False
        self.paused = False
        self._write_command_file('stop')

    def run(self):
        if WithOpus:
            # Run the Eugene model using the XML version of the Eugene configuration.
            # This code adapted from opus_core/tools/start_run.py
            # statusdir is a temporary directory into which to write a status file
            # regarding the progress of the simulation - the progress bar reads this file
            statusdir = None
            succeeded = False
            try:
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                #print fileNameAbsolute
                #print self.modeltorun
                config = XMLConfiguration(str(fileNameAbsolute)).get_run_configuration(str(self.modeltorun))
                if self.run_name is not None:
                    config['description'] = self.run_name
                    
                insert_auto_generated_cache_directory_if_needed(config)
                (self.start_year, self.end_year) = config['years']

                self.run_manager.setup_new_run(run_name = config['cache_directory'])

                #statusdir = tempfile.mkdtemp()
                statusdir = self.run_manager.get_current_cache_directory()
                self.statusfile = os.path.join(statusdir, 'status.txt')
                #print self.statusfile
                self.currentLogfileYear = self.start_year
                self.currentLogfileKey = 0
                self.config = config
                config['status_file_for_gui'] = self.statusfile
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
                errorInfo = formatExceptionInfo(custom_message = 'Unexpected Error From Model')
                self.errorCallback(errorInfo)
            if self.statusfile is not None:
                os.remove(self.statusfile)
            self.finishedCallback(succeeded)
        else:
            pass

    def _compute_progress(self):
        if self.statusfile is None:
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
                f = open(self.statusfile)
                lines = f.readlines()
                f.close()
                # use float for all numbers to help with percent computation
                current_year = float(lines[0])
                total_models = float(lines[1])
                current_model = float(lines[2])
                model_name = lines[3].strip()
                total_pieces = float(lines[4])
                current_piece = float(lines[5])
                # piece_description = lines[6].strip()
                total_years = float(self.end_year - self.start_year + 1)
                # For each year, we need to run all of the models.
                # year_fraction_completed is the fraction completed (ignoring the currently running year)
                # model_fraction_completed is the additional fraction of the models completed for the current year
                # piece_fraction_completed is the additional fraction of the pieces of the current model completed for the current year
                year_fraction_completed = (current_year - self.start_year) / total_years
                model_fraction_completed = (current_model / total_models) / total_years
                piece_fraction_completed = (current_piece / total_pieces) / (total_years*total_models)
                percentage = 100.0* (year_fraction_completed + model_fraction_completed + piece_fraction_completed)
                # omit the piece description for now (too long to fit)
                # message = 'year: %d  model: %s %s' % (current_year, model_name, piece_description)
                message = 'year: %d  model: %s' % (current_year, model_name)
                return {"percentage": percentage, "message": message}
            except IOError:
                return {"percentage": 0, "message":" Model initializing..."}

    def _read_log(self,filename,key):
        newKey = key
        logText = QString("")
        try:
            logfile = open(filename)
            logfile.seek(key)
            lines = logfile.read()
            newKey = logfile.tell()
            if newKey != key:
                logText.append(lines)
            else:
                logText.append(QString(".."))
            logfile.close()
        except IOError:
            if self.firstRead == True:
                logText.append("No logfile yet")
                self.firstRead = False
            else:
                logText.append(QString("."))
        return [newKey,logText]
    
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
            # Since there is a different log file for each simulation year, we also need to figure out 
            # the name of the current log file. The current year is found by looking in the status.txt
            # file (also used by the progress bar).  If this file doesn't exist, the current year is 
            # the start year.  (We open the status.txt file separately from the compute progress method,
            # since there are separate threads that may be using these methods.)
            year = self.start_year
            if self.statusfile is not None:
                #print self.statusfile
                try:
                    # the current year is in the first line of the status file
                    f = open(self.statusfile)
                    year = int(f.readline())
                    f.close()
                except IOError:
                    if year != self.currentLogfileYear:
                        # if the current is not the first year then we must be at the end. Set
                        # year = self.currentLogfileYear so we still pick up the last log bits
                        # from the last year...
                        year = self.currentLogfileYear

            if self.config is not None and 'cache_directory' in self.config:
                # Now we know we have a cache directory and year to look for our file
                currentYearLogfile = os.path.join(self.config['cache_directory'],'year_%d_log.txt' % year)
                # Check if we have jumped to the next year
                if year != self.currentLogfileYear:
                    # We have switched to the next year and need to grab the last of the previous years
                    # log and then the first part of the new log...
                    lastYearLogfile = os.path.join(self.config['cache_directory'],'year_%d_log.txt' % self.currentLogfileYear)
                    [newKey,logText] = self._read_log(lastYearLogfile,key)
                    self.guiElement.logText.insertPlainText(logText)
                    # Reset the key and bump the year since we are switching files
                    key = 0
                    self.currentLogfileYear = year
                    # Mark the transition in the GUI log so it is easier to see
                    self.guiElement.logText.insertPlainText(QString("\n\n\n ******** Moving to next year logfile *********\n\n\n"))
                # Now we can read in from the current log for the current year
                [newKey,logText] = self._read_log(currentYearLogfile,key)
                self.guiElement.logText.insertPlainText(logText)
                self.guiElement.logText.ensureCursorVisible()
        # Return the new key to the caller
        return newKey

    def _write_command_file(self, command):
        f = open(self.commandfile, 'w')
        f.write(command)
        f.close()
