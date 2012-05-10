# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
import subprocess

class RunMalta(AbstractTravelModel):
    """
    """

    def run(self, config, year, iteration):
        """ 
        """
        
        tm_config = config['travel_model_configuration']

    # Altering the iteration count in the config file for MALTA
    fileLoc = tm_config.get("malta_project")
    fileEntries = []
    fileMaltaConfig = open(fileLoc, 'r')
    for line in fileMaltaConfig:
        fileEntries.append(line)
    fileMaltaConfig.close()

    fileMaltaConfig = open(fileLoc, 'w')
    fileMaltaConfig.write(fileEntries[0])
    fileMaltaConfig.write('%d\n' %(iteration+1))
    fileMaltaConfig.close()
    

        cmd = "%s %s" % (tm_config["malta_path"], tm_config.get("malta_project"))
        logger.log_status("Start MALTA...")
    
        try:
            stdout, stderr= subprocess.Popen(cmd,
                                         shell = True
                                     ).communicate()
        except:
            print "Error occured when running MALTA"
            raise
        """
        if stderr:
            print "Error occured when running MALTA"
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
    RunMalta().run(resources, options.year)
