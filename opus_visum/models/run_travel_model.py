# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
from visum_functions import load_version_file

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """

    def run(self, config, year):
        """Runs the VISUM executables, using appropriate info from config. 
        Assumes the VISUM input files are present. 
        Raise an exception if the VISUM run fails. 
        """
        tm_config = config['travel_model_configuration']
	
        #Get config params
        visum_dir, fileName = tm_config[year]['version']
	visum_version_number = tm_config['visum_version_number']
        
        #Startup Visum
        Visum = load_version_file(visum_dir, fileName)

        #Load procedure file and execute
        parFileName = tm_config[year]['procedure_file']	
        try:
	    Visum.Procedures.Open(parFileName)
	    Visum.Procedures.Execute()
        except Exception:
	    error_msg = "Loading and executing procedures file failed"
	    raise StandardError(error_msg)

	#Save version file
	#This saves over the existing version file
        try:
        	Visum.SaveVersion(fileName)
        except Exception:
        	error_msg = "Saving version file failed"
        	raise StandardError(error_msg)
	    
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
    RunTravelModel().run(resources, options.year)    
