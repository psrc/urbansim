# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from lxml import etree
from opus_matsim.sustain_city.models.pyxb_xml_parser import pyxb_matsim_config_parser
from opus_core import paths

class MATSimConfigObjectV3(object):
    
    def __init__(self, config, year):
        """ Constructor
        """
        try: # tnicolai :for debugging
            import pydevd
            pydevd.settrace()
        except: pass

        self.config_dictionary = config
        self.sub_config_exists = False
        self.config_destination_location = None
        
        # get directories
        self.opus_home = paths.get_opus_home_path()
        self.opus_data_path = paths.get_opus_data_path_path()
        self.matsim4opus_path = paths.get_opus_home_path( 'matsim4opus' )
        self.checkAndCreateFolder(self.matsim4opus_path)
        cache_directory = config['cache_directory']
        matsim4opus_target_path = os.path.join(cache_directory, 'matsim4opus') 
        
        
        # get sub dictionaries from travel model configuration
        matsim4urbansim, matsim_config, accessibility, common, plan_calc_score = self.__get_travel_model_sub_dictionaries()
        
        ###########################
        # matsim4urbansim parameter
        ###########################
        self.matsim4urbansim.population_sampling_rate =  matsim4urbansim['population_sampling_rate']
        self.matsim4urbansim.custom_parameter =  matsim4urbansim['custom_parameter']
        self.matsim4urbansim.backup = self.__get_value_as_boolean('backup_run_data',  matsim4urbansim['backup'])
        self.matsim4urbansim.matsim_data_to_compute.zone2zone_impedance = self.__get_value_as_boolean('zone2zone_impedance',  matsim4urbansim['matsim_data_to_compute'])
        self.matsim4urbansim.matsim_data_to_compute.agent_performance = self.__get_value_as_boolean('agent_performance',  matsim4urbansim['matsim_data_to_compute'])
        self.matsim4urbansim.matsim_data_to_compute.zone_based_accessibility = self.__get_value_as_boolean('zone_based_accessibility',  matsim4urbansim['matsim_data_to_compute'])
        self.matsim4urbansim.matsim_data_to_compute.parcel_based_accessibility = self.__get_value_as_boolean('parcel_based_accessibility',  matsim4urbansim['matsim_data_to_compute'])
        self.matsim4urbansim.year = year
        self.matsim4urbansim.matsim_config_path = os.path.join( matsim4opus_target_path, 'matsim_config' )
        self.checkAndCreateFolder(self.matsim_config_path)
        self.matsim4urbansim.matsim_output_path = os.path.join( matsim4opus_target_path, 'output' )
        self.checkAndCreateFolder(self.matsim_output_path)
        self.matsim4urbansim.matsim_temp_path = os.path.join( matsim4opus_target_path, 'tmp' )
        self.checkAndCreateFolder(self.matsim_temp_path)
        
        
        ###########################
        # matsim_config parameter
        ###########################
        self.matsim_config.random_location_distribution_radius_for_urbansim_zone = matsim_config['random_location_distribution_radius_for_urbansim_zone']
        self.matsim_config.random_location_distribution_shape_file_for_urbansim_zone =  matsim_config['random_location_distribution_shape_file_for_urbansim_zone']
        
        # matsim_config/accessibility parameter
        self.matsim_config.accessibility.cell_size = accessibility['cell_size']
        self.matsim_config.accessibility.study_area_boundary_shape_file = accessibility['study_area_boundary_shape_file']
        self.matsim_config.accessibility.bounding_box_left = accessibility['bounding_box_left']
        self.matsim_config.accessibility.bounding_box_bottom = accessibility['bounding_box_bottom']
        self.matsim_config.accessibility.bounding_box_top = accessibility['bounding_box_top']
        self.matsim_config.accessibility.bounding_box_right = accessibility['bounding_box_right']
        accessibility_computation_area = accessibility['accessibility_computation_area'] # loading sub directory ...
        if not(accessibility_computation_area.__len__ != 1):
            logger.log_error("Please select ONE item in 'travel_model_configuration/matsim_config/accessibility/accessibility_computation_area' to determine how the study area for the accessibility computation!")
            exit()
        self.matsim_config.accessibility.accessibility_computation_area.from_shapefile = self.__get_value_as_boolean( 'from_shapefile', accessibility_computation_area )
        self.matsim_config.accessibility.accessibility_computation_area.from_bounding_box = self.__get_value_as_boolean( 'from_bounding_box', accessibility_computation_area )
        self.matsim_config.accessibility.accessibility_computation_area.from_network = self.__get_value_as_boolean( 'from_network', accessibility_computation_area )
        
        # matsim_config/common parameter
        self.matsim_config.common.network_file = self.__get_file_location( common['matsim_network_file'], required=True)
        self.matsim_config.common.first_iteration = 0
        self.matsim_config.common.last_iteration = common['last_iteration']
        self.matsim_config.common.matsim_configuration = self.__get_external_matsim_config_for_current_year(common['external_matsim_config'], year)
        self.matsim_config.common.warm_start_plans_file = self.__get_plans_file(common, 'warm_start_plans_file')
        self.matsim_config.common.use_hot_start = self.__get_value_as_boolean( 'use_hot_start', common['use_hot_start'] )
        self.matsim_config.common.hot_start_plans_file = ''
        if self.matsim_config.common.use_hot_start:
            self.matsim_config.common.hot_start_plans_file = 'todo'
        
        # matsim_config/plan_calc_score parameter
        self.matsim_config.plan_calc_score.work_activity_opening_time = plan_calc_score['work_activity_opening_time']
        self.matsim_config.plan_calc_score.home_activity_typical_duration = plan_calc_score['home_activity_typical_duration']
        self.matsim_config.plan_calc_score.work_activity_typical_duration = plan_calc_score['work_activity_typical_duration']
        self.matsim_config.plan_calc_score.work_activity_latest_start_time = plan_calc_score['work_activity_latest_start_time']
        self.matsim_config.plan_calc_score.activityType_0 = 'home'
        self.matsim_config.plan_calc_score.activityType_1 = 'work'

        
        
        # setting destination location for generated matsim config       
        self.config_destination_location = self.__set_config_destination( self.config_dictionary )
        
    def __get_external_matsim_config_for_current_year(self, external_matsim_config, year):
        
        if external_matsim_config != None:
            try:
                path = external_matsim_config[str(year)]
                return self.__get_file_location( path )
            except:
                logger.log_status("There is no external MATSim configuration set for the current year!")
        
        return ""   
    
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
            path = paths.get_opus_home_path( file_path )
            if os.path.exists( path ):
                return path

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
        else:
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
    
    def checkAndCreateFolder(self, path):
        if not os.path.exists(path):
            msg = "Folder %s dosn't exist and is created ..." % (path)
            try:
                logger.log_status(msg)
                os.makedirs(path)
                logger.log_status("done!")
            except: 
                logger.log_error("Folder could not be created!")
            
    def __get_value_as_boolean(self, option, sub_config):
        ''' if a value (option) is listed in the sub_config, than it is marked in the config checkbox'''
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
        urbansim_parameter_elem = pyxb_matsim_config_parser.urbansimParameterType.Factory()
        matsim4urbansim_controler_elem = pyxb_matsim_config_parser.matsim4urbansimContolerType.Factory()
        accessibility_parameter_elem = pyxb_matsim_config_parser.accessibilityParameterType.Factory()
        
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
        
        urbansim_parameter_elem.populationSamplingRate      = self.population_sampling_rate
        urbansim_parameter_elem.randomLocationDistributionRadiusForUrbanSimZone = self.random_location_distribution_radius_for_urbansim_zone
        urbansim_parameter_elem.year                        = self.year
        urbansim_parameter_elem.opusHome                    = self.opus_home
        urbansim_parameter_elem.opusDataPath                = self.opus_data_path
        urbansim_parameter_elem.matsim4opus                 = self.matsim4opus_path
        urbansim_parameter_elem.matsim4opusConfig           = self.matsim_config_path
        urbansim_parameter_elem.matsim4opusOutput           = self.matsim_output_path
        urbansim_parameter_elem.matsim4opusTemp             = self.matsim_temp_path
        urbansim_parameter_elem.isTestRun                   = self.isTestRun
        urbansim_parameter_elem.testParameter               = self.test_parameter
        urbansim_parameter_elem.backupRunData               = self.backup_run_data
        
        matsim4urbansim_controler_elem.zone2zoneImpedance   = self.zone2zone_impedance
        matsim4urbansim_controler_elem.zoneBasedAccessibility= self.zone_based_accessibility
        matsim4urbansim_controler_elem.cellBasedAccessibility= self.cell_based_accessibility
        matsim4urbansim_controler_elem.cellSizeCellBasedAccessibility= self.cell_size
        matsim4urbansim_controler_elem.shapeFileCellBasedAccessibility= shapefile_elem
        matsim4urbansim_controler_elem.useCustomBoundingBox = self.use_bounding_box
        matsim4urbansim_controler_elem.boundingBoxTop       = self.bounding_box_top
        matsim4urbansim_controler_elem.boundingBoxLeft      = self.bounding_box_left
        matsim4urbansim_controler_elem.boundingBoxRight     = self.bounding_box_right
        matsim4urbansim_controler_elem.boundingBoxBottom    = self.bounding_box_bottom
        matsim4urbansim_controler_elem.agentPerformance     = self.agent_performance 
        
        accessibility_parameter_elem.accessibilityDestinationSamplingRate = self.accessibility_destination_sampling_rate
        accessibility_parameter_elem.useLogitScaleParameterFromMATSim= self.use_logit_scale_parameter_from_MATSim
        accessibility_parameter_elem.useCarParameterFromMATSim= self.use_car_parameter_from_MATSim
        accessibility_parameter_elem.useWalkParameterFromMATSim= self.use_walk_parameter_from_MATSim
        accessibility_parameter_elem.useRawSumsWithoutLn    = self.use_raw_sums_without_ln
        accessibility_parameter_elem.logitScaleParameter    = self.logit_scale_parameter
        accessibility_parameter_elem.betaCarTravelTime      = self.betacar_travel_time
        accessibility_parameter_elem.betaCarTravelTimePower2= self.betacar_travel_time_power2
        accessibility_parameter_elem.betaCarLnTravelTime    = self.betacar_ln_travel_time
        accessibility_parameter_elem.betaCarTravelDistance  = self.betacar_travel_distance
        accessibility_parameter_elem.betaCarTravelDistancePower2= self.betacar_travel_distance_power2
        accessibility_parameter_elem.betaCarLnTravelDistance= self.betacar_ln_travel_distance
        accessibility_parameter_elem.betaCarTravelCost      = self.betacar_travel_cost
        accessibility_parameter_elem.betaCarTravelCostPower2= self.betacar_travel_cost_power2
        accessibility_parameter_elem.betaCarLnTravelCost    = self.betacar_ln_travel_cost
        accessibility_parameter_elem.betaWalkTravelTime     = self.betawalk_travel_time
        accessibility_parameter_elem.betaWalkTravelTimePower2= self.betawalk_travel_time_power2
        accessibility_parameter_elem.betaWalkLnTravelTime   = self.betawalk_ln_travel_time
        accessibility_parameter_elem.betaWalkTravelDistance = self.betawalk_travel_distance
        accessibility_parameter_elem.betaWalkTravelDistancePower2= self.betawalk_travel_distance_power2
        accessibility_parameter_elem.betaWalkLnTravelDistance= self.betawalk_ln_travel_distance
        accessibility_parameter_elem.betaWalkTravelCost     = self.betawalk_travel_cost
        accessibility_parameter_elem.betaWalkTravelCostPower2= self.betawalk_travel_cost_power2
        accessibility_parameter_elem.betaWalkLnTravelCost   = self.betawalk_ln_travel_cost
        
        # assemble single elements with dedicated section elements
        config_elem.matsim_config                           = matsim_config_elem
        config_elem.network                                 = network_elem
        config_elem.inputPlansFile                          = input_plans_file_elem
        config_elem.hotStartPlansFile                       = hotstart_plans_file_elem
        config_elem.controler                               = controler_elem
        config_elem.planCalcScore                           = plan_calc_score_elem
        config_elem.strategy                                = strategy_elem
        
        matsim4urbansim_elem.urbansimParameter              = urbansim_parameter_elem
        matsim4urbansim_elem.matsim4urbansimContoler        = matsim4urbansim_controler_elem
        matsim4urbansim_elem.accessibilityParameter         = accessibility_parameter_elem
        
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
        travel_model_configuration = self.config_dictionary['travel_model_configuration']   # contains matsim4urbansim and matsim_config parameter
        
        # matsim4urbansim
        matsim4urbansim = travel_model_configuration['matsim4urbansim']                     # contains parameter for matsim/urbansim integration
        
        # matsim_config
        matsim_config = travel_model_configuration['matsim_config']                         # contains various matsim_config parameter 
        accessibility = matsim_config['accessibility']
        common = matsim_config['common']
        plan_calc_score = matsim_config['plan_calc_score']
        
        return matsim4urbansim, matsim_config, accessibility, common, plan_calc_score
    
    
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
        