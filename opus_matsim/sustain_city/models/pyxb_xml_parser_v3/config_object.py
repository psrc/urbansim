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
        
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass

        self.config_dictionary = config
        self.sub_config_exists = False
        self.config_destination_location = None
        
        # TODO IMPLEMENTATION
        # - configurable time-of-a-day for which to compute the travel data (default 8 am)
        
        # get sub dictionaries from travel model configuration
        matsim4urbansim, matsim_controler, matsim_controler_parameter, matsim_accessibility_parameter, matsim_common, matsim_plan_calc_score, matsim_strategy = self.__get_travel_model_sub_dictionaries()
        
        # this serves as an indicator in MATSim
        self.project_name = self.config_dictionary['project_name']
        
        # network parameter
        self.network_file = self.__get_file_location( matsim_common['matsim_network_file'], required=True)
        
        # input plans file parameter
        self.input_plans_file = self.__get_plans_file(matsim_common, warmstart_flag)
        self.hotstart_plans_file = self.__get_plans_file(matsim_common, hotstart_flag)
        
        # controler parameter
        self.first_iteration = first_iteration
        self.last_iteration = matsim_common['last_iteration']
        self.matsim_configuration = self.__get_external_matsim_config_for_current_year(matsim_common['external_matsim_config'], year)
        
        # planCalcScoreType
        self.activityType_0                 = activity_type_0
        self.activityType_1                 = activity_type_1
        self.home_activity_typical_duration = matsim_plan_calc_score['home_activity_typical_duration']
        self.work_activity_typical_duration = matsim_plan_calc_score['work_activity_typical_duration']
        self.work_activity_opening_time     = matsim_plan_calc_score['work_activity_opening_time']
        self.work_activity_latest_start_time= matsim_plan_calc_score['work_activity_latest_start_time']
        
        # strategyType
        self.max_agent_plan_memory_size     = matsim_strategy['max_agent_plan_memory_size']
        self.time_accocation_mutator_probability = matsim_strategy['time_accocation_mutator_probability']
        self.change_exp_beta_probability    = matsim_strategy['change_exp_beta_probability']
        self.reroute_dijkstra_probability   = matsim_strategy['reroute_dijkstra_probability']
        
        # urbansim parameter
        self.year = year
        self.population_sampling_rate = matsim4urbansim['population_sampling_rate']
        select_zone_location_distribution_method = matsim4urbansim['select_zone_location_distribution_method']
        self.use_shape_file_location_distribution = self.__get_value_as_boolean('use_shape_file_location_distribution', select_zone_location_distribution_method)
        self.urbansim_zone_shape_file_location_distribution = matsim4urbansim['urbansim_zone_shape_file_location_distribution']
        self.urbansim_zone_radius_location_distribution = matsim4urbansim['urbansim_zone_radius_location_distribution']
        
        self.time_of_day                  = matsim4urbansim['time_of_day']

        self.opus_home = paths.get_opus_home_path()
        self.opus_data_path = paths.get_opus_data_path_path()
        
        self.matsim4opus_path = paths.get_opus_home_path( matsim4opus )
        self.checkAndCreateFolder(self.matsim4opus_path)
        self.matsim_config_path = os.path.join( self.matsim4opus_path, matsim_config )
        self.checkAndCreateFolder(self.matsim_config_path)
        self.matsim_output_path = os.path.join( self.matsim4opus_path, matsim_output )
        self.checkAndCreateFolder(self.matsim_output_path)
        self.matsim_temp_path = os.path.join( self.matsim4opus_path, matsim_temp )
        self.checkAndCreateFolder(self.matsim_temp_path)
        
        self.isTestRun = False
        self.test_parameter = ""
        try:
            self.test_parameter = matsim_common[ test_parameter ]
        except: pass
        self.backup_run_data = self.__get_value_as_boolean( backup_run_data, matsim_common['backup'])

        # matsim4urbansim controler
        self.zone2zone_impedance      = self.__get_value_as_boolean( 'zone2zone_impedance', matsim_controler )
        self.agent_performance        = self.__get_value_as_boolean( 'agent_performance', matsim_controler )
        self.zone_based_accessibility = self.__get_value_as_boolean( 'zone_based_accessibility', matsim_controler )
        self.cell_based_accessibility = self.__get_value_as_boolean( 'cell_based_accessibility', matsim_controler )
        self.cell_size                = matsim_controler_parameter['cell_size']
        self.use_bounding_box         = self.__get_value_as_boolean( 'use_bounding_box', matsim_controler_parameter['bounding_box'])
        self.bounding_box_top         = matsim_controler_parameter['bounding_box_top']
        self.bounding_box_left        = matsim_controler_parameter['bounding_box_left']
        self.bounding_box_right       = matsim_controler_parameter['bounding_box_right']
        self.bounding_box_bottom      = matsim_controler_parameter['bounding_box_bottom']
        self.shape_file               = self.__get_file_location( matsim_controler_parameter['shape_file'] )
        
        # matsim4urbansim accessibility parameter
        self.opportunity_sampling_rate              = matsim_accessibility_parameter['opportunity_sampling_rate']
        select_MATSim_parameter                     = matsim_accessibility_parameter['select_MATSim_parameter']
        self.use_logit_scale_parameter_from_MATSim  = self.__get_value_as_boolean( 'use_logit_scale_parameter_from_MATSim', select_MATSim_parameter )
        self.use_car_parameter_from_MATSim          = self.__get_value_as_boolean( 'use_car_parameter_from_MATSim', select_MATSim_parameter )
        self.use_bike_parameter_from_MATSim         = self.__get_value_as_boolean( 'use_bike_parameter_from_MATSim', select_MATSim_parameter )
        self.use_walk_parameter_from_MATSim         = self.__get_value_as_boolean( 'use_walk_parameter_from_MATSim', select_MATSim_parameter )
        self.use_raw_sums_without_ln                = self.__get_value_as_boolean( 'use_raw_sums_without_ln', select_MATSim_parameter )
        self.logit_scale_parameter                  = matsim_accessibility_parameter['logit_scale_parameter']
        # beta car values
        car_parameter                               = matsim_accessibility_parameter['car_parameter']
        self.betacar_travel_time                    = car_parameter['betacar_travel_time']
        self.betacar_travel_time_power2             = car_parameter['betacar_travel_time_power2']
        self.betacar_ln_travel_time                 = car_parameter['betacar_ln_travel_time']
        self.betacar_travel_distance                = car_parameter['betacar_travel_distance']
        self.betacar_travel_distance_power2         = car_parameter['betacar_travel_distance_power2']
        self.betacar_ln_travel_distance             = car_parameter['betacar_ln_travel_distance']
        self.betacar_travel_cost                    = car_parameter['betacar_travel_cost']
        self.betacar_travel_cost_power2             = car_parameter['betacar_travel_cost_power2']
        self.betacar_ln_travel_cost                 = car_parameter['betacar_ln_travel_cost']
        # beta bike values
        bike_parameter                              = matsim_accessibility_parameter['bike_parameter']
        self.betabike_travel_time                   = bike_parameter['betabike_travel_time']
        self.betabike_travel_time_power2            = bike_parameter['betabike_travel_time_power2']
        self.betabike_ln_travel_time                = bike_parameter['betabike_ln_travel_time']
        self.betabike_travel_distance               = bike_parameter['betabike_travel_distance']
        self.betabike_travel_distance_power2        = bike_parameter['betabike_travel_distance_power2']
        self.betabike_ln_travel_distance            = bike_parameter['betabike_ln_travel_distance']
        self.betabike_travel_cost                   = bike_parameter['betabike_travel_cost']
        self.betabike_travel_cost_power2            = bike_parameter['betabike_travel_cost_power2']
        self.betabike_ln_travel_cost                = bike_parameter['betabike_ln_travel_cost']
        # beta walk values
        walk_parameter                              = matsim_accessibility_parameter['walk_parameter']
        self.betawalk_travel_time                   = walk_parameter['betawalk_travel_time']
        self.betawalk_travel_time_power2            = walk_parameter['betawalk_travel_time_power2']
        self.betawalk_ln_travel_time                = walk_parameter['betawalk_ln_travel_time']
        self.betawalk_travel_distance               = walk_parameter['betawalk_travel_distance']
        self.betawalk_travel_distance_power2        = walk_parameter['betawalk_travel_distance_power2']
        self.betawalk_ln_travel_distance            = walk_parameter['betawalk_ln_travel_distance']
        self.betawalk_travel_cost                   = walk_parameter['betawalk_travel_cost']
        self.betawalk_travel_cost_power2            = walk_parameter['betawalk_travel_cost_power2']
        self.betawalk_ln_travel_cost                = walk_parameter['betawalk_ln_travel_cost']
        
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
                os.mkdir(path)
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
        logger.log_status("Generating MATSim4UrbanSin configuration at " + self.config_destination_location)
        
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
        
        urbansim_parameter_elem.projectName                 = self.project_name
        urbansim_parameter_elem.populationSamplingRate      = self.population_sampling_rate
        urbansim_parameter_elem.year                        = self.year
        urbansim_parameter_elem.opusHome                    = self.opus_home
        urbansim_parameter_elem.opusDataPath                = self.opus_data_path
        urbansim_parameter_elem.matsim4opus                 = self.matsim4opus_path
        urbansim_parameter_elem.matsim4opusConfig           = self.matsim_config_path
        urbansim_parameter_elem.matsim4opusOutput           = self.matsim_output_path
        urbansim_parameter_elem.matsim4opusTemp             = self.matsim_temp_path
        urbansim_parameter_elem.useShapefileLocationDistribution = self.use_shape_file_location_distribution
        urbansim_parameter_elem.urbanSimZoneShapefileLocationDistribution = self.urbansim_zone_shape_file_location_distribution
        urbansim_parameter_elem.urbanSimZoneRadiusLocationDistribution = self.urbansim_zone_radius_location_distribution
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
        matsim4urbansim_controler_elem.timeOfADay           = self.time_of_day
        
        accessibility_parameter_elem.opportunitiySamplingRate = self.opportunity_sampling_rate
        accessibility_parameter_elem.useLogitScaleParameterFromMATSim= self.use_logit_scale_parameter_from_MATSim
        accessibility_parameter_elem.useCarParameterFromMATSim= self.use_car_parameter_from_MATSim
        accessibility_parameter_elem.useBikeParameterFromMATSim= self.use_bike_parameter_from_MATSim
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
        accessibility_parameter_elem.betaBikeTravelTime     = self.betabike_travel_time
        accessibility_parameter_elem.betaBikeTravelTimePower2= self.betabike_travel_time_power2
        accessibility_parameter_elem.betaBikeLnTravelTime   = self.betabike_ln_travel_time
        accessibility_parameter_elem.betaBikeTravelDistance = self.betabike_travel_distance
        accessibility_parameter_elem.betaBikeTravelDistancePower2= self.betabike_travel_distance_power2
        accessibility_parameter_elem.betaBikeLnTravelDistance= self.betabike_ln_travel_distance
        accessibility_parameter_elem.betaBikeTravelCost     = self.betabike_travel_cost
        accessibility_parameter_elem.betaBikeTravelCostPower2= self.betabike_travel_cost_power2
        accessibility_parameter_elem.betaBikeLnTravelCost   = self.betabike_ln_travel_cost
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
            
        logger.log_status( "Generating MATSim4UrbanSim configuration done!" )
        
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
        matsim_accessibility_parameter = matsim4urbansim['accessibility_parameter']
        # matsim_config
        matsim_config = travel_model_configuration['matsim_config']                       # contains various matsim_config parameter 
        matsim_common = matsim_config['common']
        matsim_plan_calc_score = matsim_config['plan_calc_score']
        matsim_strategy = matsim_config['strategy']
        
        return matsim4urbansim, matsim_controler, matsim_controler_parameter, matsim_accessibility_parameter, matsim_common, matsim_plan_calc_score, matsim_strategy
    
    
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
        