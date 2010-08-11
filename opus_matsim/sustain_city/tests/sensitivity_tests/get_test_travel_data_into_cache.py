# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.variables.attribute_type import AttributeType
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.csv_storage import csv_storage
from opus_core.store.attribute_cache import AttributeCache
import opus_matsim.sustain_city.tests as test_dir

class GetTestTravelDataIntoCache(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """ Integrates modified travel times and pre-computed travel costs
            into the UrbanSim cache.
        """
        
        logger.log_status('Starting GetTestTravelDataIntoCache.get_travel_data...')
        
        # get sensitivity test path asan anchor to determine the location of the MATSim travel_data file (see below).
        test_dir_path = test_dir.__path__[0]
        
        # for debugging
        try: #tnicolai
            import pydevd
            pydevd.settrace()
        except: pass

        # get the exsisting travel data from the current year
        logger.log_status('Loading travel data from UrbanSim cache (year:%i)' % year)
        table_name = "travel_data"
        cache_storage = AttributeCache().get_flt_storage_for_year(year)
        existing_travel_data_set = TravelDataDataset( in_storage=cache_storage, in_table_name=table_name )


        ###### modifyed travel time travel data
        logger.log_status('Integrating modifyed travel times in year %i for next simulation year.')
        input_directory = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "tmp" )
        logger.log_status("input_directory: " + input_directory )
        # location of the modified travel time travel_data
        in_storage = csv_storage(storage_location = input_directory)
        # create travel data set (travel times)
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )

        # join the modifyed travel times with the travel data set of the current year
        existing_travel_data_set.join(travel_data_set, travel_data_set.get_non_id_primary_attribute_names(),metadata=AttributeType.PRIMARY)


        ##### pre-calcualted MATSim travel data (travel costs)
#        logger.log_status('Integrating pre-calculated travel costs (MATSim) in year %i for next simulation year.')
#        input_directory = os.path.join( test_dir_path, 'data', 'travel_cost')
#        logger.log_status("input_directory: " + input_directory )
#        # check source file
#        if not os.path.exists( input_directory ):
#            print 'File not found! %s' % input_directory
#            sys.exit()
        # location of pre-calculated MATSim travel costs
#        in_storage = csv_storage(storage_location = input_directory)
        # create travel data set (travel costs)
#        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )

        # join travel data set from pre-calcualted MATSim results
#        existing_travel_data_set.join(travel_data_set, travel_data_set.get_non_id_primary_attribute_names(),metadata=AttributeType.PRIMARY)

        
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
    GetTestTravelDataIntoCache().run(resources, options.year)
