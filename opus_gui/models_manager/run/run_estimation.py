# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QThread, SIGNAL, QFileInfo, QString

import os, time

from opus_gui.util.exception_formatter import formatExceptionInfo
from urbansim.estimation.estimation_runner import EstimationRunner

class RunEstimationThread(QThread):
    def __init__(self, mainwindow, estimationguielement, xml_file = None):
        QThread.__init__(self, mainwindow)
        self.estimationguielement = estimationguielement
        # self.xml_file = xml_file

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
    # xml_config, model_name, model_group
    def __init__(self, xml_config, model_name, model_group = None):
        '''
        @param xml_config (XMLConfiguration): xml configuration object for the model
        @param model_name (String): the name of the model to run
        @param model_group (String): name of the sub model group to run
        '''

        dummy_callback = lambda x: None

        self.xml_config = xml_config
        self.model_name = model_name
        self.model_group = model_group

        self.er = None
        self.progressCallback = dummy_callback
        self.finishedCallback = dummy_callback
        self.errorCallback = dummy_callback

        self.guiElement = None
        self.config = None
        self.statusfile = None
        self.firstRead = True
        self.running = False
        self.paused = False
        self.cancelled = False
        self.statusfile = None

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
            # get the configuration for estimations
            estimation_section = self.xml_config.get_section('model_manager/model_system/')
            estimation_config = estimation_section['estimation_config']
            self.config = estimation_config
            # TODO: put this option into post run dialog
            save_results = estimation_config['save_estimation_results']

            # If we've paused the estimation, wait 10 seconds, and see if we are unpaused.  If we've cancelled,
            # exit the loop.  Note that this is a fairly coarse level of pause/resume/stop (at the level of
            # estimating an entire model, rather than a bit of a model).
            while self.paused and not self.cancelled:
                time.sleep(10)
            if not self.cancelled:
                self.er = EstimationRunner(model = self.model_name,
                                           specification_module = None,
                                           xml_configuration = self.xml_config,
                                           model_group = self.model_group,
                                           configuration = None,
                                           save_estimation_results=save_results)
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
        #TODO: Compute percent progress for the progress bar.
        percentage = 0
        message = 'Estimation initializing...'
        return {"percentage":percentage,"message":message}

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
