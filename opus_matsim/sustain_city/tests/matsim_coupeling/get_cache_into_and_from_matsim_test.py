# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest
from opus_core.logger import logger
import opus_matsim.sustain_city.tests as test_path
import tempfile
from shutil import rmtree
from opus_matsim.sustain_city.tests.common.extract_zip_file import ExtractZipFile
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
from opus_core.store.csv_storage import csv_storage
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.attribute_cache import AttributeCache

class IOCacheMATSimTestRun(object): #opus_unittest.OpusTestCase):
    ''' Tests the UrbanSim export and import functionality for the travel model.
    '''

    def __setUp(self):
        print "entering __setUp"
        
        logger.log_status('Testing UrbanSim export and import functionality for MATSim...')

        # get root path to test cases
        self.path = test_path.__path__[0]
        logger.log_status('Set root path for MATSim config file to: %s' % self.path)
        if not os.path.exists(self.path):
            raise StandardError("Root path doesn't exist: %s" % self.path)
        
        # get path to MATSim source files and base_year_cache
        self.matsim_source, self.base_year_data_source = self.get_source_files() 
        self.destination = tempfile.mkdtemp(prefix='opus_tmp')
        #self.destination = '/Users/thomas/Desktop/x'    # for debugging
        #if not os.path.exists(self.destination):        # for debugging
        #    os.mkdir(self.destination)                  # for debugging
                    
        # load UrbanSim config to run MATSim test
        urbansim_config_location = os.path.join( self.path, 'configs', 'urbansim_config') #'/Users/thomas/Development/workspace/urbansim_trunk/opus_matsim/tests/test_config.xml'
        logger.log_status('Loading UrbanSim config: %s' % urbansim_config_location)
        #self.run_config = XMLConfiguration( urbansim_config_location ).get_run_configuration("Test")
        urbansim_config_name = "urbansim_config_for_matsim_run_test.xml"
        self.run_config = XMLConfiguration( os.path.join(urbansim_config_location, urbansim_config_name)).get_run_configuration("Test")
        
        # set destination for MATSim config file
        self.matsim_config_full = os.path.join( self.destination, "test_matsim_config.xml" )
        
        print "leaving __setUp"


    def tearDown(self):
        print "entering tearDown"
        logger.log_status('Removing extracted MATSim files...')
        if os.path.exists(self.destination):
            rmtree(self.destination)
        logger.log_status('... cleaning up finished.')
        print "leaving tearDown"


    def testName(self):
        print "entering test_run"
        
        logger.log_status('Preparing MATSim test run ...')
        # unzip MATSim files
        matsim_zip = ExtractZipFile(self.matsim_source, self.destination)
        matsim_zip.extract()
        matsim_extracted_files = os.path.join(self.destination, 'MATSimTestClasses') # location of unziped MATSim files
        # unzip base_year_cache
        base_year_data_zip = ExtractZipFile(self.base_year_data_source, self.destination)
        base_year_data_zip.extract()
        base_year_data_extracted_files = os.path.join(self.destination, 'base_year_data') # location of unziped base_year_cache
        
                
        # updating location of base_year_data
        self.run_config['creating_baseyear_cache_configuration'].cache_directory_root = self.destination
        self.run_config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = base_year_data_extracted_files
        self.run_config['cache_directory'] = base_year_data_extracted_files
        self.run_config.add('matsim_files', matsim_extracted_files)
        self.run_config.add('matsim_config', self.matsim_config_full)
        self.run_config.add('root', self.destination)
        
        insert_auto_generated_cache_directory_if_needed(self.run_config)
        run_manager = RunManager(ServicesDatabaseConfiguration())
    
        run_manager.setup_new_run(cache_directory = self.run_config['cache_directory'],
                                  configuration = self.run_config)

        logger.log_status('Starting UrbanSim run ... ')
        run_manager.run_run(self.run_config, run_as_multiprocess = True )
        # after the UrbanSim run the travel data sets should be equal
        self.assertTrue( self.compare_travel_data_sets() )
        logger.log_status('... UrbanSim run finished.')
        
        print "leaving test_run"
    
    def get_source_files(self):
        ''' Returns the path to the MATSim and base_year_data
            source files
        '''
        
        matsim_source_files = os.path.join( self.path, 'data', 'MATSimTestClasses.zip')
        if not os.path.exists(matsim_source_files):
            raise StandardError("MATSim source file not found: %s" % matsim_source_files)
        logger.log_status('Referring to MATSim source file: %s' % matsim_source_files)
        
        base_year_data_source_files = os.path.join( self.path, 'data', 'base_year_data.zip')
        if not os.path.exists(base_year_data_source_files):
            raise StandardError("Base year data zip file not found: %s" % base_year_data_source_files)
        logger.log_status('Referring to base year cache file: %s' % base_year_data_source_files)
       
        return matsim_source_files, base_year_data_source_files

    def compare_travel_data_sets(self):
        
        # get copied travel data csv
        copied_travel_data_location = os.path.join( self.destination, 'opus_matsim', 'tmp')
        if not os.path.exists(copied_travel_data_location):
            raise StandardError('Travel data not found: %s' % copied_travel_data_location)
        logger.log_status('Get copied travel data: %s' % copied_travel_data_location)
        # convert travel data csv into travel data set matrix
        in_storage = csv_storage(storage_location = copied_travel_data_location)
        table_name = "travel_data"
        travel_data_attribute = 'single_vehicle_to_work_travel_cost'
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )
        travel_data_attribute_mat = travel_data_set.get_attribute_as_matrix(travel_data_attribute, fill=999)
        # get exsisting travel data set and convert it also into travel data set matrix
        year = self.run_config['base_year']+2
        attribute_cache = AttributeCache(cache_directory=self.run_config['cache_directory'])
        cache_storage = attribute_cache.get_flt_storage_for_year(year)
        existing_travel_data_set = TravelDataDataset( in_storage=cache_storage, in_table_name=table_name )
        existing_travel_data_attribute_mat = existing_travel_data_set.get_attribute_as_matrix(travel_data_attribute, fill=999)
        
        from numpy import savetxt # for debugging
        savetxt( os.path.join(self.destination, 'origin_travel_data.txt'), travel_data_attribute_mat , fmt="%f")
        savetxt( os.path.join(self.destination, 'existing_travel_data') , existing_travel_data_attribute_mat, fmt="%f")
        
        # compare both data set matices
        compare = travel_data_attribute_mat == existing_travel_data_attribute_mat
        # return result
        return compare.all()     

if __name__ == "__main__":
    opus_unittest.main()