# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from numpy import array, float32, ones
from os.path import join
import os
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        
        tm_config = config["travel_model_configuration"]
        tm_data_dir = tm_config["directory"]
        self.prepare_for_run(config, year)
        logger.log_status('Start travel model from directory %s for year %d' % (tm_data_dir, year))
        cmd_batch = self.create_travel_model_command_batch(tm_config, year, *args, **kwargs)
        logger.log_status('Running command %s' % cmd_batch)
        cmd_result = os.system(cmd_batch)
        if cmd_result != 0:
            error_msg = "Run travel model failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            raise StandardError(error_msg)

    def prepare_for_run(self, config, year):
        raise NotImplementedError, "subclass responsibility"
    
    def create_travel_model_command_batch(self, *args, **kwargs):
        """"""
        raise NotImplementedError, "subclass responsibility"
        

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.utils.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    RunTravelModel().run(resources, options.year)    
