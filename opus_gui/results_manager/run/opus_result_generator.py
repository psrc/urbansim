# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker
from opus_gui.results_manager.run.indicator_framework_interface import IndicatorFrameworkInterface
from opus_gui.util.exception_formatter import formatExceptionInfo

class OpusResultGenerator(object):

    def __init__(self, project, ignore_cache = False):
        self.project = project
        # Dummy callbacks
        self.finishedCallback = lambda x: ()
        self.errorCallback = lambda x: ()
        self.guiElement = None
        self.cache_directory = None
        self.firstRead = True
        self.interface = IndicatorFrameworkInterface(project)
        self.computed_indicators = []
        self.ignore_cache = ignore_cache

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
        except Exception as e:
            succeeded = False
            errorinfo = formatExceptionInfo(custom_message = 'Unexpected error in the result generator')
            self.errorCallback(errorinfo)
            if raise_exception:
                raise e
        self.finishedCallback(succeeded)

    def _generate_results(self):

        self.computed_indicators = []

        source_data = self.interface.get_source_data(
                             source_data_name = self.source_data_name,
                             years = self.years,
                             cache_directory = self.cache_directory
        )

        self.cache_directory = source_data.cache_directory

        indicator = self.interface.get_indicator(
                                 indicator_name = self.indicator_name,
                                 dataset_name = self.dataset_name,
                                 indicator_definition = self.indicator_definition)

        maker = Maker(self.project.name, False,
                      self.project.xml_config.get_expression_library())

#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass

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
                    self.guiElement.logText.insertPlainText(".")
            #self.guiElement.logText.append("ping")
        return newKey
