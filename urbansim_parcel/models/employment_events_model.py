# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, concatenate, where, ones, logical_and, logical_not, arange
from numpy.random import randint
from opus_core.model import Model
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from urbansim.models.subarea_employment_transition_model import SubareaEmploymentTransitionModel

class EmploymentEventsModel(Model):
    """ 
        Update the jobs dataset to accommodate employment events. The employment_events dataset should have
        the following stucture:
            'scheduled_year'
            'sector_id'
            'building_id' - optional. If negative, parcel_id must be positive
            'parcel_id' - optional but either building_id or parcel_id must be present. 
                          If negative, building_id must be positive
            'number_of_non_home_based_jobs' - optional. Default is 0 for all table entries.
            'number_of_home_based_jobs' - optional. Default is 0 for all table entries.
            'replace_non_home_based_jobs' - optional. Should have one for 'replace' events
                                            of non-home-based jobs, otherwise zeros, which is the default.
            'replace_home_based_jobs' - optional. Should have one for 'replace' events
                                        of home-based jobs, otherwise zeros, which is the default.
        Negative events should be given by negative values in number_of_xxx_jobs.
        
        The model creates or deletes jobs according to the employment events table. Created jobs are placed 
        into either given buildings or buildings within given parcels. If there are multiple buildings
        in a parcel, the jobs are randomly distributed across them. Home-based jobs are placed into residential buildings,
        Non-home-based jobs into non-residential buildings. The model does not take into account 
        available job space in the buildings.
    """
    model_name = 'Employment Events Model'
    
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
        # select events for the current year
        events_for_this_year = DatasetSubset(employment_events, 
                                             index=where(employment_events.get_attribute('scheduled_year')==current_year)[0])
        
        # create control totals on the fly
        control_totals = self.create_control_totals(events_for_this_year, jobs, year=current_year)
        
        # run subarea employment transition model in order to create or delete the given number of jobs
        ETM = SubareaEmploymentTransitionModel(subarea_id_name=self.location_dataset.get_id_name()[0], 
                                               location_id_name=self._job_location_id_name, dataset_pool=self.dataset_pool)
        etm_result = ETM.run(current_year, jobs, control_totals, self.dataset_pool.get_dataset('job_building_type'))
        
        self.place_jobs_into_buildings(events_for_this_year, jobs, etm_result)
        
        return etm_result
    
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
        if 'parcel_id' in employment_events.get_known_attribute_names():
            all_parcels = employment_events.get_attribute('parcel_id')
        else:
            all_parcels = -1*ones(employment_events.size(), dtype='int32')
        if 'building_id' in employment_events.get_known_attribute_names():
            all_buildings = employment_events.get_attribute('building_id')
            known_buildings_idx = where(all_buildings > 0)[0]
            # set parcel_ids where building is known
            if known_buildings_idx.size > 0:
                buildings = self.dataset_pool.get_dataset('building')
                try:
                    bidx = buildings.get_id_index(all_buildings[known_buildings_idx])
                except:
                    bidx = buildings.try_get_id_index(all_buildings[known_buildings_idx])
                    error_idx = where(bidx < 0)
                    logger.log_warning('Problems with buildings:')
                    logger.log_warning(all_buildings[known_buildings_idx[bidx[error_idx]]])
                    raise ValueError, 'Building(s) given for employment events do not exist.'
                
                all_parcels[known_buildings_idx] = buildings.get_attribute_by_id('parcel_id', all_buildings[known_buildings_idx])
                employment_events.modify_attribute('parcel_id', all_parcels[known_buildings_idx], index=known_buildings_idx)
        else:
            all_buildings = -1*ones(employment_events.size(), dtype='int32')

        unknown_buildings_idx = where(all_buildings < 0)[0]
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
        
    def place_jobs_into_buildings(self, employment_events, jobs, job_index):
        all_sectors = employment_events.get_attribute('sector_id')
        unique_sectors = unique_values(all_sectors)
        for sector_id in unique_sectors:
            jobs.compute_variables(['urbansim.job.is_in_employment_sector_%s_home_based' % sector_id,
                                    'urbansim.job.is_in_employment_sector_%s_non_home_based' % sector_id,
                                    'urbansim_parcel.job.parcel_id'],
                    dataset_pool=self.dataset_pool)
        placed_jobs = zeros(job_index.size, dtype='bool8')
        buildings = self.dataset_pool.get_dataset('building')
        # place jobs into known buildings
        if 'building_id' in employment_events.get_known_attribute_names():
            all_buildings = employment_events.get_attribute('building_id')
            known_buildings_idx = where(all_buildings > 0)[0]
            unknown_buildings_idx = where(all_buildings <= 0)[0]
            for i in known_buildings_idx:
                idx = where(logical_and(jobs.get_attribute_by_index('is_in_employment_sector_%s' % 
                                                        all_sectors[i], job_index),
                                        jobs.get_attribute_by_index('parcel_id', job_index) == 
                                        buildings.get_attribute_by_id('parcel_id', all_buildings[i])))[0]
                if idx.size > 0:
                    jobs.modify_attribute(name='building_id', data=array(idx.size*[all_buildings[i]]), index=job_index[idx])
                    placed_jobs[idx] = True
        else:
            unknown_buildings_idx = arange(employment_events.size())
                
        # place jobs into buildings when building_id is not known
        unplaced_jobs_idx = where(placed_jobs==0)[0]
        if unknown_buildings_idx.size > 0:
            all_parcels = employment_events.get_attribute('parcel_id')
            is_residential = buildings.compute_variables(['urbansim_parcel.building.is_residential'], 
                                                         dataset_pool=self.dataset_pool)
        for i in unknown_buildings_idx:
            idx_hb = where(logical_and(jobs.get_attribute_by_index('is_in_employment_sector_%s_home_based' % 
                                                        all_sectors[i], job_index[unplaced_jobs_idx]),
                                        jobs.get_attribute_by_index('parcel_id', job_index[unplaced_jobs_idx]) == 
                                        all_parcels[i]))[0]
            idx_nhb = where(logical_and(jobs.get_attribute_by_index('is_in_employment_sector_%s_non_home_based' % 
                                                        all_sectors[i], job_index[unplaced_jobs_idx]),
                                        jobs.get_attribute_by_index('parcel_id', job_index[unplaced_jobs_idx]) == 
                                        all_parcels[i]))[0]
            buildings_in_this_parcel = buildings.get_attribute('parcel_id')==all_parcels[i]
            if buildings_in_this_parcel.sum() <= 0:
                logger.log_warning('There are no buildings in parcel %s to place created jobs.' % all_parcels[i])
                continue
            residential_bldgs_idx = where(logical_and(buildings_in_this_parcel, is_residential))[0]
            non_residential_bldgs_idx = where(logical_and(buildings_in_this_parcel, logical_not(is_residential)))[0]
            
            if idx_hb.size > 0: # place home-based jobs
                if residential_bldgs_idx.size > 0: # into residential_buildings
                    random_order = randint(0, residential_bldgs_idx.size, idx_hb.size)
                    jobs.modify_attribute(name='building_id', 
                                          data=buildings.get_id_attribute()[residential_bldgs_idx][random_order],
                                          index=job_index[unplaced_jobs_idx[idx_hb]])
                else: # if no residential buildings available, place them into non-residential buildings
                    random_order = randint(0, non_residential_bldgs_idx.size, idx_hb.size)
                    jobs.modify_attribute(name='building_id', 
                                          data=buildings.get_id_attribute()[non_residential_bldgs_idx][random_order],
                                          index=job_index[unplaced_jobs_idx[idx_hb]])
                    logger.log_warning('There are no residential buildings in parcel %s. Home-based jobs placed into non-residential building(s).' 
                                       % all_parcels[i])
            if idx_nhb.size > 0: # place non-home-based jobs
                if non_residential_bldgs_idx.size > 0: # into non-residential_buildings
                    random_order = randint(0, non_residential_bldgs_idx.size, idx_nhb.size)
                    jobs.modify_attribute(name='building_id', 
                                          data=buildings.get_id_attribute()[non_residential_bldgs_idx][random_order],
                                          index=job_index[unplaced_jobs_idx[idx_nhb]])
                else: # if no non-residential buildings available, place them into residential buildings
                    random_order = randint(0, residential_bldgs_idx.size, idx_nhb.size)
                    jobs.modify_attribute(name='building_id', 
                                          data=buildings.get_id_attribute()[residential_bldgs_idx][random_order],
                                          index=job_index[unplaced_jobs_idx[idx_nhb]])
                    logger.log_warning('There are no non-residential buildings in parcel %s. Non-home-based jobs placed into residential building(s).' 
                                       % all_parcels[i])
            
                    
        
