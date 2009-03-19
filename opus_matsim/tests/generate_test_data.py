# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from numpy import array
import os



class GenerateTestData(object):
    """ I don't think this is used anywhere
    """

    def run(self, config, year, *args, **kwargs):
        """ """
        logger.start_block('Starting GenerateTestData.run(...)')
        
        cache_dir_w_year = os.path.join(config['cache_directory'],year.__str__())
        
        storage = StorageFactory().get_storage('flt_storage', storage_location = cache_dir_w_year )
        storage.write_table(table_name = 'persons',
                            table_data = {'person_id':    array([1,2,3]),
                                          'household_id': array([1,2,3]),
                                          'job_id':       array([4,5,6])
                                          }
                            )
        storage.write_table(table_name = 'households',
                            table_data = {'household_id':    array([1,2,3]),
                                          'building_id': array([1,2,3]),
                                          }
                            )
        storage.write_table(table_name = 'jobs',
                            table_data = {'job_id':    array([4,5,6]),
                                          'building_id': array([4,5,6]),
                                          }
                            )
        storage.write_table(table_name = 'buildings',
                            table_data = {'building_id':    array([1,2,3,4,5,6]),
                                          'parcel_id': array([1,2,3,4,5,6]),
                                          }
                            )
        storage.write_table(table_name = 'parcels',
                            table_data = {'parcel_id':    array([1,2,3,4,5,6]),
                                          'x_coord_sp': array([1.,2.,3.,4.,5.,6.]),
                                          'y_coord_sp': array([1.,2.,3.,4.,5.,6.]),
                                          'zone_id': array([1,1,1,3,3,3]),
                                          }
                            )

        logger.end_block()        
        


# the following is needed, since it is called as "main" from the framework ...  
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
    GenerateTestData().run(resources, options.year)
    
