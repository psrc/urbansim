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
from PyQt4.QtCore import QThread, SIGNAL, QFileInfo, QString

import os, time

from opus_gui.util.exception_formatter import formatExceptionInfo
from urbansim.estimation.estimation_runner import EstimationRunner
    
class RunEstimationThread(QThread):
    def __init__(self, mainwindow, estimationguielement, xml_file):
        QThread.__init__(self, mainwindow)
        self.estimationguielement = estimationguielement
        self.xml_file = xml_file

    def run(self):
        self.estimationguielement.progressBar.setRange(0,100)
        self.estimationguielement.estimation.progressCallback = self.progressCallback
        self.estimationguielement.estimation.finishedCallback = self.finishedCallback
        self.estimationguielement.estimation.errorCallback = self.errorCallback
        self.estimationguielement.estimation.run()

    def pause(self):
        self.estimationguielement.estimation.pause()

    def resume(self):
        self.estimationguielement.estimation.resume()

    def cancel(self):
        self.estimationguielement.estimation.cancel()

    def progressCallback(self,percent):
        print "Ping From Estimation"
        self.emit(SIGNAL("estimationPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Estimation"
        else:
            print "Error returned from Estimation"
        self.emit(SIGNAL("estimationFinished(PyQt_PyObject)"),success)

    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("estimationError(PyQt_PyObject)"),errorMessage)


class OpusEstimation(object):
    def __init__(self,xmltreeobject,xml_path, model_name):
        self.xmltreeobject = xmltreeobject
        self.xml_path = xml_path
        self.er = None
        self.progressCallback = None
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.statusfile = None
        self.firstRead = True
        self.running = False
        self.paused = False
        self.cancelled = False
        self.statusfile = None
        self.model_name = model_name

    def pause(self):
        self.paused = True
        print "Pause pressed"
        # Can access the estimation manager via self.er

    def resume(self):
        self.paused = False
        print "Resume pressed"
        # Can access the estimation manager via self.er

    def cancel(self):
        self.running = False
        self.paused = False
        self.cancelled = True
        print "Cancel pressed"
        # Can access the estimation manager via self.er

    def run(self):
        # Start the estimation. This code adapted from urbansim/tools/start_estimation.py
        # statusdir is a temporary directory into which to write a status file
        # regarding the progress of the simulation - the progress bar reads this file
        statusfile = None
        succeeded = False
        try:
            fileNameInfo = QFileInfo(self.xml_path)
            filename = fileNameInfo.absoluteFilePath().trimmed()
            xml_config = self.xmltreeobject.toolboxbase.opusXMLTree
            estimation_section = xml_config.get_section('model_manager/estimation')
            estimation_config = estimation_section['estimation_config']
            self.config = estimation_config
            # TODO: put save_estimation results etc into config
            save_results = estimation_section['save_estimation_results']
            model_name = self.model_name
#                for model_name in estimation_config['models_to_estimate']:
            # If we've paused the estimation, wait 10 seconds, and see if we are unpaused.  If we've cancelled,
            # exit the loop.  Note that this is a fairly coarse level of pause/resume/stop (at the level of
            # estimating an entire model, rather than a bit of a model).
            while self.paused and not self.cancelled:
                time.sleep(10)
            if not self.cancelled:
                
                if type(model_name) == dict:
                    for name, group_members in model_name.items():
                        self.__class__.er = EstimationRunner(model=name, 
                                              xml_configuration=xml_config, 
                                              model_group = group_members['group_members'],
                                              configuration=None, 
                                              save_estimation_results=save_results)
                    self.running = True
                    self.er.estimate()
                    self.running = False
                else:
                    self.er = EstimationRunner(model=model_name, xml_configuration=xml_config, configuration=None, save_estimation_results=save_results)
                    self.running = True
                    self.er.estimate()
                    self.running = False
                succeeded = True
        except:
            succeeded = False
            self.running = False
            errorInfo = formatExceptionInfo(custom_message = 'Unexpected Error From Estimation')
            self.errorCallback(errorInfo)
        if statusfile is not None:
            os.remove(statusfile)
        self.finishedCallback(succeeded)

    def _compute_progress(self):
        if self.statusfile is None:
            return {"percentage":0,"message":"Estimation initializing..."}
        # Compute percent progress for the progress bar.
        try:
            # Need to calculate the percentage here...
            return {"percentage":percentage,"message":message}
        except IOError:
            return {"percentage":0,"message":"Estimation initializing..."}

    def _get_current_log(self, key):
        newKey = key
        # We attempt to keep up on the current progress of the model run.  We pass into this
        # function an initial "key" value of 0 and expect to get back a new "key" after the
        # function returns.  It is up to us in this function to use this key to determine
        # what has happened since last time this function was called.
        # In this example we use the key to indicate where in a logfile we last stopped reading
        # and seek into that file point and read to the end of the file and append to the
        # log text edit field in the GUI.
        if self.config is not None and 'cache_directory' in self.config:
            try:
                base_year = self.config['base_year']
                f = open(os.path.join(self.config['cache_directory'],'year_%d_log.txt' % base_year))
                f.seek(key)
                lines = f.read()
                newKey = f.tell()
                if newKey != key:
                    self.guiElement.logText.append(lines)
                f.close()
            except IOError:
                if self.firstRead == True:
                    self.guiElement.logText.append("No logfile yet")
                    self.firstRead = False
                else:
                    self.guiElement.logText.insertPlainText(QString("."))
            #self.guiElement.logText.append("ping")
        return newKey