from opus_core.tests import opus_unittest
from numpy import array, logical_and, int32, int8, zeros, arange
from numpy import ma
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from urbansim.datasets.job_dataset import JobDataset


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
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
                  'parcel_id': array([1,2,3]),
                  'is_residential': array([0,0,0])
                          }
                            )
        
        self.jobs_data = {
             "job_id": arange(13000)+1,
             "building_id": array(6000*[1] + 4000*[2] + 3000*[3]), # corresponds to parcel_id
             "sector_id": array(4000*[1] + 1000*[2] + 1000*[15] + 2000*[1] + 1000*[2] + 1000*[15] +
                            1000*[1] + 1000*[2] + 1000*[15], dtype=int32),
             "building_type": array(2000*[indc]+2000*[comc] + # sector 1, area 1
                                    300*[indc] + 600*[comc] + 100*[hbc] + # sector 2, area 1
                                    1000*[indc] + # sector 15, area 1
                                    1000*[indc]+ 1000*[comc] + # sector 1, area 2
                                    300*[indc] + 600*[comc] + 100*[hbc] + # sector 2, area 2
                                    1000*[indc] + # sector 15, area 2
                                    500*[indc]+500*[comc] + # sector 1, area 3
                                    300*[indc] + 600*[comc] + 100*[hbc] + # sector 2, area 3
                                    1000*[indc], # sector 15, area 3
                                    dtype=int8)
             }
        storage.write_table(table_name = 'jobs', table_data = self.jobs_data)
        
        # jobs data
        ############   
