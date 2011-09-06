# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys, opus_matsim, shutil
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_matsim.models.pyxb_xml_parser.config_object import MATSimConfigObject

class RunDummyTravelModel(AbstractTravelModel):
    """Run a dummy travel model.  This is used in the test, where this is run in lieu of the Java code.
    """
    
    def __init__(self):
        """Constructor
        """
        self.matsim_config_destination = None  # path to generated matsim config xml
        self.matsim_config_name = None  # matsim config xml name
        self.matsim_config_full = None  # concatenation of matsim config path and name
        self.test_parameter = ""        # optional parameter for testing and debugging purposes
    
    def run(self, config, year):
        """
        """
        logger.start_block("Starting RunDummyTravelModel.run(...)")
        
        print >> sys.stderr, "\nThis should also check if get_cache_data_into_matsim did something reasonable"
        
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        self.__setUp( config )
        
        config_obj = MATSimConfigObject(config, year, self.matsim_config_full)
        config_obj.marschall()        
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s %(test_parameter)s""" % {
                'opus_home': os.environ['OPUS_HOME'],
                'vmargs': "-Xmx2000m", # set to 8GB on math cluster and 2GB on Notebook
                'classpath': "jar/matsim4urbansim.jar",
                'javaclass': "playground.run.Matsim4Urbansim", # "playground.tnicolai.urbansim.cupum.MATSim4UrbansimCUPUM",
                'matsim_config_file': self.matsim_config_full,
                'test_parameter': self.test_parameter } 
        
        logger.log_status('would normally run command %s' % cmd )
        
        in_file_name = os.path.join(opus_matsim.__path__[0], 'tests', 'testdata', 'travel_data.csv' )
        out_file_name = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp', 'travel_data.csv' )
        
        print "Copying dummy travel data ..."
        shutil.copyfile(in_file_name, out_file_name)
        print "... done."
                
    def __setUp(self, config):
        """ create MATSim config data
        """
        self.matsim_config_destination = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "matsim_config")
        if not os.path.exists(self.matsim_config_destination):
            try: os.mkdir(self.matsim_config_destination)
            except: pass
        self.matsim_config_name = config['project_name'] + "_matsim_config.xml"
        self.matsim_config_full = os.path.join( self.matsim_config_destination, self.matsim_config_name  )
        
        tmc = config['travel_model_configuration']
        if tmc['matsim4urbansim'].get('test_parameter') != None:
            self.test_parameter = tmc['matsim4urbansim'].get('test_parameter')

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
    RunDummyTravelModel().run(resources, options.year)    
