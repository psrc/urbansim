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
    from opus_core.tools.start_run import StartRunOptionGroup
    from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed, SimulationRunError
    from opus_gui.configurations.xml_configuration import XMLConfiguration
    WithOpus = True
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class OpusModel(object):
    def __init__(self,parent,xml_path):
        self.parent = parent
        self.xml_path = xml_path
        self.progressCallback = parent.progressCallback
        self.finishedCallback = parent.finishedCallback

    def run(self):
        if WithOpus:
            # Run the Eugene model using the XML version of the Eugene configuration.
            # This code adapted from opus_core/tools/start_run.py
            statusfile = None
            try:
                option_group = StartRunOptionGroup()
                parser = option_group.parser
                # simulate 0 command line arguments by passing in []
                (options, args) = parser.parse_args([])
                run_manager = option_group.get_run_manager(options)
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(QString(self.xml_path))
                fileNameAbsolute = fileNameInfo.absoluteFilePath()
                config = XMLConfiguration(str(fileNameAbsolute))
                insert_auto_generated_cache_directory_if_needed(config)
                (self.start_year, self.end_year) = config['years']
                cache_dir = config['cache_directory']
                statusfile = os.path.join(cache_dir, 'status.txt')
                self.statusfile = statusfile
                config['status_file_for_gui'] = statusfile
                run_manager.run_run(config)
                succeeded = True
            except SimulationRunError:
                succeeded = False
            if statusfile is not None and os.path.exists(statusfile):
                os.remove(statusfile)
            self.parent.finishedCallback(succeeded)
        else:
            pass
        
    def _compute_progress(self, statusfile):
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

