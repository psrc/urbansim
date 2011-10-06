# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, opus_matsim
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.variables.attribute_type import AttributeType
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.csv_storage import csv_storage
from opus_core.store.attribute_cache import AttributeCache

class GetMatsimDataIntoCacheDummy(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """
    
    def init(self, year, config):
        self.input_directory = os.path.join( opus_matsim.__path__[0], 'tests', 'testdata' )
        logger.log_status("input_directory: " + self.input_directory )
        self.in_storage = csv_storage(storage_location = self.input_directory)
        self.cache_storage = AttributeCache().get_flt_storage_for_year(year)
        self.cache_directory = config['cache_directory']
        
        self.travel_data_table_name = "travel_data"
        self.zone_table_name = "zones"

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """ Reads the output from the travel model and imports the fresh computed travel data attributes into the cache. 
        """
        logger.log_status('Starting GetMatsimDataIntoCache.get_travel_data...')
        
        #try: # tnicolai :for debugging
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        self.init(year, config);
        
        # tnicolai: experimental -> import workplace accessibility from matsim
        #self.get_workplace_accessibility_into_cache(year)
        
        # import travel data from matsim
        travel_data_set = TravelDataDataset( in_storage=self.in_storage, in_table_name=self.travel_data_table_name )
        
        # load actual travel data set from cache
        existing_travel_data_set = TravelDataDataset( in_storage=self.cache_storage, in_table_name=self.travel_data_table_name )
        
        # join remaining data set with imported travel data
        existing_travel_data_set.join(travel_data_set, travel_data_set.get_non_id_primary_attribute_names(),metadata=AttributeType.PRIMARY)
        
        # return new travel data set
        return existing_travel_data_set

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
    GetMatsimDataIntoCacheDummy().run(resources, options.year)
