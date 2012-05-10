# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
import subprocess, sys

class RunOpenamos(AbstractTravelModel):
    """
    """

    def run(self, config, year, iteration, setupCache, backupResults):
        """ 
        """
        
        tm_config = config['travel_model_configuration']
        xml_config = tm_config.get("openamos_configuration")

        if tm_config.has_key("openamos_module"):
            python_cmd = "%s -m %s %s %s %s %s" % (sys.executable, tm_config["openamos_module"], xml_config, iteration, setupCache, backupResults)
        elif tm_config.has_key("openamos_path"):
            python_cmd = "%s %s -file %s -it %s -crca %s -bkup %s" % (sys.executable, tm_config["openamos_path"], xml_config, iteration, setupCache, backupResults)
        else:
            raise ValueError("Either openamos_module or openamos_path needs to be specified in travel_model_configuration.")
            
        logger.log_status("Start OpenAMOS...%s" %python_cmd)

        try:
            stdout, stderr= subprocess.Popen(python_cmd,
                                             shell = True
                                             ).communicate()
        except:
            print "Error occured when running OpenAMOS"
            raise

    
        """
        if stderr:
            print "Error occured when running OpenAMOS"
            print stderr
            sys.exit(1)
        """
if __name__ == "__main__":
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
    RunOpenamos().run(resources, options.year)    