#        parcel/sector       1              2              3
#            1            4000nhb         2000nhb        1000nhb
#            2            900nhb/100hb    900nhb/100hb   900nhb/100hb 
#            15           1000nhb         1000nhb        1000nhb
        
        self.employment_events_data = {
           'parcel_id':                     array([2,     2,    3,     1,   1]),
           'scheduled_year':                array([2006, 2008, 2008, 2006, 2006]),
           'number_of_non_home_based_jobs': array([3500, 500, -100,   0,   100]),
           'sector_id':                     array([1,     2,    15,    2,    1]),
           'replace_non_home_based_jobs':   array([0,     0,     0,    1,    0])
        }
        storage.write_table(table_name = 'employment_events', table_data = self.employment_events_data)
        
        # change in 2006
        ############   
#        parcel/sector       1              2              3
#            1            +100nhb         +3500nhb        --
#            2            =0nhb            --             --
#            15             --             --             --

        # change in 2008
        ############   
#        parcel/sector       1              2              3
#            1              --             --             --
#            2              --           +500nhb          --
#            15             --             --           -100nhb

        self.storage=storage

    def test_run_model(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=['urbansim_parcel', 'urbansim'])
        model = EmploymentEventsModel(dataset_pool=dataset_pool)
        job_set = dataset_pool.get_dataset('job')
        # run 2006
        model.run(dataset_pool.get_dataset('employment_event'), job_set, current_year=2006)
        results = self.get_count_all_sectors_and_areas(job_set)
        expected_results = array([4100, 100, 1000, 5500, 1000, 1000, 1000, 1000, 1000])
        self.assertEqual(ma.allequal(results, expected_results), True)
        # check locations
        buildings = dataset_pool.get_dataset('building')
        jobs_in_sec_1 = buildings.compute_variables(['urbansim_parcel.building.number_of_jobs_of_sector_1'],
                                                    dataset_pool=dataset_pool)
        self.assertEqual(ma.allequal(jobs_in_sec_1, array([4100, 5500, 1000])), True)
        # run 2008
        model.run(dataset_pool.get_dataset('employment_event'), job_set, current_year=2008)
        results = self.get_count_all_sectors_and_areas(job_set)
 
        expected_results = array([4100, 100, 1000, 5500, 1500, 1000, 1000, 1000, 900])
        self.assertEqual(ma.allequal(results, expected_results), True)
 
    def test_run_model_with_known_buildings(self):
        storage = self.storage
        storage.write_table(
            table_name = 'buildings',
            table_data = {
                  'building_id':    array([1,2,3,4,5,6,7]),
                  'parcel_id':      array([1,1,2,2,2,3,3]),
                  'is_residential': array([0,0,0,1,1,0,0])
                          }
                            )
        
        storage.write_table(
            table_name = 'employment_events',
            table_data = {
           'parcel_id':                     array([2,       2,    -1,     -1,   1]),
           'building_id':                   array([-1,     -1,     6,      7,  -1]),
           'scheduled_year':                array([2006, 2006,   2006,    2006, 2006]),
           'number_of_non_home_based_jobs': array([3500, 500,    -100,     0,   100]),
           'number_of_home_based_jobs':     array([0,     20,       0,    10,    0]),
           'sector_id':                     array([1,     2,       15,     2,    1]),
           'replace_non_home_based_jobs':   array([0,     0,        0,     1,    0])
                          }
                            )
        
        # change in 2006
        ############   
