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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, sys

from opus_core.logger import logger


class OpusGuiThread(QThread):

    def __init__(self, parentThread, parentGuiElement, thread_object):
        #parent is a GenerateResultsForm
        QThread.__init__(self, parentThread)
        self.parentGuiElement = parentGuiElement
        self.thread_object = thread_object
        
    def run(self, 
            progressCallback = None,
            finishedCallback = None,
            errorCallback = None,
            args = {}):
    
        
        if progressCallback is None:
            progressCallback = self.progressCallback
        if finishedCallback is None:
            finishedCallback = self.finishedCallback
        if errorCallback is None:
            errorCallback = self.errorCallback
            
        self.thread_object.progressCallback = progressCallback
        self.thread_object.finishedCallback = finishedCallback
        self.thread_object.errorCallback = errorCallback
        self.thread_object.run(args)
        
    def progressCallback(self,percent):
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            logger.log_note("Success returned from results")
        else:
            logger.log_warning("Error returned from results")
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)

    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("runError(PyQt_PyObject)"),errorMessage)
