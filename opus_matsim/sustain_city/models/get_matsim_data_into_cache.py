# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.variables.attribute_type import AttributeType
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.csv_storage import csv_storage
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim_parcel.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory
from urbansim_parcel.datasets.person_dataset import PersonDataset
from opus_matsim.sustain_city.models.pyxb_xml_parser.config_object_v3 import MATSimConfigObjectV3

class GetMatsimDataIntoCache(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """
    
    def init(self, year, config):
        
        config_obj_v3 = MATSimConfigObjectV3(config, year)
        
        self.input_directory = config_obj_v3.matsim4urbansim_matsim_temp_path
        
        # self.input_directory = paths.get_opus_home_path( matsim4opus, matsim_temp )
        logger.log_status("input_directory: " + self.input_directory )
        self.in_storage = csv_storage(storage_location = self.input_directory)
        self.cache_storage = AttributeCache().get_flt_storage_for_year(year)
        self.cache_directory = config['cache_directory']
        # tnicolai: experimental code 
        self.matsim_controler = self.__get_matsim_controler_section(config)
        
        # this deletes travel model attributes from cache that are not updated/handled by the travel model (MATSim)
        self.delete_travel_data_columns = ['am_bike_to_work_travel_time', 
                                      'am_biking_person_trips',
                                      #'am_pk_period_drive_alone_vehicle_trips',
                                      'am_total_transit_time_walk',
                                      'am_transit_person_trip_table',
                                      #'am_walk_time_in_minutes',
                                      'am_walking_person_trips',
                                      'am_double_vehicle_to_work_travel_time',
                                      'am_threeplus_vehicle_to_work_travel_time',
                                      'logsum_hbw_am_income_1',
                                      'logsum_hbw_am_income_2',
                                      'logsum_hbw_am_income_3',
                                      'logsum_hbw_am_income_4',
                                      'md_vehicle_miles_traveled',
                                      'nweubk',
                                      'nweuda',
                                      'nweus2',
                                      'nweus3',
                                      'nweutw',
                                      'nweuwk',
                                      'pm_ev_ni_vehicle_miles_traveled',
                                      'single_vehicle_to_work_travel_distance']
        
        self.travel_data_table_name = "travel_data"
        self.parcel_table_name      = "parcels"
        self.zone_table_name        = "zones"
        self.person_data_table      = "persons"

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """ Reads the output from the travel model and imports the fresh computed travel data into the cache. 
        """
        logger.log_status('Starting GetMatsimDataIntoCache.get_travel_data...')
        # print >> sys.stderr, "MATSim replaces only _some_ of the columns of travel_data.  Yet, Urbansim does not truly merge them"
        # print >> sys.stderr, " but simply overwrites the columns, without looking for a different sequence of from_zone_id, to_zone_id"
        # solved 3dec08 by hana
        
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        self.init(year, config);
        
        # import parcel-based accessibilities from MATSim into parcel table
        if( self.__get_value_as_boolean('cell_based_accessibility', self.matsim_controler) ):
            self.get_parcel_based_accessibility_into_cache(year)
        # import zone-based accessibilities from MATSim into zones table
        if( self.__get_value_as_boolean('zone_based_accessibility', self.matsim_controler) ):
            self.get_zone_based_accessibility_into_cache(year)
        # import agent performances from MATSim into persons table
        if( self.__get_value_as_boolean( 'agent_performance', self.matsim_controler ) ):
            self.get_agent_performance_into_cache(year)
        
        # delete travel data attributes in UrbanSim data store (see list above: "self.delete_travel_data_columns") -> (may causes errors in some models)
        # self.clear_cache_travel_data(year) 
        # load current travel data set from cache
        existing_travel_data_set = TravelDataDataset( in_storage=self.cache_storage, in_table_name=self.travel_data_table_name )
        # import zone2zone impedances from MATSim into travel_data table
        if(self.__get_value_as_boolean('zone2zone_impedance', self.matsim_controler)):
            logger.log_status('Importing zone to zone impedances from MATSim ...')
            travel_data_set = TravelDataDataset( in_storage=self.in_storage, in_table_name=self.travel_data_table_name )
            # tnicolai : Replace travel data table 
            # Case 1) Delete all 'columns' but the 'columns' passing to urbansim first. then no join operation is needed
            # Case 2) Join the data sets and delete unneeded 'columns' here
            
            ##TODO:This may not work or may be wrong after the id_names of travel_data 
            ##changed from ['from_zone_id', 'to_zone_id'] to _hidden_id (lmwang)
            # join current data set with imported matsim travel data
            existing_travel_data_set.join(travel_data_set, travel_data_set.get_non_id_primary_attribute_names(),metadata=AttributeType.PRIMARY)
            logger.log_status('Finished join operation for zone to zone impedances (travel_data_set).') 
            
        # return new travel data set
        return existing_travel_data_set
            
    def clear_cache_travel_data(self, year):
        """ deleting unneeded travel data columns in cache
        """
        logger.log_status('Clearing travel data cache ...')
        cache_directory = AttributeCache().get_storage_location()
        dir = os.path.join(cache_directory, str(year), self.travel_data_table_name)
        if os.path.exists(dir):
            for file in self.delete_travel_data_columns:
                file = os.path.join(dir, file+'.lf4')
                if os.path.exists(file):
                    logger.log_status('Removing %s ...'%file)
                    os.remove(file)
        logger.log_status('Finished clearing.')     
        
    def get_parcel_based_accessibility_into_cache(self, year):
        """ Imports accessibility results from MATSim into 
            UrbanSim cache (parcel table)
        """
        logger.log_status('Importing parcel-based accessibility indicators from MATSim ...')
        try:
            parcel_data_set = ParcelDataset(in_storage=self.in_storage, in_table_name=self.parcel_table_name)
            
            existing_parcel_data_set = ParcelDataset( in_storage=self.cache_storage, in_table_name=self.parcel_table_name )
            
            existing_parcel_data_set.join(parcel_data_set, parcel_data_set.get_non_id_primary_attribute_names(), metadata=AttributeType.PRIMARY)
            
            logger.log_status('Writing parcel data to cache ...')
            flt_dir_for_next_year = os.path.join(self.cache_directory, str(year+1))
            out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_dir_for_next_year)
            existing_parcel_data_set.write_dataset(attributes=existing_parcel_data_set.get_known_attribute_names(),
                                                 out_storage=out_storage,
                                                 out_table_name=self.parcel_table_name)
        except:
            logger.log_warning('There is no parcel dataset! The parcel-based accessibility indicators from MATSim can not be imported!')
        
        logger.log_status('Finished importing parcel-based accessibility indicators to parcel dataset.')   
    
    def get_zone_based_accessibility_into_cache(self, year):
        """ Imports accessibility results from MATSim into 
            UrbanSim cache (zones table)
        """
        logger.log_status('Importing zone-based accessibility indicators from MATSim ...')
        
        zone_data_set = ZoneDataset(in_storage=self.in_storage, in_table_name=self.zone_table_name)
        
        existing_zone_data_set = ZoneDataset( in_storage=self.cache_storage, in_table_name=self.zone_table_name )
        
        existing_zone_data_set.join(zone_data_set, zone_data_set.get_non_id_primary_attribute_names(), metadata=AttributeType.PRIMARY)
        
        logger.log_status('Writing zone data to cache ...')
        flt_dir_for_next_year = os.path.join(self.cache_directory, str(year+1))
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_dir_for_next_year)
        existing_zone_data_set.write_dataset(attributes=existing_zone_data_set.get_known_attribute_names(),
                                             out_storage=out_storage,
                                             out_table_name=self.zone_table_name)
        
        logger.log_status('Finished importing zone-based accessibility indicators to zone dataset.')
        
    def get_agent_performance_into_cache(self, year):
        """ Imports person/agent performances, like travel durations or distances,
            from MATSim into UrbanSim cache (persons table)
        """
        logger.log_status('Importing person/agent performances from MATSim ...')
        
        person_data_set = PersonDataset( in_storage=self.in_storage, in_table_name=self.person_data_table )
        
        existing_person_data_set = PersonDataset( in_storage=self.cache_storage, in_table_name=self.person_data_table )
        
        existing_person_data_set.join(person_data_set, person_data_set.get_non_id_primary_attribute_names(), metadata=AttributeType.PRIMARY)
        
        logger.log_status('Writing person data to cache ...')
        flt_dir_for_next_year = os.path.join(self.cache_directory, str(year+1))
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_dir_for_next_year)
        existing_person_data_set.write_dataset(attributes=existing_person_data_set.get_known_attribute_names(),
                                               out_storage=out_storage,
                                               out_table_name=self.person_data_table)
        
        logger.log_status('Finished importing person/agent performances to person dataset.')
        
    def __get_matsim_controler_section(self, config):
        """ returns the matsim_controler configuration section from the travel model configuration
        """
        # get travel model parameter from the opus dictionary
        travel_model_configuration = config['travel_model_configuration']
        matsim4urbansim = travel_model_configuration['matsim4urbansim']
        return matsim4urbansim['matsim_controler']

    def __get_value_as_boolean(self, option, sub_config):
        ''' if a value (option) is listed in the sub_config, than it is marked in the config checkbox'''
        if sub_config != None and option != None:
            for param in sub_config:
                if str(param).lower() == str(option).lower():
                    return True
            return False
    
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
    GetMatsimDataIntoCache().run(resources, options.year)