#        parcel/sector       1              2              3
#            1            +100nhb         +3500nhb        --
#            2            =0nhb           +500nhb/+20hb  +10hb
#            15             --             --           -100nhb
       
        dataset_pool = DatasetPool(storage=storage, package_order=['urbansim_parcel', 'urbansim'])
        job_set = JobDataset(in_storage=storage)
        job_set.modify_attribute('building_id', array(6000*[1] + 4000*[3] + 3000*[6]))
        dataset_pool.add_datasets_if_not_included({'job':job_set})
        model = EmploymentEventsModel(dataset_pool=dataset_pool)

        model.run(dataset_pool.get_dataset('employment_event'), job_set, current_year=2006)
        buildings = dataset_pool.get_dataset('building')
        jobs_in_sec_1 = buildings.compute_variables(['urbansim_parcel.building.number_of_jobs_of_sector_1'],
                                                    dataset_pool=dataset_pool)
        jobs_in_sec_2 = buildings.compute_variables(['urbansim_parcel.building.number_of_jobs_of_sector_2'],
                                                    dataset_pool=dataset_pool)
        jobs_in_sec_15 = buildings.compute_variables(['urbansim_parcel.building.number_of_jobs_of_sector_15'],
                                                    dataset_pool=dataset_pool)

        self.assertEqual(jobs_in_sec_1[0:2].sum()==4100, True) # parcel 1
        self.assertEqual(jobs_in_sec_1[2] == 5500, True) # parcel 2 non-residential
        self.assertEqual(jobs_in_sec_1[5:7].sum()==1000, True) # parcel 3
        self.assertEqual(jobs_in_sec_2[0:2].sum()==1000, True) # parcel 1
        self.assertEqual(jobs_in_sec_2[2] == 1500, True) # parcel 2 non-residential
        self.assertEqual(jobs_in_sec_2[3:5].sum() == 20, True) # parcel 2 residential
        self.assertEqual(jobs_in_sec_2[5]==100, True) # parcel 3, building 6
        self.assertEqual(jobs_in_sec_2[6]==10, True) # parcel 3, building 7
        self.assertEqual(jobs_in_sec_15[0:2].sum()==1000, True) # parcel 2 non-residential
        self.assertEqual(jobs_in_sec_15[2] == 1000, True) # parcel 2 residential
        self.assertEqual(jobs_in_sec_15[5]==900, True) # parcel 3, building 6
        
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
