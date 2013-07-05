# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

#from urbansim.datasets.travel_data_daset import TravelDataDataset
from opus_core.resources import Resources
from numpy import array, float32, ones
import os
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory

class GetTravelModelDataIntoCache(AbstractTravelModel):
    """Class to copy travel model results into the UrbanSim cache.
    """

    def run(self, config, year, *args, **kwargs):
        """This is the main entry point.  It gets the appropriate values from the 
        travel_model_configuration part of this config, and then copies the specified 
        data into the specified travel_data variable names.  Results in
        a new travel_data cache for year+1.
        """
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        simulation_state.set_cache_directory(cache_directory)
        
        logger.start_block('Getting data from travel model')
        next_year = year + 1
        flt_dir_for_next_year = os.path.join(cache_directory, str(next_year))
        if not os.path.exists(flt_dir_for_next_year):
            os.mkdir(flt_dir_for_next_year)
        attribute_cache = AttributeCache()        
        dataset_pool = SessionConfiguration(new_instance=True,
                                            package_order=config['dataset_pool_configuration'].package_order,
                                            in_storage=attribute_cache).get_dataset_pool()
        zone_set = dataset_pool.get_dataset('travel_zone')

#        zone_set = ZoneDataset(in_storage_location=flt_dir_for_this_year, 
#                               in_storage_type='flt_storage', 
#                               in_table_name='zones')
        zone_set.load_dataset()
        self.prepare_for_run(config['travel_model_configuration'], year)
        travel_data_set = self.get_travel_data_from_travel_model(config, year, zone_set, 
                                                                 *args, **kwargs)
        logger.end_block()
        
        logger.start_block('Writing travel data to cache')
        out_storage = StorageFactory().get_storage('flt_storage', storage_location = flt_dir_for_next_year)
        #out_storage = flt_storage(Resources(data={"storage_location":flt_dir_for_next_year}))
        travel_data_set.write_dataset(attributes=travel_data_set.get_known_attribute_names(), 
                                      out_storage=out_storage, 
                                      out_table_name='travel_data')
        logger.end_block()

    def prepare_for_run(self, *args, **kwargs):
        pass
    
    def get_travel_data_from_travel_model(self, config, year, zone_set, *args, **kwargs):
        """"""
        raise NotImplementedError, "subclass responsibility"
        
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.utils.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetTravelModelDataIntoCache().run(resources, options.year)    
