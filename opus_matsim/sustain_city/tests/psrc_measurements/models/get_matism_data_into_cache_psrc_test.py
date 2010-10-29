# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import time, os
from opus_matsim.sustain_city.models.get_matsim_data_into_cache import GetMatsimDataIntoCache
from opus_core.logger import logger
from opus_core.resources import Resources

class GetMatsimDataIntoCachePsrcTest(GetMatsimDataIntoCache):

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        
        # execute the import 
        self.start_time = time.time()
        existing_travel_data_set = GetMatsimDataIntoCache.get_travel_data_from_travel_model(self, config, year, zone_set)
        self.end_time = time.time()
        
        # gather measurement data
        travel_data = os.path.join( self.input_directory, 
                                    self.table_name + '.csv')
        
        # store results in logfile
        self.dump_results(config, 
                          int( os.path.getsize(travel_data) ),
                          int ( self.end_time-self.start_time ) )
        
        return existing_travel_data_set
        
    def dump_results(self, config, travel_data, duration):
        
        logger.log_status('Loging results...')
        
        file = config['psrc_logfile']
        
        # append measurements to log file
        file_object = open( file , 'a') 
        
        file_object.write('Size of travel data in MBytes:%f\n'%(travel_data/(1024.0**2)))
        file_object.write('Duration reading and joning travel data in seconds:%f\n'%duration) 
        file_object.write('\n')
        
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status('Finished loging.')

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
    GetMatsimDataIntoCachePsrcTest().run(resources, options.year)