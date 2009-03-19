# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.misc import unique_values
from numpy import arange, array, where, logical_and, concatenate
from numpy import zeros, ones, compress, resize
from numpy import logical_not, int8, int32
from opus_core.datasets.dataset import DatasetSubset
from opus_core.logger import logger
from opus_core.variables.attribute_type import AttributeType
from urbansim.models.employment_transition_model import EmploymentTransitionModel

class SubareaEmploymentTransitionModel(EmploymentTransitionModel):
    """Creates and removes jobs from job_set. It runs the urbansim ETM with control totals for each region."""

    model_name = "Subarea Employment Transition Model"
    
    def __init__(self, subarea_id_name, **kwargs):
        super(SubareaEmploymentTransitionModel, self).__init__(**kwargs)
        self.subarea_id_name = subarea_id_name

    def run(self, year, job_set, control_totals, job_building_types, data_objects=None, resources=None):
        self._do_initialize_for_run(job_set, job_building_types, data_objects)
        subarea_ids = control_totals.get_attribute(self.subarea_id_name)
        jobs_subarea_ids = job_set.compute_variables("urbansim_parcel.job.%s" % self.subarea_id_name)
        unique_subareas = unique_values(subarea_ids)
        is_year = control_totals.get_attribute("year")==year
        all_jobs_index = arange(job_set.size())
        sectors = unique_values(control_totals.get_attribute("sector_id")[is_year])
        self._compute_sector_variables(sectors, job_set)
        for area in unique_subareas:
            idx = where(logical_and(is_year, subarea_ids == area))[0]
            self.control_totals_for_this_year = DatasetSubset(control_totals, idx)
            jobs_index = where(jobs_subarea_ids == area)[0]
            jobs_for_this_area = DatasetSubset(job_set, jobs_index)
            logger.log_status("ETM for area %s (currently %s jobs)" % (area, jobs_for_this_area.size()))
            last_remove_idx = self.remove_jobs.size
            self._do_run_for_this_year(jobs_for_this_area)
            add_jobs_size = self.new_jobs[self.location_id_name].size-self.new_jobs[self.subarea_id_name].size
            remove_jobs_size = self.remove_jobs.size-last_remove_idx
            logger.log_status("add %s, remove %s, total %s" % (add_jobs_size, remove_jobs_size,
                                                               jobs_for_this_area.size()+add_jobs_size-remove_jobs_size))
            self.new_jobs[self.subarea_id_name] = concatenate((self.new_jobs[self.subarea_id_name],
                    array(add_jobs_size*[area], dtype="int32")))
            # transform indices of removing jobs into indices of the whole dataset
            self.remove_jobs[last_remove_idx:self.remove_jobs.size] = all_jobs_index[jobs_index[self.remove_jobs[last_remove_idx:self.remove_jobs.size]]]
        self._update_job_set(job_set)
        idx_new_jobs = arange(job_set.size()-self.new_jobs[self.subarea_id_name].size, job_set.size())
        jobs_subarea_ids = job_set.compute_variables("urbansim_parcel.job.%s" % self.subarea_id_name)
        jobs_subarea_ids[idx_new_jobs] = self.new_jobs[self.subarea_id_name]
        job_set.delete_one_attribute(self.subarea_id_name)
        job_set.add_attribute(jobs_subarea_ids, self.subarea_id_name, metadata=AttributeType.PRIMARY)
        # return an index of new jobs
        return arange(job_set.size()-self.new_jobs[self.subarea_id_name].size, job_set.size())  
        
    def _do_initialize_for_run(self, job_set, job_building_types, data_objects):
        EmploymentTransitionModel._do_initialize_for_run(self, job_set, job_building_types, data_objects)
        self.new_jobs[self.subarea_id_name] = array([], dtype="int32")
        
from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.resources import Resources
from numpy import array, logical_and, int32, int8, zeros
from numpy import ma
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from opus_core.storage_factory import StorageFactory


