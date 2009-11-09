# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, float32, ones
from os.path import join
import os, sys
from opus_core.logger import logger
from travel_model.models.run_travel_model import RunTravelModel
from opus_core.misc import module_path_from_opus_path
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class RunSanfranciscoTravelModel(RunTravelModel):
    """Run the travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """Runs the travel model, using appropriate info from config. 
        """
        tm_config = config["travel_model_configuration"]
        tm_data_dir = tm_config["directory"]

        year_dir = tm_config[year]  #'2001'

        dir_part1, dir_part2 = os.path.split(tm_config['travel_model_command'])
        
        cmdline =  os.path.join(dir_part1, year_dir, dir_part2)
        logger.log_status('Running travel model with %s' % cmdline)
        os.chdir(os.path.join(dir_part1, year_dir))
        os.system(cmdline)

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
    
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                           
                         in_storage=AttributeCache())

    RunSanfranciscoTravelModel().run(resources, options.year)    
