# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os
import sys

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """

    def run(self, config, year):
        """Running MATSim.  A lot of paths are relative; the base path is ${OPUS_HOME}/opus_matsim.  As long as ${OPUS_HOME}
        is correctly set and the matsim tarfile was unpacked in OPUS_HOME, this should work out of the box.  There may eventually
        be problems with the java version.
        """
        
        logger.start_block("Starting RunTravelModel.run(...)")
        
        travel_model_configuration = config['travel_model_configuration']

        # The default config file name
        matsim_config_filename = travel_model_configuration['matsim_config_filename']
        
        # over-written if there is a specific config file name for the year:
        if travel_model_configuration[year]['matsim_config_filename']:
            matsim_config_filename = travel_model_configuration[year]['matsim_config_filename']
        
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s --year=%(year)i --samplingRate=%(sampling_rate)f""" % {
                'opus_home': os.environ['OPUS_HOME'],
                'vmargs': "-Xmx2000m",
                'classpath': "classes:jar/MATSim.jar",
                'javaclass': "playground.run.Matsim4Urbansim",
                'matsim_config_file': os.path.join( os.environ['OPUS_HOME'], "opus_matsim", matsim_config_filename), 
                'sampling_rate': config['travel_model_configuration']['sampling_rate'],
                'year': year } 
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "Matsim Run failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            logger.log_error("Note that currently (dec/08), paths in the matsim config files are relative to the opus_matsim root,")
            logger.log_error("  which is one level 'down' from OPUS_HOME.")
            raise StandardError(error_msg)        
        
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
    RunTravelModel().run(resources, options.year)    
