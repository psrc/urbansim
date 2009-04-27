# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, concatenate, where
from opus_core.model import Model
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from urbansim.models.subarea_employment_transition_model import SubareaEmploymentTransitionModel

class ProcessEmploymentEvents(Model):
    
    model_name = 'Process Employment Events'
    
    _location_dataset_name_default = 'parcel'
    _job_location_id_name_default = 'building_id'
    
    def __init__(self, location_dataset_name=None, job_location_id_name=None, dataset_pool=None):
        Model.__init__(self)
        self.dataset_pool = self.create_dataset_pool(dataset_pool)
        self._location_dataset_name = self._location_dataset_name_default
        self._job_location_id_name = self._job_location_id_name_default
        if location_dataset_name is not None:
            self._location_dataset_name = location_dataset_name
        if job_location_id_name is not None:
            self._job_location_id_name = job_location_id_name
        self.location_dataset = self.dataset_pool.get_dataset(self._location_dataset_name)
        
    def run(self, employment_events, jobs, current_year):
        """ 
        Update the jobs dataset to accommodate employment events. The employment_events dataset should have
        columns 'parcel_id', 'scheduled_year', 'number_of_home_based_jobs', 'number_of_non_home_based_jobs',
        'sector_id', 'replace_home_based_jobs' (optional), 'replace_non_home_based_jobs' (optional).
        Negative events should be given by negative values in number_of_xxx_jobs. If it is a 'replace' event, 
        the 'replace_xxx_jobs' columnn should have one for that event (default is 0).
        """
        # select events for the current year
        events_for_this_year = DatasetSubset(employment_events, 
                                             index=where(employment_events.get_attribute('scheduled_year')==current_year)[0])
        
        # create control totals on the fly
        control_totals = self.create_control_totals(events_for_this_year, jobs, year=current_year)
        
        # run subarea employment transition model in order to create or delete the given number of jobs
        ETM = SubareaEmploymentTransitionModel(subarea_id_name=self.location_dataset.get_id_name()[0], 
                                               location_id_name=self._job_location_id_name, dataset_pool=self.dataset_pool)
        return ETM.run(current_year, jobs, control_totals, self.dataset_pool.get_dataset('job_building_type'))
        
        
    def create_control_totals(self, employment_events, jobs, year):
        all_sectors = employment_events.get_attribute('sector_id')
        unique_sectors = unique_values(all_sectors)
        for sector_id in unique_sectors:
            self.location_dataset.compute_variables(
                    ['number_of_hb_jobs_of_sector_%s = %s.aggregate(urbansim.job.is_in_employment_sector_%s_home_based, [building])' % 
                         (sector_id, self._location_dataset_name, sector_id),
                     'number_of_nhb_jobs_of_sector_%s = %s.aggregate(urbansim.job.is_in_employment_sector_%s_non_home_based, [building])' % 
                         (sector_id, self._location_dataset_name, sector_id)
                     ],
                    dataset_pool=self.dataset_pool)
        if 'replace_home_based_jobs' in employment_events.get_known_attribute_names():
            replace_hb = employment_events.get_attribute('replace_home_based_jobs')
        else:
            replace_hb = zeros(employment_events.size(), dtype='bool8')
        if 'replace_non_home_based_jobs' in employment_events.get_known_attribute_names():
            replace_nhb = employment_events.get_attribute('replace_non_home_based_jobs')
        else:
            replace_nhb = zeros(employment_events.size(), dtype='bool8')
            
        if 'number_of_non_home_based_jobs' in employment_events.get_known_attribute_names():
            number_of_nonhb = employment_events.get_attribute('number_of_non_home_based_jobs')
        else:
            number_of_nonhb = zeros(employment_events.size(), dtype='int32')
            
        if 'number_of_home_based_jobs' in employment_events.get_known_attribute_names():
            number_of_hb = employment_events.get_attribute('number_of_home_based_jobs')
        else:
            number_of_hb = zeros(employment_events.size(), dtype='int32')
            
        hbj = array([], dtype='int32')
        nhbj = array([], dtype='int32')
        all_parcels = employment_events.get_attribute('parcel_id')
        for i in range(employment_events.size()):
            sector_id = all_sectors[i]
            loc_idx = self.location_dataset.get_id_index(all_parcels)[i]
            if replace_hb[i] == 1:
                hbj = concatenate((hbj, array([number_of_hb[i]])))
            else:
                hbj = concatenate((hbj, 
                       array([self.location_dataset.get_attribute_by_index('number_of_hb_jobs_of_sector_%s' % sector_id, loc_idx) + 
                               number_of_hb[i]])))
            if replace_nhb[i] == 1:
                nhbj = concatenate((nhbj, array([number_of_nonhb[i]])))
            else:
                nhbj = concatenate((nhbj, 
                       array([self.location_dataset.get_attribute_by_index('number_of_nhb_jobs_of_sector_%s' % sector_id, loc_idx) + 
                               number_of_nonhb[i]])))
            
        
        control_totals_data = {
            self.location_dataset.get_id_name()[0]: all_parcels,
            "sector_id": all_sectors,
            "year": array(employment_events.size()*[year], dtype='int32'),
            "total_home_based_employment": hbj,
            "total_non_home_based_employment" : nhbj
            }
        storage = StorageFactory().get_storage('dict_storage')
        table_name = 'employment_control_totals_by_%s' % self._location_dataset_name
        storage.write_table(
            table_name=table_name,
            table_data=control_totals_data)
        return Dataset(in_storage=storage, in_table_name=table_name, dataset_name='control_total', id_name=[])
        
