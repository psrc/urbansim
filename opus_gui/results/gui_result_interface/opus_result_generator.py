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

import os, sys

try:
    WithOpus = True
    from opus_gui.results.indicator_framework.maker.maker import Maker
    from opus_gui.results.gui_result_interface.indicator_framework_interface import IndicatorFrameworkInterface
    from opus_gui.results.gui_result_interface.opus_gui_thread import formatExceptionInfo
    from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs for opus result generator"


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
                 cache_directory = None):
        self.source_data_name = source_data_name
        self.indicator_name = indicator_name
        self.dataset_name = dataset_name
        self.years = years
        self.cache_directory = cache_directory
        
    def run(self, args = {}):
        
        if WithOpus:
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
                (exception_type, args, trace) = formatExceptionInfo()
                error_characterization = 'Unexpected Error From Model'
                error_message = str(e)
                errorString = '%s :: %s \n%s\n%s%s'%(
                    error_characterization,
                    exception_type,
                    args,
                    ''.join(trace),
                    error_message                                   
                )
                print errorString
                if self.errorCallback is not None:
                    self.errorCallback(errorString)
            if self.finishedCallback is not None:
                self.finishedCallback(succeeded)
        else:
            pass

    def _generate_results(self):
#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass
        self.computed_indicators = []
        
        if self.cache_directory is not None:            
            source_data = self.interface.get_source_data(
                                         source_data_name = None,
                                         cache_directory = self.cache_directory, 
                                         years = self.years)
        else:
            source_data = self.interface.get_source_data(
                                         source_data_name = self.source_data_name, 
                                         years = self.years)

            self.cache_directory = source_data.cache_directory

        indicator = self.interface.get_indicator(
                                 indicator_name = self.indicator_name,
                                 dataset_name = self.dataset_name)
        
        maker = Maker()

        computed_indicator = maker.create(indicator = indicator, 
                                          source_data = source_data)
        self.computed_indicators.append(computed_indicator)
        name = '%s.%s.%s'%(self.indicator_name, 
            self.dataset_name, 
            self.source_data_name)
#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass
#        
        if self.source_data_name is not None:
            self.xml_helper.add_result_to_xml(result_name = name,
                                              source_data_name = self.source_data_name, 
                                              indicator_name = self.indicator_name, 
                                              dataset_name = self.dataset_name, 
                                              years = self.years)

        self.last_added_indicator_result_name = name
        
    def get_computed_indicators(self):
        return self.computed_indicators
                
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
                        self.guiElement.logText.insertPlainText(QString("."))
                #self.guiElement.logText.append("ping")
        return newKey
