# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from lxml import etree
from opus_matsim.sustain_city.models.pyxb_xml_parser import pyxb_matsim_config_parser
from opus_matsim.models.org.constants import matsim4opus, matsim_config,\
    matsim_output, matsim_temp, activity_type_0, activity_type_1, first_iteration,\
    backup_run_data, test_parameter, warmstart_flag, hotstart_flag
from opus_core import paths

class MATSimConfigObject(object):
    
    def __init__(self, config, year):
        """ Constructor
        """

        self.config_dictionary = config
        self.sub_config_exists = False
        self.config_destination_location = None
        
        # get sub dictionaries from travel model configuration
        matsim4urbansim, matsim_controler, matsim_controler_parameter, matsim_common, matsim_plan_calc_score, matsim_strategy = self.__get_travel_model_sub_dictionaries()
        
        # network parameter
        self.network_file = self.__get_file_location( matsim_common['matsim_network_file'], required=True)
        
        # input plans file parameter
        self.input_plans_file = self.__get_plans_file(matsim_common, warmstart_flag)
        self.hotstart_plans_file = self.__get_plans_file(matsim_common, hotstart_flag)
        
        # controler parameter
        self.first_iteration = first_iteration
        self.last_iteration = matsim_common['last_iteration']
        self.matsim_configuration = self.__get_file_location( matsim_common['matsim_config'] )
        
        # planCalcScoreType
        self.activityType_0                 = activity_type_0
        self.activityType_1                 = activity_type_1
        self.home_activity_typical_duration = matsim_plan_calc_score['home_activity_typical_duration']
        self.work_activity_typical_duration = matsim_plan_calc_score['work_activity_typical_duration']
        self.work_activity_opening_time     = matsim_plan_calc_score['work_activity_opening_time']
        self.work_activity_latest_start_time= matsim_plan_calc_score['work_activity_latest_start_time']
        self.brain_exp_beta                 = matsim_plan_calc_score['brain_exp_beta']
        
        # strategyType
        self.max_agent_plan_memory_size     = matsim_strategy['max_agent_plan_memory_size']
        self.time_accocation_mutator_probability = matsim_strategy['time_accocation_mutator_probability']
        self.change_exp_beta_probability    = matsim_strategy['change_exp_beta_probability']
        self.reroute_dijkstra_probability   = matsim_strategy['reroute_dijkstra_probability']
        
        # urbansim parameter
        self.year = year
        self.samplingRate = matsim4urbansim['sampling_rate']

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
            self.test_parameter = matsim_common[ test_parameter ]
        except: pass
        self.backup_run_data = False
        try:
            self.backup_run_data = self.__get_value_as_boolean( backup_run_data, matsim_common) #matsim_common[ backup_run_data ]
        except: pass

        # matsim4urbansim controler
        self.zone2zone_impedance      = self.__get_value_as_boolean( 'zone2zone_impedance', matsim_controler )
        self.agent_performance        = self.__get_value_as_boolean( 'agent_performance', matsim_controler )
        self.zone_based_accessibility = self.__get_value_as_boolean( 'zone_based_accessibility', matsim_controler )
        self.cell_based_accessibility = self.__get_value_as_boolean( 'cell_based_accessibility', matsim_controler )
        self.cell_size                = matsim_controler_parameter['cell_size']
        self.bounding_box_top         = matsim_controler_parameter['bounding_box_top']
        self.bounding_box_left        = matsim_controler_parameter['bounding_box_left']
        self.bounding_box_right       = matsim_controler_parameter['bounding_box_right']
        self.bounding_box_bottom      = matsim_controler_parameter['bounding_box_bottom']
        self.shape_file               = self.__get_file_location( matsim_controler_parameter['shape_file'] )
        
        self.config_destination_location = self.__set_config_destination( self.config_dictionary )
    
    def __get_file_location(self, file_path, required=False ):
        ''' checks if a given sub path exists
        '''
        try:
            self.sub_config_exists = (file_path != None)
        except:
            if required:
                raise StandardError('File not found: %s' %file_path)
                self.sub_config_exists = False
        if self.sub_config_exists:
            self.check_abolute_path( file_path )
            return paths.get_opus_home_path( file_path )
        else:
            return ""
        
        
    def __get_plans_file(self, common_matsim_part, entry):
        try:
            self.sub_config_exists = ( common_matsim_part[entry] != None)
        except:
            logger.log_note('No input plans file in "travel_model_configuration" section found (i.e. MATSim warm/hot start is not active).') 
            return ""
        if self.sub_config_exists:
            self.check_abolute_path( common_matsim_part[entry]  )    
            logger.log_note('Input plans file found (MATSim warm start enabled).') 
            return paths.get_opus_home_path( common_matsim_part[entry]  )
        
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
            
    def __get_value_as_boolean(self, option, sub_config):
        
        if sub_config != None and option != None:
            for param in sub_config:
                if str(param).lower() == str(option).lower():
                    return True
            return False
    
    def marschall(self):
        """ create a matsim config with the parameter from the travel model configuration with PyxB
        """

        # create/maschal matsim config file
        logger.log_status("Creating MATSim config file in " + self.config_destination_location)
        
        # xml root element
        root = pyxb_matsim_config_parser.matsim_configType.Factory()

        # main elements
        config_elem = pyxb_matsim_config_parser.configType.Factory()
        matsim4urbansim_elem = pyxb_matsim_config_parser.matsim4urbansimType.Factory()
        
        # different element sections for network, controler, planCalcScore, ect.
        matsim_config_elem = pyxb_matsim_config_parser.fileType.Factory()
        network_elem = pyxb_matsim_config_parser.fileType.Factory()
        shapefile_elem = pyxb_matsim_config_parser.fileType.Factory()
        input_plans_file_elem = pyxb_matsim_config_parser.inputPlansFileType.Factory()
        hotstart_plans_file_elem = pyxb_matsim_config_parser.inputPlansFileType.Factory()
        controler_elem = pyxb_matsim_config_parser.controlerType.Factory()
        plan_calc_score_elem = pyxb_matsim_config_parser.planCalcScoreType.Factory()
        strategy_elem = pyxb_matsim_config_parser.strategyType.Factory()
        urbansim_elem = pyxb_matsim_config_parser.urbansimParameterType.Factory()
        matsim4urbansim_controler_elem = pyxb_matsim_config_parser.matsim4urbansimContolerType.Factory()
        
        # single elements containing values
        matsim_config_elem.inputFile                        = self.matsim_configuration
        network_elem.inputFile                              = self.network_file
        shapefile_elem.inputFile                            = self.shape_file
        
        input_plans_file_elem                               = self.input_plans_file
        hotstart_plans_file_elem                            = self.hotstart_plans_file
        
        controler_elem.firstIteration                       = self.first_iteration
        controler_elem.lastIteration                        = self.last_iteration
        
        plan_calc_score_elem.activityType_0                 = self.activityType_0
        plan_calc_score_elem.activityType_1                 = self.activityType_1
        plan_calc_score_elem.homeActivityTypicalDuration    = self.home_activity_typical_duration
        plan_calc_score_elem.workActivityTypicalDuration    = self.work_activity_typical_duration
        plan_calc_score_elem.workActivityOpeningTime        = self.work_activity_opening_time
        plan_calc_score_elem.workActivityLatestStartTime    = self.work_activity_latest_start_time
        
        strategy_elem.maxAgentPlanMemorySize                = self.max_agent_plan_memory_size
        strategy_elem.timeAllocationMutatorProbability      = self.time_accocation_mutator_probability
        strategy_elem.changeExpBetaProbability              = self.change_exp_beta_probability
        strategy_elem.reRouteDijkstraProbability            = self.reroute_dijkstra_probability
        
        urbansim_elem.samplingRate                          = self.samplingRate
        urbansim_elem.year                                  = self.year
        urbansim_elem.opusHome                              = self.opus_home
        urbansim_elem.opusDataPath                          = self.opus_data_path
        urbansim_elem.matsim4opus                           = self.matsim4opus_path
        urbansim_elem.matsim4opusConfig                     = self.matsim_config_path
        urbansim_elem.matsim4opusOutput                     = self.matsim_output_path
        urbansim_elem.matsim4opusTemp                       = self.matsim_temp_path
        urbansim_elem.isTestRun                             = self.isTestRun
        urbansim_elem.testParameter                         = self.test_parameter
        urbansim_elem.backupRunData                         = self.backup_run_data
        
        matsim4urbansim_controler_elem.zone2zoneImpedance   = self.zone2zone_impedance
        matsim4urbansim_controler_elem.zoneBasedAccessibility= self.zone_based_accessibility
        matsim4urbansim_controler_elem.cellBasedAccessibility= self.cell_based_accessibility
        matsim4urbansim_controler_elem.cellSizeCellBasedAccessibility= self.cell_size
        matsim4urbansim_controler_elem.shapeFileCellBasedAccessibility= shapefile_elem
        matsim4urbansim_controler_elem.boundingBoxTop       = self.bounding_box_top
        matsim4urbansim_controler_elem.boundingBoxLeft      = self.bounding_box_left
        matsim4urbansim_controler_elem.boundingBoxRight     = self.bounding_box_right
        matsim4urbansim_controler_elem.boundingBoxBottom    = self.bounding_box_bottom
        matsim4urbansim_controler_elem.agentPerformance     = self.agent_performance
        matsim4urbansim_controler_elem.betaBrain            = self.brain_exp_beta     
        
        # assemble single elements with dedicated section elements
        config_elem.matsim_config                           = matsim_config_elem
        config_elem.network                                 = network_elem
        config_elem.inputPlansFile                          = input_plans_file_elem
        config_elem.hotStartPlansFile                       = hotstart_plans_file_elem
        config_elem.controler                               = controler_elem
        config_elem.planCalcScore                           = plan_calc_score_elem
        config_elem.strategy                                = strategy_elem
        
        matsim4urbansim_elem.urbansimParameter              = urbansim_elem
        matsim4urbansim_elem.matsim4urbansimContoler        = matsim4urbansim_controler_elem
        
        # assemble with root element
        root.config                                         = config_elem
        root.matsim4urbansim                                = matsim4urbansim_elem
        
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
        matsim4urbansim = travel_model_configuration['matsim4urbansim']            # contains parameter for matsim/urbansim integration
        matsim_controler = matsim4urbansim['matsim_controler']
        matsim_controler_parameter = matsim4urbansim['controler_parameter']
        # matsim_config
        matsim_config = travel_model_configuration['matsim_config']                       # contains various matsim_config parameter 
        matsim_common = matsim_config['common']
        matsim_plan_calc_score = matsim_config['plan_calc_score']
        matsim_strategy = matsim_config['strategy']
        
        return matsim4urbansim, matsim_controler, matsim_controler_parameter, matsim_common, matsim_plan_calc_score, matsim_strategy
    
    
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