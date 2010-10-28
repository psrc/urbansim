# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
import opus_matsim.sustain_city.tests.psrc_measurements as psrc_path

class PsrcResults(object):

    # singelton instance to hold a reference to PsrcResults singelton
    instance = None
    
    class PsrcResultHelper:
        
        def __call__(self, *args, **kw):
            # if an instance of PsrcResults does not exist,
            # create one and assign it to TestSingleton.instance.
            if PsrcResults.instance is None :
                PsrcResults.instance = PsrcResults()

            # return PsrcResults.instance, which should contain
            # a reference to the only instance of PsrcResults
            # in the system.
            return PsrcResults.instance
    
    # call the class level method to get the single instance of PsrcResults.
    getInstance = PsrcResultHelper()

    def __init__(self):
        
        if PsrcResults.instance == None:
            self.logfile_path = psrc_path.__path__[0]
            self.size_person_table = -1
            self.size_parcel_table = -1
            self.size_matsim_config = -1
            self.size_travel_data = -1
            self.duration_writing_tabels = -1
            self.duration_writing_config = -1
            self.duration_reading_travel_data = -1
        else:
            logger.log_status('PsrcResults is already instanciated!!!')
        
    def setTableSizes(self, person, parcel):
        self.size_person_table = person
        self.size_parcel_table = parcel
        
    def setConfigSize(self, matsim):
        self.size_matsim_config = matsim
        
    def setTravelDataSize(self, td_size):
        self.size_travel_data = td_size
        
    def setDurationTabels(self, tabels):
        self.duration_writing_tabels = tabels
        
    def setDurationConfig(self, config):
        self.duration_writing_config = config
        
    def setDurationTravelData(self, td):
        self.duration_reading_travel_data = td
        
    def printResults(self):
        logger.start_block('PSRC measurements results')
        logger.log_status('Size of person table in bytes: %i' %self.size_person_table)
        logger.log_status('Size of parcel table in bytes: %i' %self.size_parcel_table)
        logger.log_status('Duration writing tables in seconds: %i' %self.duration_writing_tabels)
        logger.log_status('')
        logger.log_status('Size of matsim config: in bytes %i' %self.size_matsim_config)
        logger.log_status('Duration writing config in seconds: %i' %self.duration_writing_config)
        logger.log_status('')
        logger.log_status('Size of travel data in bytes: %i' %self.size_travel_data)
        logger.log_status('Duration reading travel data in seconds: %i' %self.duration_reading_travel_data)
        logger.end_block('')
    
    def dump_logfile(self):
        
        logger.log_status('Dumping logfile...')
        
        destination = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp', 'psrc_log.txt')
        
        file_object = open( destination , 'w')
        
        file_object.write('PSRC measurements results\n')
        file_object.write('=========================\n') 
        file_object.write('\n') 
        file_object.write('Size of person table in bytes:%s\n'%self.size_person_table) 
        file_object.write('Size of parcel table in bytes:%s\n'%self.size_parcel_table) 
        file_object.write('Duration writing tables in seconds:%s\n'%self.duration_writing_tabels) 
        file_object.write('\n') 
        file_object.write('Size of matsim config in bytes:%s\n'%self.size_matsim_config) 
        file_object.write('Duration writing config in seconds:%s\n'%self.duration_writing_config) 
        file_object.write('\n') 
        file_object.write('Size of travel data in bytes:%s\n'%self.size_travel_data) 
        file_object.write('Duration reading travel data: in seconds:%s\n'%self.duration_reading_travel_data) 
        
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status('Finished dumping logfile.')
        
if __name__ == "__main__":
    
    # create a test instance
    instance = PsrcResults.getInstance()
    instance.setTableSizes(500, 500)
    instance.setConfigSize(100)
    instance.setTravelDataSize(200)
    instance.setDurationTabels(1234)
    instance.setDurationConfig(2345)
    instance.setDurationTravelData(3456)
    
    # test the implementation of the Singleton pattern.  all of the
    # references printed out should have the same values and the same address.
    
    for i in range(5):
        tmp_instance = PsrcResults.getInstance()
        logger.log_status(tmp_instance)
        tmp_instance.printResults()
    
    # this call should show a message indicating
    # that a single instance of PsrcResults already exists.
    PsrcResults()
    
        