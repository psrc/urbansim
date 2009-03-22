# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import string
import sys
import time
import re
from opus_core.logger import logger
from numpy import round_, zeros
from travel_model_input_file_writer import TravelModelInputFileWriter as BMTravelModelInputFileWriter
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.variables.attribute_type import AttributeType

class TravelModelInputFileWriterWithObservedValues(BMTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. 
        It uses the observed number of households and jobs.
    """
    log_file_name = 'run_travel_model_with_observed_data.log'
    storage_type_of_observed_files = 'tab_storage'
    file_with_observed_households = "PSRC2005TAZDataNew" 
    file_with_observed_jobs = "jobs_by_zones_and_groups"
    directory = "/Users/hana/bm/observed_data"
    
    def _do_setup(self, *args, **kwargs):
        BMTravelModelInputFileWriter._do_setup(self, *args, **kwargs)
        storage = StorageFactory().get_storage(self.storage_type_of_observed_files, storage_location=self.directory)
        self.observed_zones_with_households = DatasetFactory().search_for_dataset('zone', ['urbansim'], 
                                arguments={'in_storage':storage, 'in_table_name': self.file_with_observed_households})
        self.observed_zones_with_households.load_dataset()
        self.observed_zones_with_jobs =  DatasetFactory().search_for_dataset('zone', ['urbansim'], 
                                arguments={'in_storage':storage, 'in_table_name': self.file_with_observed_jobs})
        self.observed_zones_with_jobs.load_dataset()
        self.total_number_of_jobs = zeros(self.observed_zones_with_jobs.size(), dtype='int32')
        for attr in self.observed_zones_with_jobs.get_known_attribute_names():
            if attr not in self.observed_zones_with_jobs.get_id_name():
                self.total_number_of_jobs = self.total_number_of_jobs + self.observed_zones_with_jobs.get_attribute(attr)

    def generate_travel_model_input(self, zone_set):
        self._determine_current_share(zone_set)
        for attr in self.observed_zones_with_households.get_known_attribute_names()+self.observed_zones_with_jobs.get_known_attribute_names():
            if attr in zone_set.get_known_attribute_names() and attr not in zone_set.get_id_name():
                zone_set.delete_one_attribute(attr)
        zone_set.join(self.observed_zones_with_households, self.observed_zones_with_households.get_known_attribute_names(), metadata=AttributeType.PRIMARY, 
                      return_value_if_not_found=0)
        zone_set.join(self.observed_zones_with_jobs, self.observed_zones_with_jobs.get_known_attribute_names(), metadata=AttributeType.PRIMARY, 
                      return_value_if_not_found=0)
        self._set_travel_model_input(zone_set)
        
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        self._modify_variable_set()
        BMTravelModelInputFileWriter._write_to_file(self, zone_set, variables_list, tm_input_file)
        
    def _modify_variable_set(self):
        self.full_variable_list[8:20] = self.variables_for_direct_matching['job']
            
    def _set_travel_model_input(self, zone_set):
        zone_ids = zone_set.get_id_attribute()
        # set household input
        dataset_name = 'household'
        number_of_agents = zone_set.get_attribute("number_of_%ss" % dataset_name)
        logger.log_status('Observed number of %ss' % dataset_name)
        logger.log_status(round_(number_of_agents))
        for var, ratios in self.variables_to_scale[dataset_name].iteritems():
            self.simulated_values[var] = zeros(zone_set.size())
            self.simulated_values[var] = (round_(number_of_agents*ratios)).astype(self.simulated_values[var].dtype)
            logger.log_status(var)
            logger.log_status(self.simulated_values[var])

        # set job input
        dataset_name = 'job'
        zone_set.compute_variables(self.variables_for_direct_matching[dataset_name], dataset_pool=self.dataset_pool)
        logger.log_status('Observed values for %ss:' % dataset_name)
        for var in self.variables_for_direct_matching[dataset_name]:
            self.simulated_values[var] = zone_set.get_attribute(var)
            logger.log_status(var)
            logger.log_status(self.simulated_values[var])
                

            
from opus_core.tests import opus_unittest
import tempfile
import shutil
from numpy import array, arange
from opus_core.misc import write_to_text_file, write_table_to_text_file
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.zone_dataset import ZoneDataset
from opus_core.datasets.dataset_pool import DatasetPool

class TestTMInputWriter(opus_unittest.OpusTestCase):
    def test_generate_input(self):
        # prepare file with observed data
        temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        temp_file_jobs = os.path.join(temp_dir, "observed_jobs.tab")
        write_to_text_file(temp_file_jobs, array(['zone_id', "number_of_jobs_of_sector_group_retail", "number_of_jobs_of_sector_group_manu"]), delimiter='\t')
        jobs_data = array([[1, 90, 10],
                           [2, 1500, 0],
                           [3, 50, 2000],
                           [4, 20, 0],
                           [6, 100, 0],
                           [7, 5, 5],
                           [8, 0, 93],
                           [9, 1005, 940],
                           [10, 785, 1]])
        write_table_to_text_file(temp_file_jobs,  jobs_data, mode='a', delimiter='\t')                 

        temp_file_households = os.path.join(temp_dir, "observed_households.tab")
        write_to_text_file(temp_file_households, array(['zone_id', "number_of_households"]), delimiter='\t')
        households_data = array([
                           [1, 20],
                           [2, 10],
                           [3, 44],
                           [5, 21],
                           [6, 5],
                           [7, 0],
                           [8, 76],
                           [9, 6],
                           [10, 100]])
        write_table_to_text_file(temp_file_households,  households_data, mode='a', delimiter='\t') 
         
        high_income = array([5, 0, 5, 1, 0, 60, 10, 7, 0, 0])
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name = "zones",
            table_data = {
                "zone_id": arange(10)+1,
                "number_of_jobs_of_sector_group_retail": array([100, 2000, 0, 40, 23, 35, 0, 1, 900, 879]),
                "number_of_jobs_of_sector_group_manu": array([0, 0, 2030, 20, 421, 0, 3, 97, 600, 0]),
                "density": array([1,1,1,1,1,2,2,2,2,2]),
                }
            )
        storage.write_table(
            table_name = "households",
            table_data = {
                "household_id": arange(221)+1,
                "zone_id": array(10*[1] + 25*[3] + [4] + 100*[6] + 30*[7] + 43*[8] + 2*[9] + 10*[10]),
                "is_high_income": array(5*[True] + 5*[False] + 5*[True] + 20*[False] + [True] + 60*[True]+ 40*[False] + 10*[True] + 20*[False] + 7*[True] + 36*[False] + 2*[False] + 10*[False])
                }
            )
        zones = ZoneDataset(in_storage=storage)
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        tmiw = TravelModelInputFileWriterWithObservedValues()
        
        tmiw.variables_to_scale = {
            'household': {
                    "high_income = zone.aggregate(household.is_high_income)": None,
                    "low_income = zone.aggregate(numpy.logical_not(household.is_high_income))": None,
                        }
                          }
        tmiw.variables_for_direct_matching = {
          'job': [
                  "retail1 = (zone.density==1) * zone.number_of_jobs_of_sector_group_retail",
                  "retail2 = (zone.density==2) * zone.number_of_jobs_of_sector_group_retail",
                  "manu = zone.number_of_jobs_of_sector_group_manu"
                  ]
          }
        tmiw.file_with_observed_households = "observed_households"
        tmiw.file_with_observed_jobs = "observed_jobs"
        tmiw.directory = temp_dir
        
        tmiw._do_setup(2010, dataset_pool, enable_file_logging=False)
        zones.compute_variables(tmiw.variables_to_scale['household'].keys(), dataset_pool = tmiw.dataset_pool)
        
        tmiw.generate_travel_model_input(zones)
        shutil.rmtree(temp_dir)
        
if __name__ == '__main__':
    opus_unittest.main()