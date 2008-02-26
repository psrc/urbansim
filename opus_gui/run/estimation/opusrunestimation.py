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
import os, sys, time


try:
    import os
    from opus_core.configurations.xml_configuration import XMLConfiguration
    # from psrc_parcel.estimation.run_estimation import EstimationRunner
    from gui_estimation_runner import EstimationRunner
    WithOpus = True
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class RunEstimationThread(QThread):
    def __init__(self, parentThread,parent,xml_file):
        QThread.__init__(self, parentThread)
        self.parent = parent
        self.xml_file = xml_file

    def run(self):
        self.parent.progressBar.setRange(0,100)
        self.parent.estimation.progressCallback = self.progressCallback
        self.parent.estimation.finishedCallback = self.finishedCallback
        self.parent.estimation.errorCallback = self.errorCallback
        self.parent.estimation.run()

    def pause(self):
        self.parent.estimation.pause()

    def resume(self):
        self.parent.estimation.resume()

    def cancel(self):
        self.parent.estimation.cancel()

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
    def __init__(self,parent,xml_path):
        self.parent = parent
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
        if WithOpus:
            # Run the Eugene model using the XML version of the Eugene configuration.
            # This code adapted from opus_core/tools/start_run.py
            # statusdir is a temporary directory into which to write a status file
            # regarding the progress of the simulation - the progress bar reads this file
            statusfile = None
            statusdir = None
            succeeded = False
            try:
                fileNameInfo = QFileInfo(self.xml_path)
                filename = fileNameInfo.absoluteFilePath().trimmed()
                print filename
                xml_config = XMLConfiguration(str(filename))
                estimation_section = xml_config.get_section('model_manager/estimation')
                estimation_config = estimation_section['estimation_config']
                self.config = estimation_config
                # TODO: put save_estimation results etc into config
                for model_name in estimation_config['models_to_estimate']:
                    # If we've paused the estimation, wait 10 seconds, and see if we are unpaused.  If we've cancelled,
                    # exit the loop.  Note that this is a fairly coarse level of pause/resume/stop (at the level of
                    # estimating an entire model, rather than a bit of a model).
                    while self.paused and not self.cancelled:
                        time.sleep(10)
                    if self.cancelled:
                        break
                    model_config = estimation_config['model_parameters'][model_name]
                    model = (model_config['abbreviation'], model_config['full_name'])
                    if 'location' in model_config:
                        model = model , (model_config['location'], model_config['add_member_prefix'])
                    specification = xml_config.get_estimation_specification(model_config['full_name'])
                    self.er = EstimationRunner()
                    self.running = True
                    self.er.run_estimation(estimation_config, model,
                                      specification, save_estimation_results=False, diagnose=False)
                    self.running = False
                succeeded = True
            except:
                succeeded = False
                self.running = False
                errorInfo = self.formatExceptionInfo()
                errorString = "Unexpected Error From Estimation :: " + str(errorInfo)
                print errorInfo
                self.errorCallback(errorString)
            if statusfile is not None:
                os.remove(statusfile)
            self.finishedCallback(succeeded)
        else:
            pass

    def _compute_progress(self, statusfile):
        if statusfile is None:
            return {"percentage":0,"message":"Estimation initializing..."}
        if WithOpus:
            # Compute percent progress for the progress bar.
            try:
                # Need to calculate the percentage here...
                return {"percentage":percentage,"message":message}
            except IOError:
                return {"percentage":0,"message":"Estimation initializing..."}

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
                    f = open(os.path.join(self.config['cache_directory'],'year_2000_log.txt'))
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
