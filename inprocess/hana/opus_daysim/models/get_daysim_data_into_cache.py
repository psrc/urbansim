# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.session_configuration import SessionConfiguration
from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, float32, ones
import os, shutil
from opus_core.logger import logger
from inprocess.hana.opus_daysim.models.abstract_daysim_travel_model import AbstractDaysimTravelModel
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.travel_data_link_dataset import TravelDataLinkDataset

class GetDaysimDataIntoCache(AbstractDaysimTravelModel):
    """Class to copy DaySim results into the UrbanSim cache.
    """
    
    def run(self, year, skim_directory=None):
        """ It gets the appropriate values from the 
        travel_model_configuration part of this config, and then copies the specified 
        data into the specified travel_data variable names.  Results in
        a new travel_data cache for year+1.
        """
        cache_directory = self.config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        simulation_state.set_cache_directory(cache_directory)
        
        year_config = self.config['travel_model_configuration'][year]
        self.write_travel_data(year, cache_directory)

            
    def write_travel_data(self, year, cache_directory):
        """
        """        
        table_name = 'travel_data_link'
        in_storage = StorageFactory().get_storage('dict_storage')
        in_storage.write_table(
                table_name=table_name,
                table_data={
                    'travel_data_link_id': array([1]),
                    'data_link': array([self.get_daysim_skim_dir(year)]),
                    }
            )
        travel_data = TravelDataLinkDataset(in_storage=in_storage, in_table_name=table_name)
        logger.start_block('Writing data to cache')
        try:
            next_year = year + 1
            out_storage = AttributeCache().get_flt_storage_for_year(next_year)
            travel_data.write_dataset(attributes='*', 
                                          out_storage=out_storage, 
                                          out_table_name=table_name)
        finally:
            logger.end_block()
            

        
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
    parser.add_option("--skim_directory", dest="skim_directory", default=None, 
                      help="Directory with skim files in hdf5 format.")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                         
                         in_storage=AttributeCache())
        
#    logger.enable_memory_logging()
    GetDaysimDataIntoCache(resources).run(options.year, options.skim_directory)

