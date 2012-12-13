# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os, sys
from opus_matsim.sustain_city.models.pyxb_xml_parser.config_object import MATSimConfigObject
from opus_matsim.models.org.constants import matsim4opus
from opus_core import paths

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """
    def __init__(self):
        """Constructor
        """
        self.matsim_config_destination = None   # path to generated matsim config xml
        self.matsim_config_name = None          # matsim config xml name
        self.matsim_config_full = None          # concatenation of matsim config path and name
        self.test_parameter = ""                # optional parameter for testing and debugging purposes

    def run(self, config, year):
        """Running MATSim.  A lot of paths are relative; the base path is ${OPUS_HOME}/opus_matsim.  As long as ${OPUS_HOME}
        is correctly set and the matsim tar-file was unpacked in OPUS_HOME, this should work out of the box.  There may eventually
        be problems with the java version.
        """

        logger.start_block("Starting RunTravelModel.run(...)")
        
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        config_obj = MATSimConfigObject(config, year)
        self.matsim_config_full = config_obj.marschall()
        
        # check for test parameter
        tmc = config['travel_model_configuration']
        if tmc['matsim4urbansim'].get('test_parameter') != None:
            self.test_parameter = tmc['matsim4urbansim'].get('test_parameter')
        # change to directory opus_matsim
        os.chdir( paths.get_opus_home_path(matsim4opus) )
        
        # int cmd
        cmd = ""
        # calling travel model with cmd command
        if sys.platform.lower() == 'win32': 
            # reserve memory for java
            xmx = '-Xmx1500m'# Windows can't reserve more than 1500m
            logger.log_note("Note that Java for Windows can't reserve more than 1500 MB of memory to run MATSim!!!")
            cmd = """java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s %(test_parameter)s""" % {
                'vmargs': xmx, 
                'classpath': "jar/matsim.jar:jar/contrib/matsim4urbansim.jar",
                'javaclass': "org.matsim.contrib.matsim4opus.matsim4urbansim.MATSim4UrbanSimParcel",
                'matsim_config_file': self.matsim_config_full,
                'test_parameter': self.test_parameter } 
        else:
            # reserve memory for java
            xmx = '-Xmx4000m'
            cmd = """java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s %(test_parameter)s""" % {
                'vmargs': xmx, 
                'classpath': "jar/matsim.jar:jar/contrib/matsim4urbansim.jar",
                'javaclass': "org.matsim.contrib.matsim4opus.matsim4urbansim.MATSim4UrbanSimParcel",
                'matsim_config_file': self.matsim_config_full,
                'test_parameter': self.test_parameter } 
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "MATSim Run failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            logger.log_error("Note that paths in the matsim config files are relative to the matsim4opus root,")
            logger.log_error("which is one level 'down' from OPUS_HOME.")
            raise StandardError(error_msg)        
        
        logger.end_block()

# called from opus via main!
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
    RunTravelModel().run(resources, options.year)    
