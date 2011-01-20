# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os
from opus_matsim.sustain_city.models.pyxb_xml_parser import pyxb_matsim_config_parser
from lxml import etree

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """
    def __init__(self):
        """Constructor
        """
        
        # parameter for matsim execution
        self.firstRun = "FALSE"         # flag is true on the first run
        self.matsim_config_destination = None  # path to generated matsim config xml
        self.matsim_config_name = None  # matsim config xml name
        self.matsim_config_full = None  # concatination of matsim config path and name
        self.isTestRun          = None  # indicates wheter running the travel model is a test run
                                        # this flag is needed for test cases
        
        # parameter for matsim configuration
        self.network_file = None        # (relative) path to network xml file
        
        self.first_iteration = None     # number of 1. iteration of a run
        self.last_iteration = None      # number of last iteration of a run
        
        self.activityType_0 = None      # activity type home
        self.activityType_1 = None      # activity type work
        
        self.samplingRate = None        # sampling rate
        self.year = None                # year of current run
        self.temp_directory = None      # temp directory, cache for urbansim-matsim communication (relative to OPUS_HOME)
        self.opus_home = None           # path to opus home

    def run(self, config, year):
        """Running MATSim.  A lot of paths are relative; the base path is ${OPUS_HOME}/opus_matsim.  As long as ${OPUS_HOME}
        is correctly set and the matsim tarfile was unpacked in OPUS_HOME, this should work out of the box.  There may eventually
        be problems with the java version.
        """
        try:
            import pydevd
            pydevd.settrace()
        except: pass
        
        logger.start_block("Starting RunTravelModel.run(...)")
        
        self.setUp( config )
        
        # get travel model parameter from the opus dictionary
        travel_model_configuration = config['travel_model_configuration']      # contains matsim4urbansim and matsim_config parameter
        # matsim4urbansim
        matsim4urbansim_config = travel_model_configuration['matsim4urbansim'] # contains parameter for matsim/urbansim integration
        # matsim_config
        matsim_config = travel_model_configuration['matsim_config']            # contains various matsim_config parameter 
        matsim_common = matsim_config['common']

        # network parameter
        if matsim_common['matsim_network_file'] == None:
            raise StandardError('Network location for MATSim not set in "travel_model_configuration" of your current configuration file')
        self.network_file = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", matsim_common['matsim_network_file'])
        # controler parameter
        self.first_iteration = matsim_common['first_iteration']
        self.last_iteration = matsim_common['last_iteration']
        # planCalcScoreType
        self.activityType_0 = matsim_common['activityType_0']
        self.activityType_1 = matsim_common['activityType_1']
        # urbansim parameter
        self.year = year
        self.samplingRate = matsim4urbansim_config['sampling_rate']
        self.temp_directory = matsim4urbansim_config['temp_directory']
        self.isTestRun = False
        self.opus_home = os.environ['OPUS_HOME']
        
        self.firstRun = "FALSE"
        try: # determine for MATSim if this is the fist run
            if self.travel_model_configuration['start_year'] == year:
                self.firstRun = "TRUE"
        except: pass
            
        # create/maschal matsim config file
        logger.log_status("Creating Matsim config file in " + self.matsim_config_full)
        self.marschalling_matsim_config_pyxB()
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': os.environ['OPUS_HOME'],
                'vmargs': "-Xmx2000m",
                'classpath': "libs/log4j/log4j/1.2.15/log4j-1.2.15.jar:libs/jfree/jfreechart/1.0.7/jfreechart-1.0.7.jar:libs/jfree/jcommon/1.0.9/jcommon-1.0.9.jar:classesMATSim:classesToronto:classesTNicolai:classesKai:classesEntry", #  'classpath': "classes:jar/MATSim.jar",
                'javaclass': "playground.run.Matsim4Urbansim",
                'matsim_config_file': self.matsim_config_full } 
        
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
        """ set matism config path
        """
        self.matsim_config_destination = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "matsim_config")
        if not os.path.exists(self.matsim_config_destination):
            try: os.mkdir(self.matsim_config_destination)
            except: pass
        self.matsim_config_name = config['project_name'] + "_matsim_config.xml"
        self.matsim_config_full = os.path.join( self.matsim_config_destination, self.matsim_config_name  )
        
    def marschalling_matsim_config_pyxB(self):
        """ create a matsim config with the parameter from the travel model configuration with PyxB
        """
        # xml root element
        root = pyxb_matsim_config_parser.matsim_configType.Factory()

        # main elements
        config_elem = pyxb_matsim_config_parser.configType.Factory()
        matsim4urbansim_elem = pyxb_matsim_config_parser.matsim4urbansimType.Factory()
        
        # different element sections for network, controler, planCalcScore, ect.
        network_elem = pyxb_matsim_config_parser.networkType.Factory()
        controler_elem = pyxb_matsim_config_parser.controlerType.Factory()
        plan_calc_score_elem = pyxb_matsim_config_parser.planCalcScoreType.Factory()
        urbansim_elem = pyxb_matsim_config_parser.urbansimParameterType.Factory()
        
        # single elemts containing values
        network_elem.inputFile = self.network_file
        
        controler_elem.firstIteration = self.first_iteration
        controler_elem.lastIteration = self.last_iteration
        
        plan_calc_score_elem.activityType_0 = self.activityType_0
        plan_calc_score_elem.activityType_1 = self.activityType_1
        
        urbansim_elem.samplingRate = self.samplingRate
        urbansim_elem.year = self.year
        urbansim_elem.tempDirectory = self.temp_directory
        urbansim_elem.isTestRun = self.isTestRun
        urbansim_elem.opusHOME = self.opus_home
        
        # assemble single elements with dedicated section elements
        config_elem.network = network_elem
        config_elem.controler = controler_elem
        config_elem.planCalcScore = plan_calc_score_elem
        
        matsim4urbansim_elem.urbansimParameter = urbansim_elem
        
        # assemble with root element
        root.config = config_elem
        root.matsim4urbansim = matsim4urbansim_elem
        
        # content = root.content() # get children
        
        # convert to dom object
        dom = root.toDOM(element_name='matsim_config') # TODO: hier war ein Fehler letztes mal
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        logger.log_status( prettydom )
        
        xml = root.toxml()
        logger.log_status(' Generated following MATSim configuration:\n%s' %xml )
        logger.log_status( "Writing (marschalling) this matsim config xml to {0}".format( self.matsim_config_full ) )
        
        file_object = open(self.matsim_config_full, 'w')
        #dom.writexml(file_object, encoding="UTF-8") # no pretty format :-(
        file_object.write(prettydom) # maybe the better way to save matsim config xml ?
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status( "Finished Marschalling" )
        
    def validate_xml(self, xml, xsd):
        
        logger.log_status("Loading XML file: {0}".format(xml))
        logger.log_status("Loading XSD file: {0}".format(xsd))
        
        schema = open(xsd)
        library = open(xml)
            
        xmlschema_doc = etree.parse(schema)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        library_doc = etree.parse(library)
        
        logger.log_status("Validationg XML")
        if xmlschema.validate(library_doc):
            logger.log_status("Valid XML")
            return True
        else:
            logger.log_error("Invalid XML")
            return False

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

    #try: #tnicolai
    #    import pydevd
    #    pydevd.settrace()
    #except: pass

    logger.enable_memory_logging()
    RunTravelModel().run(resources, options.year)    
