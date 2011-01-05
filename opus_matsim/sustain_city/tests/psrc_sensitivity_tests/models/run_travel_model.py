# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os
from opus_matsim.sustain_city.models.pyxb_xml_parser.config_object import MATSimConfigObject

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """
    def __init__(self):
        """Constructor
        """
        self.matsim_config_destination = None  # path to generated matsim config xml
        self.matsim_config_name = None  # matsim config xml name
        self.matsim_config_full = None  # concatination of matsim config path and name

    def run(self, config, year):
        """Running MATSim.  A lot of paths are relative; the base path is ${OPUS_HOME}/opus_matsim.  As long as ${OPUS_HOME}
        is correctly set and the matsim tarfile was unpacked in OPUS_HOME, this should work out of the box.  There may eventually
        be problems with the java version.
        """

        logger.start_block("Starting RunTravelModel.run(...)")
        
        # tnicolai :for debugging
        #try:
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        self.setUp( config )
        
        config_obj = MATSimConfigObject(config, year, self.matsim_config_full)
        config_obj.marschall()
        
        # tnicolai: original call
        #cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
        #        'opus_home': os.environ['OPUS_HOME'],
        #        'vmargs': "-Xmx2000m",
        #        'classpath': "libs/log4j/log4j/1.2.15/log4j-1.2.15.jar:libs/jfree/jfreechart/1.0.7/jfreechart-1.0.7.jar:libs/jfree/jcommon/1.0.9/jcommon-1.0.9.jar:classesMATSim:classesToronto:classesTNicolai:classesKai:classesEntry", #  'classpath': "classes:jar/MATSim.jar",
        #        'javaclass': "playground.tnicolai.urbansim.cupum.MATSim4UrbanSimCUPUM",
        #        'matsim_config_file': self.matsim_config_full } 
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': os.environ['OPUS_HOME'],
                'vmargs': "-Xmx2000m",
                'classpath': "libs/log4j/log4j/1.2.15/log4j-1.2.15.jar:libs/jfree/jfreechart/1.0.7/jfreechart-1.0.7.jar:libs/jfree/jcommon/1.0.9/jcommon-1.0.9.jar:classesMATSim:classesToronto:classesTNicolai:classesKai:classesEntry", #  'classpath': "classes:jar/MATSim.jar",
                'javaclass': "playground.tnicolai.urbansim.cupum.MATSim4UrbanSimCUPUM",
                'matsim_config_file': self.matsim_config_full } 
        
        # tnicolai : test for matsim jar execution ...
        #cmd = """cd %(opus_home)s ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
        #        'opus_home': '/Users/thomas/Desktop/export',
        #        'vmargs': "-Xmx2000m",
        #        'classpath': "matsim4urbansim20110103.jar",
        #        'javaclass': "playground.tnicolai.urbansim.cupum.MATSim4UrbanSimCUPUM",
        #        'matsim_config_file': self.matsim_config_full } 
        
        logger.log_status('Running command %s' % cmd ) 
        
        cmd_result = os.system(cmd)
        if cmd_result != 0:
            error_msg = "Matsim Run failed. Code returned by cmd was %d" % (cmd_result)
            logger.log_error(error_msg)
            logger.log_error("Note that currently (dec/08), paths in the matsim config files are relative to the opus_matsim root,")
            logger.log_error("  which is one level 'down' from OPUS_HOME.")
            raise StandardError(error_msg)        
        
        logger.end_block()
        
    def setUp(self, config):
        """ create MATSim config data
        """
        self.matsim_config_destination = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "matsim_config")
        if not os.path.exists(self.matsim_config_destination):
            try: os.mkdir(self.matsim_config_destination)
            except: pass
        self.matsim_config_name = config['project_name'] + "_matsim_config.xml"
        self.matsim_config_full = os.path.join( self.matsim_config_destination, self.matsim_config_name  )

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
