# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# PyQt4 includes for python bindings to QT

from PyQt4.QtCore import QThread, SIGNAL


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
#        if success:
#            logger.log_note("Success returned from results")
#        else:
#            logger.log_warning("Error returned from results")
        logger.log_note('Results finished.')
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)

    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("runError(PyQt_PyObject)"),errorMessage)
