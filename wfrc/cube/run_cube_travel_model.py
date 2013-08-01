# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from numpy import array, float32, ones
import os, sys, time
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel

class RunCubeTravelModel(RunTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config = config["travel_model_configuration"]
        self.prepare_for_run(tm_config, year)
        
        base_dir = tm_config.get('travel_model_base_directory')
        year_dir = tm_config[year]['year_dir']
        batch_file = tm_config.get('batch_file')
        #project_year_dir = get_project_year_dir(tm_config, year)
        
        logger.log_status('Start travel model from directory %s for year %d' % (base_dir, year))

        logger.log_status('Running travel model ...')

        os.system('%s/%s/%s' % (base_dir, year_dir, batch_file))
        time.sleep(1)

    def prepare_for_run(self, config, year, check_tcw_process=False):
        """before calling travel model macro, check if transcad GUI is running, 
        if not, try to start transcad binary process"""
        ## TODO: TransCAD COM server is very picky about tcw.exe process in memory
        ## as of April 2007, a tcw process started by python won't work
        ## so manually start TransCAD program is needed before running this script
        
        return 

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    
#    options.resources_file_name = "c:\urbansim_cache\semcog_test_tm.pickle"
#    options.year = 2001   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    RunCubeTravelModel().run(resources, options.year)    