class Tests(StochasticTestCase):
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

        self.job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)

        self.jobs_data = {
             "job_id": arange(13000)+1,
             "grid_id": array(6000*[1] + 4000*[2] + 3000*[3]),
             "faz_id": array(6000*[1] + 7000*[2]),
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
        self.annual_employment_control_totals_data = {
            "sector_id": array([1,2, 1, 2]),
            "year": array([2000,2000, 2000, 2000]),
            "total_home_based_employment": array([0,0, 0, 0]),
            "total_non_home_based_employment" : array([2250, 1000, 3000, 2000]),
            "faz_id": array([1,1,2,2])
            }

    def test_same_distribution_after_job_subtraction(self):
        """Removes 1,750 sector_1 jobs, without specifying the distribution across gridcells (so it is assumed equal)
        Test that the distribution (in %) of sector 1 jobs across gridcells before and after the subtraction are
        relatively equal.
        """
        storage = StorageFactory().get_storage('dict_storage')

        jobs_set_table_name = 'jobs_set'
        storage.write_table(table_name = jobs_set_table_name, table_data = self.jobs_data)
        jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(table_name = ect_set_table_name, table_data = self.annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name, what="employment")

        model = SubareaEmploymentTransitionModel("faz_id")
        model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)
        
        # check the totals in regions
        areas = jobs_set.get_attribute("faz_id")
        results = array([0,0])
        for iarea in [0,1]:
            results[iarea] = where(areas == [1,2][iarea])[0].size
        should_be = [4250, 7000]
        self.assertEqual(ma.allequal(should_be, results), True, "Error, should_be: %s, but result: %s" % (should_be, results))

        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            jobs_set_table_name = 'jobs_set'
            storage.write_table(
                table_name = jobs_set_table_name,
                table_data = self.jobs_data,
                )

            jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

            model = SubareaEmploymentTransitionModel("faz_id")
            model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)
            # check that the distribution of jobs is the same before and after subtracting jobs
            results = self.get_count_all_sectors_and_areas(jobs_set)
            return results

        expected_results = array([2250.0, 1000, 1000, 3000, 2000.0, 2000])

        self.run_stochastic_test(__file__, run_model, expected_results, 10)

        def run_model2():
            storage = StorageFactory().get_storage('dict_storage')

            jobs_set_table_name = 'jobs_set'
            storage.write_table(
                table_name = jobs_set_table_name,
                table_data = self.jobs_data,
                )

            jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

            model = SubareaEmploymentTransitionModel("faz_id")
            model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)
            # check that the distribution of building type is the same before and after subtracting jobs
            jobs_set.compute_variables(["urbansim.job.is_in_employment_sector_1_industrial",
                                        "urbansim.job.is_in_employment_sector_2_industrial",
                                        "urbansim.job.is_in_employment_sector_1_commercial",
                                        "urbansim.job.is_in_employment_sector_2_commercial",
                                        "urbansim.job.is_in_employment_sector_1_governmental",
                                        "urbansim.job.is_in_employment_sector_2_governmental"],
                                        resources = Resources({"job_building_type":self.job_building_types}))
            result = array([jobs_set.get_attribute("is_in_employment_sector_1_industrial").sum(),
                            jobs_set.get_attribute("is_in_employment_sector_2_industrial").sum(),
                            jobs_set.get_attribute("is_in_employment_sector_1_commercial").sum(),
                            jobs_set.get_attribute("is_in_employment_sector_2_commercial").sum(),
                            jobs_set.get_attribute("is_in_employment_sector_1_governmental").sum(),
                            jobs_set.get_attribute("is_in_employment_sector_2_governmental").sum()
                            ])
            return result
        expected_results = array([3500.0/7000.0*5250.0, 900, 3500.0/7000.0*5250.0, 1800, 0, 300])
        self.run_stochastic_test(__file__, run_model2, expected_results, 20)

    def test_same_distribution_after_job_addition(self):
        """Add 1,750 new jobs of sector 1 without specifying a distribution across gridcells (so it is assumed equal)
        Test that the total number of jobs in each sector after the addition matches the totals specified
        in annual_employment_control_totals.
        Ensure that the number of unplaced jobs after the addition is exactly 1,750 because this model
        is not responsible for placing jobs, only for creating them.
        NOTE: unplaced jobs are indicated by grid_id <= 0
        """
        storage = StorageFactory().get_storage('dict_storage')

        jobs_set_table_name = 'jobs_set'
        storage.write_table(
            table_name = jobs_set_table_name,
            table_data = self.jobs_data,
            )
        jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

        annual_employment_control_totals_data = self.annual_employment_control_totals_data
        annual_employment_control_totals_data["total_non_home_based_employment"] = array([5750, 1400, 4000, 1600])

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name = ect_set_table_name,
            table_data = annual_employment_control_totals_data,
            )
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name, what="employment")

        # run model
        model = SubareaEmploymentTransitionModel("faz_id")
        model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)

        #check that there are indeed 14750 total jobs after running the model
        areas = jobs_set.get_attribute("faz_id")
        results = array([0,0])
        for iarea in [0,1]:
            results[iarea] = where(areas == [1,2][iarea])[0].size
        should_be = [8150, 7600]
        self.assertEqual(ma.allequal(should_be, results), True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that total #jobs within each sector are close to what was set in the control_totals
        results = self.get_count_all_sectors_and_areas(jobs_set)
        should_be = [5750, 1400, 1000, 4000, 1600, 2000]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True,
                         "Error, should_be: %s, but result: %s" % (should_be, results))


    def get_count_all_sectors_and_areas(self, job_set):
        res = zeros(2 * len(self.possible_sector_ids))
        i=0
        for area in [1, 2]:
            tmp = job_set.get_attribute("faz_id") == area
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
