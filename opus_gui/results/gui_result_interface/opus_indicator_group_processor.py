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

try:
    WithOpus = True
    from opus_gui.results.gui_result_interface.opus_result_generator import OpusResultGenerator
    from opus_gui.results.gui_result_interface.opus_result_visualizer import OpusResultVisualizer
    from opus_gui.results.gui_result_interface.opus_gui_thread import formatExceptionInfo
    
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs for opus indicator group processor"

class OpusIndicatorGroupProcessor(object):
    def __init__(self, 
                 toolboxStuff,
                 kwargs = None):
          
        self.generator = OpusResultGenerator(
           toolboxStuff = toolboxStuff                                            
        )
          
        self.visualizer = OpusResultVisualizer(
           toolboxStuff = toolboxStuff,
           indicator_type = None,
           indicators = None,
           kwargs = kwargs                     
        )
        self.finishedCallback = None
        self.errorCallback = None
            
    def set_data(self,                  
                 indicator_defs, 
                 source_data_name,
                 years):
        
        self.indicator_defs = indicator_defs
        self.years = years
        self.source_data_name = source_data_name        
        
    def run(self):
        succeeded = False
        
        try:
            self.visualizations = []
            for (visualization_type, dataset_name), indicators in self.indicator_defs.items():
                indicator_results = []
                for indicator_name in indicators:
                    try:
                        self.generator.set_data(self.source_data_name, 
                                                indicator_name, 
                                                dataset_name, 
                                                self.years)
                        self.generator.run()
                        indicator = {'indicator_name':indicator_name,#self.generator.last_added_indicator_result_name,
                                     'dataset_name':dataset_name,
                                     'source_data_name':self.source_data_name,
                                     'years':self.years}
                        indicator_results.append(indicator)
                        
                    except:
                        print 'could not generate indicator %s'%indicator_name
                self.visualizer.indicator_type = visualization_type
                self.visualizer.indicators = indicator_results
                try:
                    import pydevd;pydevd.settrace()
                except:
                    pass
                self.visualizer.run()
                self.visualizations.append((visualization_type, self.visualizer.get_visualizations()))
            
            succeeded = True
        except:
            succeeded = False
            errorInfo = formatExceptionInfo()
            errorString = "Unexpected Error From Model :: " + str(errorInfo)
            print errorInfo
            self.errorCallback(errorString)

        self.finishedCallback(succeeded)
    
    def get_visualizations(self): 
        return self.visualizations
    