from opus_core.tests import opus_unittest
from numpy import array, logical_and, int32, int8, zeros, arange
from numpy import ma
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        #since the initial conditions for jobs are the same across tests,
        #(each test starts with the same number of jobs in grid_id X and sector_id Y)
        self.possible_grid_ids = [1,2,3]
        self.possible_sector_ids = [1,2,15]
        comc = 1
        indc = 3
        govc = 2
        hbc = 4

        storage = StorageFactory().get_storage('dict_storage')

        job_building_types_table_name = 'job_building_types'
        storage.write_table(
            table_name = job_building_types_table_name,
            table_data = {
                "id":array([govc,comc,indc,hbc]),
                "name": array(["governmental", "commercial", "industrial", "home_based"]),
                "home_based": array([0, 0, 0, 1])
                }
            )

        storage.write_table(
            table_name = 'parcels',
            table_data = {
                  'parcel_id': array([1,2,3])
                          }
                            )
        storage.write_table(
            table_name = 'buildings',
            table_data = {
                  'building_id': array([1,2,3]),
                  'parcel_id': array([1,2,3])
                          }
                            )
        
        self.jobs_data = {
             "job_id": arange(13000)+1,
             "building_id": array(6000*[1] + 4000*[2] + 3000*[3]), # corresponds to parcel_id
             "sector_id": array(4000*[1] + 1000*[2] + 1000*[15] + 2000*[1] + 1000*[2] + 1000*[15] +
                            1000*[1] + 1000*[2] + 1000*[15], dtype=int32),
             "building_type": array(2000*[indc]+2000*[comc] + # sector 1, area 1
                                    300*[indc] + 600*[comc] + 100*[govc] + # sector 2, area 1
                                    1000*[indc] + # sector 15, area 1
                                    1000*[indc]+ 1000*[comc] + # sector 1, area 2
                                    300*[indc] + 600*[comc] + 100*[govc] + # sector 2, area 2
                                    1000*[indc] + # sector 15, area 2
                                    500*[indc]+500*[comc] + # sector 1, area 2
                                    300*[indc] + 600*[comc] + 100*[govc] + # sector 2, area 2
                                    1000*[indc], # sector 15, area 2
                                    dtype=int8)
             }
        storage.write_table(table_name = 'jobs', table_data = self.jobs_data)
        
        self.employment_events_data = {
           'parcel_id':                     array([2,     2,    3,     1,   1]),
           'scheduled_year':                array([2006, 2008, 2008, 2006, 2006]),
           'number_of_non_home_based_jobs': array([3500, 500, -100,   0,   100]),
           'sector_id':                     array([1,     2,    15,    2,    1]),
           'replace_non_home_based_jobs':   array([0,     0,     0,    1,    0])
        }
        storage.write_table(table_name = 'employment_events', table_data = self.employment_events_data)
        self.dataset_pool = DatasetPool(storage=storage, package_order=['urbansim_parcel', 'urbansim'])

    def test_run_model(self):
        model = ProcessEmploymentEvents(dataset_pool=self.dataset_pool)
        job_set = self.dataset_pool.get_dataset('job')
        # run 2006
        model.run(self.dataset_pool.get_dataset('employment_event'), job_set, current_year=2006)
        results = self.get_count_all_sectors_and_areas(job_set)
 
        expected_results = array([4100, 0, 1000, 5500, 1000, 1000, 1000, 1000, 1000])
        self.assertEqual(ma.allequal(results, expected_results), True)
        
        # run 2008
        model.run(self.dataset_pool.get_dataset('employment_event'), job_set, current_year=2008)
        results = self.get_count_all_sectors_and_areas(job_set)
 
        expected_results = array([4100, 0, 1000, 5500, 1500, 1000, 1000, 1000, 900])
        self.assertEqual(ma.allequal(results, expected_results), True)
 

    def get_count_all_sectors_and_areas(self, job_set):
        res = zeros(3 * len(self.possible_sector_ids))
        i=0
        for area in [1, 2, 3]:
            tmp = job_set.get_attribute("parcel_id") == area
            for sector_id in self.possible_sector_ids:
                res[i] = logical_and(job_set.get_attribute("sector_id") == sector_id, tmp).sum()
                i+=1
        return res

    def get_count_all_sectors(self, job_set):
        res = zeros(len(self.possible_sector_ids))
        i=0
        for sector_id in self.possible_sector_ids:
            res[i] = where(job_set.get_attribute("sector_id") == sector_id)[0].size
            i+=1
        return res

if __name__=='__main__':
    opus_unittest.main()
