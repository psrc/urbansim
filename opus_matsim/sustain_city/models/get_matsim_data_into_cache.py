# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.variables.attribute_type import AttributeType
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.csv_storage import csv_storage
from opus_core.store.attribute_cache import AttributeCache

class GetMatsimDataIntoCache(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """
        """
        logger.log_status('Starting GetMatsimDataIntoCache.get_travel_data...')
#        print >> sys.stderr, "MATSim replaces only _some_ of the columns of travel_data.  Yet, Urbansim does not truly merge them"
#        print >> sys.stderr, " but simply overwrites the columns, without looking for a different sequence of from_zone_id, to_zone_id"
        # solved 3dec08 by hana
        input_directory = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "tmp" )
        logger.log_status("input_directory: " + input_directory )

        in_storage = csv_storage(storage_location = input_directory)

        table_name = "travel_data"
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )

        cache_storage = AttributeCache().get_flt_storage_for_year(year)
        existing_travel_data_set = TravelDataDataset( in_storage=cache_storage, in_table_name=table_name )
        ##TODO:This may not work or may be wrong after the id_names of travel_data 
        ##changed from ['from_zone_id', 'to_zone_id'] to _hidden_id (lmwang)
        existing_travel_data_set.join(travel_data_set, travel_data_set.get_non_id_primary_attribute_names(),metadata=AttributeType.PRIMARY)
        
        return existing_travel_data_set


# this is needed since it is called from opus via "main":        
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
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetMatsimDataIntoCache().run(resources, options.year)
