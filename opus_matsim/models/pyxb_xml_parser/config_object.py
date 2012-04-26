# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from lxml import etree
from opus_matsim.models.pyxb_xml_parser import pyxb_matsim_config_parser
from opus_matsim.models.org.constants import matsim4opus, matsim_config,\
    matsim_output, matsim_temp, activity_type_0, activity_type_1, first_iteration,\
    backup_run_data, test_parameter
from opus_core import paths

class MATSimConfigObject(object):
    
    def __init__(self, config, year):
        """ Constructor
        """

        self.config_dictionary = config
        self.sub_config_exists = False
        self.config_destination_location = None
        
        # get sub dictionaries from travel model configuration
        travel_model_configuration, matsim4urbansim_part, common_matsim_part = self.__get_travel_model_sub_dictionaries()
        
        # network parameter
        try:    # checks if sub config for matsim network exists
            self.sub_config_exists = (common_matsim_part['matsim_network_file'] != None)
        except: pass
        if self.sub_config_exists:
            self.check_abolute_path( common_matsim_part['matsim_network_file'] )
            self.network_file = paths.get_opus_home_path( common_matsim_part['matsim_network_file'] )
        else:
            raise StandardError('No network given in the  "travel_model_configuration" of your current configuration file. A network is required in order to run MATSim. ')
        self.sub_config_exists = False
        
        # input plans file parameter
        self.input_plans_file = self.__get_plans_file(common_matsim_part, 'input_plans_file')
        self.hotstart_plans_file = self.__get_plans_file(common_matsim_part, 'hotstart_plans_file')
        
        # controler parameter
        self.first_iteration = first_iteration
        self.last_iteration = common_matsim_part['last_iteration']
        
        # planCalcScoreType
        self.activityType_0 = activity_type_0
        self.activityType_1 = activity_type_1
        
        # urbansim parameter
        self.year = year
        self.population_sampling_rate = matsim4urbansim_part['sampling_rate']

        self.opus_home = paths.get_opus_home_path()
        self.opus_data_path = paths.get_opus_data_path_path()
        
        self.matsim4opus_path = paths.get_opus_home_path( matsim4opus )
        self.ceckAndCreateFolder(self.matsim4opus_path)
        self.matsim_config_path = os.path.join( self.matsim4opus_path, matsim_config )
        self.ceckAndCreateFolder(self.matsim_config_path)
        self.matsim_output_path = os.path.join( self.matsim4opus_path, matsim_output )
        self.ceckAndCreateFolder(self.matsim_output_path)
        self.matsim_temp_path = os.path.join( self.matsim4opus_path, matsim_temp )
        self.ceckAndCreateFolder(self.matsim_temp_path)
        
        self.isTestRun = False
        self.test_parameter = ""
        try:
            self.test_parameter = common_matsim_part[ test_parameter ]
        except: pass
        self.backup_run_data = False
        try:
            self.backup_run_data = common_matsim_part[ backup_run_data ]
        except: pass
        
        self.firstRun = "FALSE"
        try: # determine for MATSim if this is the fist run
            if travel_model_configuration['start_year'] == year:
                self.firstRun = "TRUE"
        except: pass
        
        self.config_destination_location = self.__set_config_destination( self.config_dictionary )
        
    def __get_plans_file(self, common_matsim_part, entry):
        try:    # checks if sub config for matsim input plans file exists
            self.sub_config_exists = ( common_matsim_part[entry] != None)
        except: return ""
        if self.sub_config_exists:
            self.check_abolute_path( common_matsim_part[entry]  )    
            logger.log_note('Input plans file found (MATSim warm start enabled).') 
            return paths.get_opus_home_path( common_matsim_part[entry]  )
        else: 
            logger.log_note('No input plans file set in the "travel_model_configuration" of your current configuration file (MATSim warm start disabled).')
            return ""
        
    def __set_config_destination(self, config):
        """ set destination for MATSim config
        """
        self.matsim_config_name = config['project_name'] + "_matsim_config.xml"
        return os.path.join( self.matsim_config_path, self.matsim_config_name  )
        
    def check_abolute_path(self, path):
        """ raises an exception if an absolute path is given
        """
        if(path.startswith('/')):
            raise StandardError('Absolute path names are not supported by now! Check: %s' %path)
    
    def ceckAndCreateFolder(self, path):
        if not os.path.exists(path):
            try: os.mkdir(path)
            except: pass
    
    def marschall(self):
        """ create a matsim config with the parameter from the travel model configuration with PyxB
        """

        # create/maschal matsim config file
        logger.log_status("Creating Matsim config file in " + self.config_destination_location)
        
        # xml root element
        root = pyxb_matsim_config_parser.matsim_configType.Factory()

        # main elements
        config_elem = pyxb_matsim_config_parser.configType.Factory()
        matsim4urbansim_elem = pyxb_matsim_config_parser.matsim4urbansimType.Factory()
        
        # different element sections for network, controler, planCalcScore, ect.
        network_elem = pyxb_matsim_config_parser.networkType.Factory()
        input_plans_file_elem = pyxb_matsim_config_parser.inputPlansFileType.Factory()
        hotstart_plans_file_elem = pyxb_matsim_config_parser.inputPlansFileType.Factory()
        controler_elem = pyxb_matsim_config_parser.controlerType.Factory()
        plan_calc_score_elem = pyxb_matsim_config_parser.planCalcScoreType.Factory()
        urbansim_elem = pyxb_matsim_config_parser.urbansimParameterType.Factory()
        
        # single elemts containing values
        network_elem.inputFile = self.network_file
        
        input_plans_file_elem = self.input_plans_file
        hotstart_plans_file_elem = self.hotstart_plans_file
        
        controler_elem.firstIteration = self.first_iteration
        controler_elem.lastIteration = self.last_iteration
        
        plan_calc_score_elem.activityType_0 = self.activityType_0
        plan_calc_score_elem.activityType_1 = self.activityType_1
        
        urbansim_elem.population_sampling_rate = self.population_sampling_rate
        urbansim_elem.year = self.year
        urbansim_elem.opusHome = self.opus_home
        urbansim_elem.opusDataPath = self.opus_data_path
        urbansim_elem.matsim4opus = self.matsim4opus_path
        urbansim_elem.matsim4opusConfig = self.matsim_config_path
        urbansim_elem.matsim4opusOutput = self.matsim_output_path
        urbansim_elem.matsim4opusTemp = self.matsim_temp_path
        urbansim_elem.isTestRun = self.isTestRun
        urbansim_elem.testParameter = self.test_parameter
        urbansim_elem.backupRunData = self.backup_run_data
        
        # assemble single elements with dedicated section elements
        config_elem.network = network_elem
        config_elem.inputPlansFile = input_plans_file_elem
        config_elem.hotStartPlansFile = hotstart_plans_file_elem
        config_elem.controler = controler_elem
        config_elem.planCalcScore = plan_calc_score_elem
        
        matsim4urbansim_elem.urbansimParameter = urbansim_elem
        
        # assemble with root element
        root.config = config_elem
        root.matsim4urbansim = matsim4urbansim_elem
        
        # content = root.content() # get children
        
        # convert to dom object
        dom = root.toDOM(element_name='matsim_config')
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        
        logger.log_status( 'Generated MATSim configuration file:' )
        logger.log_status( prettydom )
        logger.log_status( 'Writing (marschalling) this matsim config xml to {0}'.format( self.config_destination_location ) )
        
        file_object = open(self.config_destination_location, 'w')
        #dom.writexml(file_object, encoding="UTF-8") # no pretty format :-(
        file_object.write(prettydom) # maybe the better way to save matsim config xml ?
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status( "Finished Marschalling" )
        
        return self.config_destination_location
        
        
    def __get_travel_model_sub_dictionaries(self):
        """ returns the configuration from the travel model configuration
            for the MATSim4UrbanSim and common MATSim part
        """
        # get travel model parameter from the opus dictionary
        travel_model_configuration = self.config_dictionary['travel_model_configuration'] # contains matsim4urbansim and matsim_config parameter
        
        # matsim4urbansim
        matsim4urbansim_config = travel_model_configuration['matsim4urbansim'] # contains parameter for matsim/urbansim integration
        # matsim_config
        matsim_config = travel_model_configuration['matsim_config']            # contains various matsim_config parameter 
        matsim_common = matsim_config['common']
        
        return travel_model_configuration, matsim4urbansim_config, matsim_common
    
    
    def validate_xml(self, xml, xsd):
        """ validate a xml against a xsd
        """
        
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