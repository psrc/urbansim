# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from lxml import etree
from opus_core import paths
from opus_matsim.sustain_city.models.pyxb_xml_parser import pyxb_matsim_config_parser_v3
from pyxb.utils.domutils import BindingDOMSupport
import pyxb

class MATSimConfigObjectV3(object):
    
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
        
        # get directories
        self.opus_home = paths.get_opus_home_path()
        self.opus_data_path = paths.get_opus_data_path_path()
        self.matsim4opus_path = paths.get_opus_home_path( 'matsim4opus' )
        self.checkAndCreateFolder(self.matsim4opus_path)
        cache_directory = config['cache_directory']
        matsim4opus_target_path = os.path.join(cache_directory, 'matsim4opus') 
        self.matsim_config_path = os.path.join( matsim4opus_target_path, 'matsim_config' )
        
        
        # get sub dictionaries from travel model configuration

        # get travel model parameter from the opus dictionary
        travel_model_configuration = self.config_dictionary['travel_model_configuration']   # contains matsim4urbansim and matsim_config parameter
        
        # matsim4urbansim
        self.matsim4urbansim_dict = travel_model_configuration['matsim4urbansim']                     # contains parameter for matsim/urbansim integration
        
        # matsim_config
        self.matsim_config_dict = travel_model_configuration['matsim_config']                         # contains various matsim_config parameter 
        self.accessibility_dict = self.matsim_config_dict['accessibility']
        self.urbansim_zone_random_location_distribution_dict = self.matsim_config_dict['urbansim_zone_random_location_distribution']
        self.common_dict = self.matsim_config_dict['common']
        self.plan_calc_score_dict = self.matsim_config_dict['plan_calc_score']
        
        ###########################
        # matsim4urbansim parameter
        ###########################
        self.matsim4urbansim_population_sampling_rate =   self.matsim4urbansim_dict['population_sampling_rate']
        self.matsim4urbansim_custom_parameter =   self.matsim4urbansim_dict['custom_parameter']
        self.matsim4urbansim_backup = self.__get_value_as_boolean('backup_run_data',   self.matsim4urbansim_dict['backup'])
        self.matsim4urbansim_matsim_data_to_compute_zone2zone_impedance = self.__get_value_as_boolean('zone2zone_impedance',   self.matsim4urbansim_dict['matsim_data_to_compute'])
        self.matsim4urbansim_matsim_data_to_compute_agent_performance = self.__get_value_as_boolean('agent_performance',  self.matsim4urbansim_dict['matsim_data_to_compute'])
        self.matsim4urbansim_matsim_data_to_compute_zone_based_accessibility = self.__get_value_as_boolean('zone_based_accessibility',   self.matsim4urbansim_dict['matsim_data_to_compute'])
        self.matsim4urbansim_matsim_data_to_compute_parcel_based_accessibility = self.__get_value_as_boolean('parcel_based_accessibility',   self.matsim4urbansim_dict['matsim_data_to_compute'])
        self.matsim4urbansim_year = year
        self.matsim4urbansim_matsim_config_path = os.path.join( matsim4opus_target_path, 'matsim_config' )
        self.checkAndCreateFolder(self.matsim4urbansim_matsim_config_path)
        self.matsim4urbansim_matsim_output_path = os.path.join( matsim4opus_target_path, 'output' )
        self.checkAndCreateFolder(self.matsim4urbansim_matsim_output_path)
        self.matsim4urbansim_matsim_temp_path = os.path.join( matsim4opus_target_path, 'tmp' )
        self.checkAndCreateFolder(self.matsim4urbansim_matsim_temp_path)
        
        
        ###########################
        # matsim_config parameter
        ###########################
        self.matsim_config_urbansim_zone_random_location_distribution_by_radius = self.urbansim_zone_random_location_distribution_dict['by_radius']
        self.matsim_config_urbansim_zone_random_location_distribution_by_shape_file = self.__get_string_value(self.urbansim_zone_random_location_distribution_dict['by_zone_shape_file'])
        
        # matsim_config/accessibility parameter
        self.matsim_config_accessibility_cell_size = self.accessibility_dict['cell_size']
        self.matsim_config_accessibility_study_area_boundary_shape_file = self.__get_string_value(self.accessibility_dict['study_area_boundary_shape_file'])
        self.matsim_config_accessibility_bounding_box_left = self.accessibility_dict['bounding_box_left']
        self.matsim_config_accessibility_bounding_box_bottom = self.accessibility_dict['bounding_box_bottom']
        self.matsim_config_accessibility_bounding_box_top = self.accessibility_dict['bounding_box_top']
        self.matsim_config_accessibility_bounding_box_right = self.accessibility_dict['bounding_box_right']
        accessibility_computation_area = self.accessibility_dict['accessibility_computation_area'] # loading sub directory ...
        if not(accessibility_computation_area.__len__ != 1):
            logger.log_error("Please select ONE item in 'travel_model_configuration/matsim_config/accessibility/accessibility_computation_area' to determine how the study area for the accessibility computation!")
            exit()
        self.matsim_config_accessibility_accessibility_computation_area_from_shapefile = self.__get_value_as_boolean( 'from_shapefile', accessibility_computation_area )
        self.matsim_config_accessibility_accessibility_computation_area_from_bounding_box = self.__get_value_as_boolean( 'from_bounding_box', accessibility_computation_area )
        self.matsim_config_accessibility_accessibility_computation_area_from_network = self.__get_value_as_boolean( 'from_network', accessibility_computation_area )
        
        # matsim_config/common parameter
        self.matsim_config_common_network_file = self.__get_file_location( self.common_dict['network'], required=True)
        self.matsim_config_common_first_iteration = 0
        self.matsim_config_common_last_iteration = self.common_dict['last_iteration']
        self.matsim_config_common_external_matsim_configuration = self.__get_external_matsim_config_for_current_year(self.common_dict['external_matsim_config'], year)
        self.matsim_config_common_warm_start_plans_file = self.__get_plans_file(self.common_dict, 'warm_start_plans_file')
        self.matsim_config_common_use_hot_start = self.__get_value_as_boolean( 'use_hot_start', self.common_dict['hot_start'] )
        self.matsim_config_common_hot_start_plans_file = ''
        if self.matsim_config_common_use_hot_start:
            self.matsim_config_common_hot_start_plans_file = os.path.join(matsim4opus_target_path, 'hot_start_plans_file.xml.gz')
        
        # matsim_config/plan_calc_score parameter
        self.matsim_config_plan_calc_score_work_activity_opening_time = self.plan_calc_score_dict['work_activity_opening_time']
        self.matsim_config_plan_calc_score_home_activity_typical_duration = self.plan_calc_score_dict['home_activity_typical_duration']
        self.matsim_config_plan_calc_score_work_activity_typical_duration = self.plan_calc_score_dict['work_activity_typical_duration']
        self.matsim_config_plan_calc_score_work_activity_latest_start_time = self.plan_calc_score_dict['work_activity_latest_start_time']
        self.matsim_config_plan_calc_score_activityType_0 = 'home'
        self.matsim_config_plan_calc_score_activityType_1 = 'work'

        # setting destination location for generated matsim config       
        self.config_destination_location = os.path.join( self.matsim_config_path, config['project_name'] + "_matsim_config.xml"  )
        logger.log_status('MATSim4UrbanSim config file will be written to %s' %self.config_destination_location)
        
    def __get_external_matsim_config_for_current_year(self, external_matsim_config, year):
        
        if external_matsim_config != None:
            try:
                path = external_matsim_config[str(year)]
                return self.__get_file_location( path )
            except:
                logger.log_status("There is no external MATSim configuration set for the current year!")
        
        return ""   
    
    def __get_string_value(self, value):
        if value == None:
            return ""
        return value
    
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
        root = pyxb_matsim_config_parser_v3.matsim4urbansim_configType.Factory()
        
        # main elements
        matsim_config_elem   = pyxb_matsim_config_parser_v3.matsim_configType.Factory()
        matsim4urbansim_elem = pyxb_matsim_config_parser_v3.matsim4urbansimType.Factory()
        
        # init matsim config elem
        matsim4urbansim_elem.populationSamplingRate = self.matsim4urbansim_population_sampling_rate
        matsim4urbansim_elem.year                   = self.matsim4urbansim_year
        matsim4urbansim_elem.opusHome               = self.opus_home
        matsim4urbansim_elem.opusDataPath           = self.opus_data_path
        matsim4urbansim_elem.matsim4opus            = self.matsim4opus_path
        matsim4urbansim_elem.matsim4opusConfig      = self.matsim4urbansim_matsim_config_path
        matsim4urbansim_elem.matsim4opusOutput      = self.matsim4urbansim_matsim_output_path
        matsim4urbansim_elem.matsim4opusTemp        = self.matsim4urbansim_matsim_temp_path
        matsim4urbansim_elem.customParameter        = self.matsim4urbansim_custom_parameter
        matsim4urbansim_elem.zone2ZoneImpedance     = self.matsim4urbansim_matsim_data_to_compute_zone2zone_impedance
        matsim4urbansim_elem.agentPerfomance        = self.matsim4urbansim_matsim_data_to_compute_agent_performance
        matsim4urbansim_elem.zoneBasedAccessibility = self.matsim4urbansim_matsim_data_to_compute_zone_based_accessibility
        matsim4urbansim_elem.parcelBasedAccessibility= self.matsim4urbansim_matsim_data_to_compute_parcel_based_accessibility
        matsim4urbansim_elem.backupRunData          = self.matsim4urbansim_backup
        
        # init matsim 4 urbansim config elem
        matsim_config_elem.cellSize                                   = self.matsim_config_accessibility_cell_size
        matsim_config_elem.accessibilityComputationAreaFromShapeFile  = self.matsim_config_accessibility_accessibility_computation_area_from_shapefile
        matsim_config_elem.accessibilityComputationAreaFromBoundingBox= self.matsim_config_accessibility_accessibility_computation_area_from_bounding_box
        matsim_config_elem.accessibilityComputationAreaFromNetwork    = self.matsim_config_accessibility_accessibility_computation_area_from_network
        matsim_config_elem.studyAreaBoundaryShapeFile                 = self.matsim_config_accessibility_study_area_boundary_shape_file
        matsim_config_elem.boundingBoxTop                             = self.matsim_config_accessibility_bounding_box_top
        matsim_config_elem.boundingBoxLeft                            = self.matsim_config_accessibility_bounding_box_left
        matsim_config_elem.boundingBoxRight                           = self.matsim_config_accessibility_bounding_box_right
        matsim_config_elem.boundingBoxBottom                          = self.matsim_config_accessibility_bounding_box_bottom
        matsim_config_elem.urbansimZoneRandomLocationDistributionByRadius = self.matsim_config_urbansim_zone_random_location_distribution_by_radius
        matsim_config_elem.urbansimZoneRandomLocationDistributionByShapeFile=self.matsim_config_urbansim_zone_random_location_distribution_by_shape_file
        matsim_config_elem.external_matsim_config                     = self.matsim_config_common_external_matsim_configuration
        matsim_config_elem.network                                    = self.matsim_config_common_network_file
        matsim_config_elem.warmStartPlansFile                         = self.matsim_config_common_warm_start_plans_file
        matsim_config_elem.useHotStart                                = self.matsim_config_common_use_hot_start
        matsim_config_elem.hotStartPlansFile                          = self.matsim_config_common_hot_start_plans_file
        matsim_config_elem.activityType_0                             = self.matsim_config_plan_calc_score_activityType_0
        matsim_config_elem.activityType_1                             = self.matsim_config_plan_calc_score_activityType_1
        matsim_config_elem.homeActivityTypicalDuration                = self.matsim_config_plan_calc_score_home_activity_typical_duration
        matsim_config_elem.workActivityTypicalDuration                = self.matsim_config_plan_calc_score_work_activity_typical_duration
        matsim_config_elem.workActivityOpeningTime                    = self.matsim_config_plan_calc_score_work_activity_opening_time
        matsim_config_elem.workActivityLatestStartTime                = self.matsim_config_plan_calc_score_work_activity_latest_start_time
        matsim_config_elem.firstIteration                             = self.matsim_config_common_first_iteration
        matsim_config_elem.lastIteration                              = self.matsim_config_common_last_iteration
        
        
        # assemble single elements to root
        root.matsim_config  = matsim_config_elem
        root.matsim4urbansim= matsim4urbansim_elem
        
        # content = root.content() # get children
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        # convert to dom object
        dom = root.toDOM(element_name='matsim4urbansim_config')
        # print on screen
        prettydom = dom.toprettyxml(encoding="UTF-8")
        prettydom = str.replace(prettydom, '<matsim4urbansim_config>', '<matsim4urbansim_config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.matsim.org/files/dtd/matsim4urbansim_v3.xsd">')
        
        logger.log_status( 'Generated MATSim configuration file:' )
        logger.log_status( prettydom )
        logger.log_status( 'Writing (marschalling) this matsim config xml to {0}'.format( self.config_destination_location ) )
        
        file_object = open(self.config_destination_location, 'w')
        file_object.write(prettydom)
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status( "Finished Marschalling" )
        
        return self.config_destination_location
    
    
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
