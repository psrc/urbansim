# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.abstract_travel_model import AbstractTravelModel
import os
import pyxb.utils.domutils as domutils
from opus_matsim.sustain_city.models.pyxb_xml_parser import pyxb_matsim_config_parser
from lxml import etree
from opus_core import paths

class RunTravelModel(AbstractTravelModel):
    """Run the travel model.
    """
    def __init__(self):
        """Constructor
        """
        self.travel_model_configuration = None # opus config dictionary for travel model
        
        # parameter for matsim execution
        self.firstRun = "FALSE"     # flag is true on the first run
        self.matsim_config_destination = None  # path to generated matsim config xml
        self.matsim_config_name = None  # matsim config xml name
        self.matsim_config_full = None  # concatination of matsim config path and name
        self.isTestRun          = None  # indicates wheter running the travel model is a test run
                                        # this flag is needed for test cases
        
        # parameter for matsim configuration
        self.network_file = None    # (relative) path to network xml file
        
        self.first_iteration = None # number of 1. iteration of a run
        self.last_iteration = None  # number of last iteration of a run
        
        self.activityType_0 = None # activity type home
        self.activityType_1 = None # activity type work
        
        self.samplingRate = None    # sampling rate
        self.year = None            # year of current run
        self.temp_directory = None  # temp directory, cache for urbansim-matsim communication (relative to OPUS_HOME)
        self.opus_home = None       # path to opus home

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
        
        # get travel model parameter from the opus dictionary
        self.travel_model_configuration = config['travel_model_configuration']
        
        # over-written if there is a specific config file name for the year:
        #if travel_model_configuration[year]['matsim_config_filename']:
        #    matsim_config_filename = travel_model_configuration[year]['matsim_config_filename']

        # network parameter
        self.network_file = self.travel_model_configuration['matsim_network_file']
        # controler parameter TODO:
        self.first_iteration = self.travel_model_configuration['first_iteration']
        self.last_iteration = self.travel_model_configuration['last_iteration']
        # planCalcScoreType
        self.activityType_0 = self.travel_model_configuration['activityType_0']
        self.activityType_1 = self.travel_model_configuration['activityType_1']
        # urbansim parameter
        self.year = year
        self.samplingRate = self.travel_model_configuration['sampling_rate']
        self.temp_directory = self.travel_model_configuration['temp_directory']
        self.isTestRun = False
        self.opus_home = paths.OPUS_HOME
        
        self.firstRun = "FALSE"
        try: # determine for MATSim if this is the fist run
            if self.travel_model_configuration['start_year'] == year:
                self.firstRun = "TRUE"
        except: pass
        
        # determine matsim config path
        if self.network_file != None and self.network_file != '':
            self.network_file = paths.get_opus_home_path("opus_matsim", self.network_file)
        else:
            logger.log_error("ERROR while creating output directory for the MATSim config file...")
            
        self.matsim_config_destination = paths.get_opus_home_path("opus_matsim", "matsim_config")
        if not os.path.exists(self.matsim_config_destination):
            try: os.mkdir(self.matsim_config_destination)
            except: pass
        self.matsim_config_name = config['project_name'] + "_matsim_config.xml"
        self.matsim_config_full = os.path.join( self.matsim_config_destination, self.matsim_config_name  )

        # create/maschal matsim config file
        logger.log_status("Creating Matsim config file in " + self.matsim_config_full)
        #self.unmarschal_matsim_config_2_pyxB()
        self.marschalling_matsim_config_pyxB()
        #self.marschalling_matsim_config_3_pyxB()
        #self.marschalling_matsim_config_2_generateDS()
        
        cmd = """cd %(opus_home)s/opus_matsim ; java %(vmargs)s -cp %(classpath)s %(javaclass)s %(matsim_config_file)s""" % {
                'opus_home': paths.OPUS_HOME,
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
        
    def marschalling_matsim_config_2_generateDS(self):
        """ create a matsim config with the parameter from the travel model configuration with generateDS
        """
        sshema_file  = os.path.join("/Users/thomas/Development/workspace/urbansim/opus_matsim/models", "MATSim4UrbanSimTestConfig2.xsd")
        
        root = matsim_xml_config_binding_2_gds.configType.factory()
        
        network_elem = matsim_xml_config_binding_2_gds.networkType.factory()
        controler_elem = matsim_xml_config_binding_2_gds.controlerType.factory()
        urbansim_elem = matsim_xml_config_binding_2_gds.urbansimParameterType.factory()
        
        # create content
        network_elem.inputFile = self.network_file
        
        controler_elem.firstIteration = self.first_iteration
        controler_elem.lastIteration = self.last_iteration
        
        urbansim_elem.samplingRate = self.samplingRate
        urbansim_elem.year = self.year
        urbansim_elem.tempDirectory = self.temp_directory
        
        root.network = network_elem
        root.controler = controler_elem
        root.urbansimParameter = urbansim_elem
        
        file_object = open(self.matsim_config_full, 'w')
        file_object.write('<?xml version="1.0" ?>\n')
        root.export(file_object, 0, '', 'config', '')
        file_object.flush()
        if not file_object.closed:
            file_object.close()
        
        self.validate_xml(self.matsim_config_full, sshema_file)
        
    def unmarschal_matsim_config_2_pyxB(self):
        
        xml_file = os.path.join("/Users/thomas/Development/opus_home/opus_matsim/matsim_config", "seattle_parcel_matsim_config_template.xml")
        
        logger.log_status("Starting Unmarschalling {0}".format(xml_file))
        
        file_object = open(xml_file, 'r')
        xml_as_string = file_object.read()
        doc = domutils.StringToDOM( xml_as_string )
        
        self.root = matsim_xml_config_binding_2.CreateFromDOM(doc.documentElement)
        
        # get single elements of this dom object
        self.network_elem = self.root.network
        self.controler_elem = self.root.controler
        self.urbansimParameter = self.root.urbansimParameter
        
        if self.network_elem != None:
            logger.log_status("Network Inputfile = {0}".format(self.network_elem.inputFile))
        if self.controler_elem != None:
            first_i = self.controler_elem.firstIteration
            last_i = self.controler_elem.lastIteration
            
            logger.log_status("Controler First Iteration = {0} and Last Iteration = {1}".format(first_i, last_i))
            
        if self.urbansimParameter != None:
            sampling = self.urbansimParameter.samplingRate
            year = self.urbansimParameter.year
            temp_dir = self.urbansimParameter.tempDirectory
            
            logger.log_status("UrbansimParameter SamplingRate = {0} Year = {1} TempDirectory = {2}".format(sampling, year, temp_dir))
            
        logger.log_status("Finisched Unmarschalling")
        
    def marschalling_matsim_config_pyxB(self):
        """ create a matsim config with the parameter from the travel model configuration with PyxB
        """
        
        root = pyxb_matsim_config_parser.configType.Factory()
        
        print dir(root)
        
        network_elem = pyxb_matsim_config_parser.networkType.Factory()
        controler_elem = pyxb_matsim_config_parser.controlerType.Factory()
        plan_calc_score_elem = pyxb_matsim_config_parser.planCalcScoreType.Factory()
        urbansim_elem = pyxb_matsim_config_parser.urbansimParameterType.Factory()
        
        # create content
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
        
        root.network = network_elem
        root.controler = controler_elem
        root.planCalcScore = plan_calc_score_elem
        root.urbansimParameter = urbansim_elem
        
        # content = root.content() # get children like network, controler and urbansimParameter ..
        
        # convert to dom object
        dom = root.toDOM(element_name='config')
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        logger.log_status( prettydom )
        
        xml = root.toxml()
        print xml
        
        logger.log_status( "Writing (marschalling) this matsim config xml to {0}".format( self.matsim_config_full ) )
        
        file_object = open(self.matsim_config_full, 'w')
        #dom.writexml(file_object, encoding="UTF-8") # no pretty format :-(
        file_object.write(prettydom) # maybe the better way to save matsim config xml ?
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status( "Finished Marschalling" )
        
    def marschalling_matsim_config_3_pyxB(self):
        """ create a matsim config with the parameter from the travel model configuration with PyxB
        """
        
        root = matsim_xml_config_binding_3.CTD_ANON_1.Factory()
        
        network_elem = matsim_xml_config_binding_3.networkType.Factory()
        controler_elem = matsim_xml_config_binding_3.controlerType.Factory()
        urbansim_elem = matsim_xml_config_binding_3.urbansimParameterType.Factory()
        
        # create content
        network_elem.inputFile = self.network_file
        
        controler_elem.firstIteration = self.first_iteration
        controler_elem.lastIteration = self.last_iteration
        
        urbansim_elem.samplingRate = self.samplingRate
        urbansim_elem.year = self.year
        urbansim_elem.tempDirectory = self.temp_directory
        
        root.network = network_elem
        root.controler = controler_elem
        root.urbansimParameter = urbansim_elem
        
        # convert to dom object
        dom = root.toDOM()
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        logger.log_status( prettydom )
        
        logger.log_status( "Writing (marschalling) this matsim config xml to {0}".format( self.matsim_config_full ) )
        
        file_object = open(self.matsim_config_full, 'w')
        #dom.writexml(file_object, encoding="UTF-8") # no pretty format :-(
        file_object.write(prettydom) # maybe the better way to save matsim config xml ?
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status( "Finisched Marschalling" )
        
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

    try: #tnicolai
        import pydevd
        pydevd.settrace()
    except: pass

    logger.enable_memory_logging()
    RunTravelModel().run(resources, options.year)    
