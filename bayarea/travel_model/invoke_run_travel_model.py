# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger, block, log_block
from optparse import OptionParser
import os, sys
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration 
from opus_core.services.run_server.run_manager import RunManager

travel_model_year_mapping = {2018:2020,
                             2025:2035,
                             2035:2035,
                             2040:2040,
                             }

class TravelModelError(Exception):
    pass

@log_block()
def invoke_run_travel_model(config, year):
    """ 
    """

    tm_config = config['travel_model_configuration']
    scenario = tm_config['travel_model_scenario'] 
    try:
        travel_model_year = travel_model_year_mapping[year]
    except KeyError:
        logger.log_warning("no travel model year mapping for %d." % year)
        travel_model_year = year
    my_location = os.path.split(__file__)[0]
    script_filepath = os.path.join(my_location, "run_travel_model.py")
    cmd = "%s %s -s %s -y %s -n -e" % (sys.executable, script_filepath, scenario, travel_model_year)

    # form the desired output dir for the travel model data.  Make it look
    # like the urbansim run cache for easy association.  Note that we
    # explicitly use the forward slash instead of os.sep and friends
    # because the travel model is managed via ssh on a cygwin machine, not
    # run on the local machine.
    outdir = "runs/" + config['cache_directory'].split(os.sep)[-1]
    outdir = outdir + "/%d_%s" % (year, scenario)
    cmd = cmd + " -o " + outdir

    logger.log_status("Launching %s" % cmd)
    if os.system(cmd) != 0:
        raise TravelModelError

if __name__ == "__main__":
    from optparse import OptionParser
    from opus_core.resources import Resources
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", 
                      action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    invoke_run_travel_model(resources, options.year)    

