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

import os

from opus_gui.results.indicator_framework.maker.maker import Maker
from opus_gui.results.gui_result_interface.indicator_framework_interface import IndicatorFrameworkInterface
from opus_gui.exceptions.formatter import formatExceptionInfo
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper


class OpusResultGenerator(object):
    
    def __init__(self, toolboxStuff):
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.cache_directory = None
        self.firstRead = True
        self.toolboxStuff = toolboxStuff
        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = toolboxStuff)
        self.interface = IndicatorFrameworkInterface(toolboxStuff = toolboxStuff)
        self.computed_indicators = []
        
    def set_data(self,
                 source_data_name,
                 indicator_name,
                 dataset_name,
                 years,
                 cache_directory = None,
                 indicator_definition = None):
        self.source_data_name = source_data_name
        self.indicator_name = indicator_name
        self.dataset_name = dataset_name
        self.years = years
        self.cache_directory = cache_directory
        self.indicator_definition = indicator_definition
        
    def run(self, args = {}, raise_exception = False):
        
        succeeded = False
        try:
#                try:
#                    import pydevd;pydevd.settrace()
#                except:
#                    pass
            
            self._generate_results()
            succeeded = True
        except Exception, e:
            succeeded = False
            errorinfo = formatExceptionInfo(custom_message = 'Unexpected error in the result generator')
            if self.errorCallback is not None:
                self.errorCallback(errorinfo)
            if raise_exception:
                raise e
        if self.finishedCallback is not None:
            self.finishedCallback(succeeded)

    def _generate_results(self):

        self.computed_indicators = []
        
        source_data = self.interface.get_source_data(
                             source_data_name = self.source_data_name, 
                             years = self.years)

        self.cache_directory = source_data.cache_directory

        indicator = self.interface.get_indicator(
                                 indicator_name = self.indicator_name,
                                 dataset_name = self.dataset_name,
                                 indicator_definition = self.indicator_definition)
        
        maker = Maker(project_name = os.environ['OPUSPROJECTNAME'], expression_library = self.toolboxStuff.opusXMLTree.get_expression_library())

        try:
            import pydevd;pydevd.settrace()
        except:
            pass

        computed_indicator = maker.create(indicator = indicator,
                                          source_data = source_data)
        self.computed_indicators.append(computed_indicator)
#                        
    def _get_current_log(self, key):
        newKey = key
        # We attempt to keep up on the current progress of the model run.  We pass into this
        # function an initial "key" value of 0 and expect to get back a new "key" after the
        # function returns.  It is up to us in this function to use this key to determine
        # what has happened since last time this function was called.
        # In this example we use the key to indicate where in a logfile we last stopped reading
        # and seek into that file point and read to the end of the file and append to the
        # log text edit field in the GUI.
        if self.cache_directory is not None:
            try:
                log_file = os.path.join(self.cache_directory,
                                      'indicators',
                                      'indicators.log')
                
                f = open(log_file)
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
                    from PyQt4.QtCore import QString
                    self.guiElement.logText.insertPlainText(QString("."))
            #self.guiElement.logText.append("ping")
        return newKey
