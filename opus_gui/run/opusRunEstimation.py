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
    import os
    from inprocess.configurations.xml_configuration import XMLConfiguration
    # from psrc_parcel.estimation.run_estimation import EstimationRunner
    from inprocess.configurations.gui_estimation_runner import EstimationRunner
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
        #self.thread = RunModelThread(self.parent.parent,self.xml_path)
        self.progressCallback = None
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.statusfile = None
        self.firstRead = True
    
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
                parcelfile = fileNameInfo.absoluteFilePath().trimmed()
                print parcelfile
                xml_config = XMLConfiguration(parcelfile)
                estimation_section = xml_config.get_estimation_section()
                estimation_config = estimation_section['estimation_config']
                # TODO: put save_estimation results etc into config
                for model_name in estimation_config['models_to_estimate']:
                    model_config = estimation_config['model_parameters'][model_name]
                    model = (model_config['abbreviation'], model_config['full_name'])
                    if 'location' in model_config:
                        model = model , (model_config['location'], model_config['add_member_prefix'])
                    specification = xml_config.get_estimation_specification(model_config['full_name'])
                    er = EstimationRunner()
                    er.run_estimation(estimation_config, model,
                                      specification, save_estimation_results=True, diagnose=False)
                succeeded = True
            except:
                succeeded = False
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
            # We attempt to keep up on the current progress
            pass
        return newKey
