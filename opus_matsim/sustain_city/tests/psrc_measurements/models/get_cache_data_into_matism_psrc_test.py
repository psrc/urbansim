# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import time, os
from opus_matsim.sustain_city.models.get_cache_data_into_matsim import GetCacheDataIntoMatsim
from opus_core.logger import logger
from opus_core.resources import Resources

class GetCacheDataIntoMatsimPsrcTest(GetCacheDataIntoMatsim):

    def create_travel_model_input_file(self, config, year, *args, **kwargs):
        
        # execute the export 
        self.start_time = time.time()
        GetCacheDataIntoMatsim.create_travel_model_input_file(self, config, year)
        self.end_time = time.time()
        
        # gather measurement data
        extension = self.dataset_table_persons.get_file_extension()
        
        person_file = os.path.join( self.output_directory, 
                                    self.dataset_table_persons.get_file_name(year, suppress_extension_addition=True) ) + '.' + extension
        parcel_file = os.path.join( self.output_directory, 
                                    self.dataset_table_parcels.get_file_name(year, suppress_extension_addition=True) ) + '.' + extension
        
        # store results in logfile
        self.dump_results(config, 
                          int( os.path.getsize(person_file) ),
                          int ( os.path.getsize(parcel_file) ),
                          int ( self.end_time-self.start_time ) )
        
    def dump_results(self, config, person_file, parcel_file, duration):
        
        logger.log_status('Loging results...')
        
        file = config['psrc_logfile']
        
        # append measurements to log file
        file_object = open( file , 'a') 
        
        file_object.write('Size of person table in MBytes:%f\n'%(person_file/(1024.0**2))) 
        file_object.write('Size of parcel table in MBytes:%f\n'%(parcel_file/(1024.0**2))) 
        file_object.write('Duration writing tables in seconds:%f\n'%duration) 
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
    GetCacheDataIntoMatsimPsrcTest().run(resources, options.year)