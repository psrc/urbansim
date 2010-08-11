# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os
import opus_matsim.sustain_city.tests as test_path
import shutil

class RunTravelModelTest(AbstractTravelModel):
    """ Run the dummy travel model.
    """

    def run(self, config, year):

        logger.start_block("Starting RunTravelModelTest.run(...)")
        
        travel_data_path = os.path.join( test_path.__path__[0], 'data', 'travel_cost')
        if not os.path.exists(travel_data_path):
            raise StandardError('Travel data not found: %s' % travel_data_path)
        
        logger.log_status('Loading travel_data ...')
        travel_data = os.path.join(travel_data_path, 'travel_data_small.csv')
        
        output_directory = os.path.join( config['root'], 'opus_matsim', 'tmp')
        if not os.path.exists(output_directory):
            raise StandardError('Travel data not found: %s' % output_directory)
        
        destination = os.path.join( output_directory, 'travel_data.csv')
        
        logger.log_status('Copying travel_data to: %s' % destination)
        shutil.copy(travel_data, destination)
        
        logger.end_block()

# called from the framework via main!
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

    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    RunTravelModelTest().run(resources, options.year)    
