# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.zone_dataset import ZoneDataset
from opus_core.storage_factory import StorageFactory

class ModifyMatsimData(GetTravelModelDataIntoCache):
    """ Reduces the accessibility values of zones that belong to the city of Brussels. Other zones are not manipulated.
        This class is supposed to run for some sensitivity tests. Dot not use for regular runs!!!
    """
    
    def init(self, year, config):
        
        self.cache_storage = AttributeCache().get_flt_storage_for_year(year)
        self.cache_directory = config['cache_directory']
        self.matsim_controler = self.__get_matsim_controler_section(config)
        self.zone_table_name        = "zones"
        self.travel_data_table_name = "travel_data"
        self.factor            = 10.

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """ Reads the output from the travel model and imports the fresh computed travel data into the cache. 
        """
        logger.log_status('Starting ModifyMatsimData...')

        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        self.init(year, config);
        
        if( self.__get_value_as_boolean('zone_based_accessibility', self.matsim_controler) ):
            self.modify_zone_based_accessibility_into_cache(year)
        
        # just load and retunrs unmodified trave ldata
        existing_travel_data_set = TravelDataDataset( in_storage=self.cache_storage, in_table_name=self.travel_data_table_name )    
        return existing_travel_data_set  
    
    def modify_zone_based_accessibility_into_cache(self, year):
        """ Modifies accessibility results from MATSim in 
            UrbanSim cache (zones table)
        """
        logger.log_status('Importing zone-based accessibility indicators from MATSim ...')
        
        existing_zone_data_set = ZoneDataset( in_storage=self.cache_storage, in_table_name=self.zone_table_name )
        
        for zone_id in range(1318,2042):
            # get row index of zone_id 
            index = existing_zone_data_set.get_id_index(zone_id)
            # get and modify car accessibility
            car_accessibility = existing_zone_data_set.get_attribute_by_index('car_accessibility', index)
            car_accessibility = car_accessibility / self.factor 
            existing_zone_data_set.modify_attribute('car_accessibility', car_accessibility, index )
            # get and modify walk accessibility
            walk_accessibility = existing_zone_data_set.get_attribute_by_index('walk_accessibility', index)
            walk_accessibility = walk_accessibility / self.factor 
            existing_zone_data_set.modify_attribute('walk_accessibility', walk_accessibility, index )
            # get and modify bike accessibility
            #bike_accessibility = existing_zone_data_set.get_attribute_by_index('bike_accessibility', index)
            #bike_accessibility = bike_accessibility / self.factor 
            #existing_zone_data_set.modify_attribute('bike_accessibility', bike_accessibility, index )
            # get and modify free accessibility
            #freespeed_accessibility = existing_zone_data_set.get_attribute_by_index('freespeed_accessibility', index)
            #freespeed_accessibility = freespeed_accessibility / self.factor 
            #existing_zone_data_set.modify_attribute('freespeed_accessibility', freespeed_accessibility, index )
        
        logger.log_status('Writing modified zone data to cache ...')
        flt_dir_for_next_year = os.path.join(self.cache_directory, str(year+1))
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_dir_for_next_year)
        existing_zone_data_set.write_dataset(attributes=existing_zone_data_set.get_known_attribute_names(),
                                             out_storage=out_storage,
                                             out_table_name=self.zone_table_name)
        
        logger.log_status('Finished modifying zone-based accessibility indicators in zone dataset.')
    
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
    ModifyMatsimData().run(resources, options.year)
