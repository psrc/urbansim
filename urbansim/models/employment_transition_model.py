# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter, unique
from opus_core.model import Model
from numpy import arange, array, where, zeros, ones, compress, concatenate, resize
from numpy import logical_not, int8, int32
from opus_core.ndimage import sum as ndimage_sum
from opus_core.sampling_toolbox import sample_noreplace, probsample_replace
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import DatasetSubset

class EmploymentTransitionModel(Model):
    """Creates and removes jobs from job_set."""

    model_name = "Employment Transition Model"
    location_id_name_default = "grid_id"
    variable_package_default = "urbansim"

    def __init__(self, location_id_name=None, variable_package=None, dataset_pool=None, debuglevel=0):
        self.debug = DebugPrinter(debuglevel)
        self.location_id_name = self.location_id_name_default
        self.variable_package = self.variable_package_default
        if location_id_name is not None:
            self.location_id_name = location_id_name
        if variable_package is not None:
            self.variable_package = variable_package
        self.dataset_pool = self.create_dataset_pool(dataset_pool, ["urbansim", "opus_core"])

    def run(self, year, job_set, control_totals, job_building_types, data_objects=None, resources=None):
        self._do_initialize_for_run(job_set, job_building_types, data_objects)
        idx = where(control_totals.get_attribute("year")==year)[0]
        self.control_totals_for_this_year = DatasetSubset(control_totals, idx)
        self._do_run_for_this_year(job_set)
        return self._update_job_set(job_set)
        
    def _do_initialize_for_run(self, job_set, job_building_types, data_objects=None):
        self.max_id = job_set.get_id_attribute().max()
        self.job_size = job_set.size()
        self.job_id_name = job_set.get_id_name()[0]
        self.new_jobs = {
            self.location_id_name:array([], dtype=job_set.get_data_type(self.location_id_name, int32)),
            "sector_id":array([], dtype=job_set.get_data_type("sector_id", int32)),
            self.job_id_name:array([], dtype=job_set.get_data_type(self.job_id_name, int32)),
            "building_type":array([], dtype=job_set.get_data_type("building_type", int8))
                    }
        self.remove_jobs = array([], dtype=int32)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.dataset_pool.add_datasets_if_not_included({job_building_types.get_dataset_name():job_building_types})
        self.available_building_types = job_building_types.get_id_attribute()

    def _compute_sector_variables(self, sectors, job_set):
        compute_resources = Resources({"debug":self.debug})
        job_set.compute_variables(
            ["%s.%s.is_in_employment_sector_%s_home_based"
                    % (self.variable_package, job_set.get_dataset_name(), x) for x in sectors] +
            ["%s.%s.is_in_employment_sector_%s_non_home_based"
                    % (self.variable_package, job_set.get_dataset_name(), x) for x in sectors] + ["is_non_home_based_job", "is_home_based_job"],
            dataset_pool = self.dataset_pool,
            resources = compute_resources)
        
    def _do_run_for_this_year(self, job_set):
        building_type = job_set.get_attribute("building_type")
        sectors = unique(self.control_totals_for_this_year.get_attribute("sector_id"))
        self._compute_sector_variables(sectors, job_set)
        for sector in sectors:
            isector = where(self.control_totals_for_this_year.get_attribute("sector_id") == sector)[0]
            total_hb_jobs = self.control_totals_for_this_year.get_attribute("total_home_based_employment")[isector]
            total_nhb_jobs = self.control_totals_for_this_year.get_attribute("total_non_home_based_employment")[isector]
            is_in_sector_hb = job_set.get_attribute("is_in_employment_sector_%s_home_based" % sector)
            is_in_sector_nhb = job_set.get_attribute("is_in_employment_sector_%s_non_home_based" % sector)
            diff_hb = int(total_hb_jobs - is_in_sector_hb.astype(int8).sum())
            diff_nhb = int(total_nhb_jobs - is_in_sector_nhb.astype(int8).sum())
            if diff_hb < 0: # home based jobs to be removed
                w = where(is_in_sector_hb == 1)[0]
                sample_array, non_placed, size_non_placed = \
                    get_array_without_non_placed_agents(job_set, w, -1*diff_hb,
                                                         self.location_id_name)
                self.remove_jobs = concatenate((self.remove_jobs, non_placed,
                                           sample_noreplace(sample_array, max(0,abs(diff_hb)-size_non_placed))))
            if diff_nhb < 0: # non home based jobs to be removed
                w = where(is_in_sector_nhb == 1)[0]
                sample_array, non_placed, size_non_placed = \
                    get_array_without_non_placed_agents(job_set, w, -1*diff_nhb,
                                                         self.location_id_name)
                self.remove_jobs = concatenate((self.remove_jobs, non_placed,
                                           sample_noreplace(sample_array, max(0,abs(diff_nhb)-size_non_placed))))

            if diff_hb > 0: # home based jobs to be created
                self.new_jobs[self.location_id_name] = concatenate((self.new_jobs[self.location_id_name],
                                   zeros((diff_hb,), dtype=self.new_jobs[self.location_id_name].dtype.type)))
                self.new_jobs["sector_id"] = concatenate((self.new_jobs["sector_id"],
                                   (resize(array([sector], dtype=self.new_jobs["sector_id"].dtype.type), diff_hb))))
                if 1 in is_in_sector_hb:
                    building_type_distribution = array(ndimage_sum(is_in_sector_hb,
                                                                    labels=building_type,
                                                                    index=self.available_building_types))
                elif 1 in job_set.get_attribute("is_home_based_job"): # take the building type distribution from the whole region
                    building_type_distribution = array(ndimage_sum(
                                                                job_set.get_attribute("is_home_based_job"),
                                                                labels=building_type,
                                                                index=self.available_building_types))
                else: # there are no home-based jobs in the region, take uniform distribution
                    building_type_distribution = ones(self.available_building_types.size)
                    building_type_distribution = building_type_distribution/building_type_distribution.sum()
                sampled_building_types = probsample_replace(
                    self.available_building_types, diff_hb, building_type_distribution/
                    float(building_type_distribution.sum()))
                self.new_jobs["building_type"] = concatenate((self.new_jobs["building_type"],
                            sampled_building_types.astype(self.new_jobs["building_type"].dtype.type)))
                new_max_id = self.max_id + diff_hb
                self.new_jobs[self.job_id_name] = concatenate((self.new_jobs[self.job_id_name],
                                                     arange(self.max_id+1, new_max_id+1)))
                self.max_id = new_max_id

            if diff_nhb > 0: # non home based jobs to be created
                self.new_jobs[self.location_id_name]=concatenate((self.new_jobs[self.location_id_name],
                                     zeros((diff_nhb,), dtype=self.new_jobs[self.location_id_name].dtype.type)))
                self.new_jobs["sector_id"]=concatenate((self.new_jobs["sector_id"],
                                           (resize(array([sector], dtype=self.new_jobs["sector_id"].dtype.type), diff_nhb))))
                if 1 in is_in_sector_nhb:
                    building_type_distribution = array(ndimage_sum(is_in_sector_nhb,
                                                                    labels=building_type,
                                                                    index=self.available_building_types))
                elif 1 in job_set.get_attribute("is_non_home_based_job"): # take the building type distribution from the whole region
                    building_type_distribution = array(ndimage_sum(
                                                        job_set.get_attribute("is_non_home_based_job"),
                                                        labels=building_type,
                                                        index=self.available_building_types))
                else: # there are no non-home-based jobs in the region, take uniform distribution
                    building_type_distribution = ones(self.available_building_types.size)
                    building_type_distribution = building_type_distribution/building_type_distribution.sum()
                sampled_building_types = probsample_replace(
                    self.available_building_types, diff_nhb, building_type_distribution/
                    float(building_type_distribution.sum()))
                self.new_jobs["building_type"] = concatenate((self.new_jobs["building_type"],
                                        sampled_building_types.astype(self.new_jobs["building_type"].dtype.type)))
                new_max_id = self.max_id+diff_nhb
                self.new_jobs[self.job_id_name]=concatenate((self.new_jobs[self.job_id_name], arange(self.max_id+1, 
                                                                                                     new_max_id+1)))
                self.max_id = new_max_id

    def _update_job_set(self, job_set):
        job_set.remove_elements(self.remove_jobs)
        job_set.add_elements(self.new_jobs, require_all_attributes=False)
        difference = job_set.size()-self.job_size
        self.debug.print_debug("Difference in number of jobs: %s (original %s,"
            " new %s, created %s, deleted %s)"
                % (difference,
                   self.job_size,
                   job_set.size(),
                   self.new_jobs[self.job_id_name].size,
                   self.remove_jobs.size),
            3)
        self.debug.print_debug("Number of unplaced jobs: %s"
            % where(job_set.get_attribute(self.location_id_name) <=0)[0].size,
            3)
        return difference

    def prepare_for_run(self, storage, **kwargs):
        from urbansim.datasets.control_total_dataset import ControlTotalDataset
        control_totals = ControlTotalDataset(in_storage=storage, what="employment")
        sample_control_totals(storage, control_totals, **kwargs)
        return control_totals


def get_array_without_non_placed_agents(dataset, arr, max_value=None, location_id_name="grid_id"):
    """ 'arr' is an index within dataset. The function returns a triple
    (arr_without_nonplaced, arr_nonplaced, nonplaced_size).
    'arr_without_nonplaced' is 'arr' with those elements being removed that don't
    have any location assigned. 'arr_nonplaced' are the elements of 'arr' that were removed
    from arr_without_nonplaced'. 'nonplaced_size' is the size of the second item of the triple.
    """
    if location_id_name in dataset.get_known_attribute_names():
        non_placed = where(dataset.get_attribute_by_index(location_id_name, arr) <= 0)[0]
    else:
        non_placed=array([], dtype='int32')
    size_non_placed = non_placed.size
    if size_non_placed <= 0:
        return (arr, non_placed, 0)
    if (max_value is not None) and (size_non_placed > max_value):
        non_placed = sample_noreplace(non_placed, max_value)
        size_non_placed = non_placed.size
    a = ones((arr.size,))
    a[non_placed] = 0
    return (compress(a, arr), arr[non_placed], size_non_placed)

def sample_control_totals(storage, control_totals, sample_control_totals=False, variance=1, multiplicator=1,
                        base_year=None, flush_control_totals=True):
    if sample_control_totals:
        if flush_control_totals:
            cache_storage=storage
        else:
            cache_storage=None
        control_totals.sample_control_totals(variance, base_year, cache_storage=cache_storage,
                                    multiplicator=multiplicator)


from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.resources import Resources
from numpy import array, logical_and
from numpy import ma
from urbansim.constants import Constants
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
            table_name=job_building_types_table_name,
            table_data={
                "id":array([govc,comc,indc,hbc]),
                "name": array(["governmental", "commercial", "industrial", "home_based"]),
                "home_based": array([0, 0, 0, 1])
                }
            )

        self.job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)

        self.jobs_data = {
             "job_id": arange(13000)+1,
             "grid_id": array(6000*[1] + 4000*[2] + 3000*[3]),
             "sector_id": array(4000*[1] + 1000*[2] + 1000*[15] + 2000*[1] + 1000*[2] + 1000*[15] +
                            1000*[1] + 1000*[2] + 1000*[15], dtype=int32),
             "building_type": array(2000*[indc]+2000*[comc] + 300*[indc] + 600*[comc] + 100*[govc] + 1000*[indc] +
                                   1000*[indc]+1000*[comc] + 300*[indc] + 600*[comc] + 100*[govc] + 1000*[indc] +
                                   500*[indc]+500*[comc] + 300*[indc] + 600*[comc] + 100*[govc] + 1000*[indc], dtype=int8)
             }
        self.annual_employment_control_totals_data = {
            "sector_id": array([1,2]),
            "year": array([2000,2000]),
            "total_home_based_employment": array([0,0]),
            "total_non_home_based_employment" : array([5250,3000])
            }

    def test_same_distribution_after_job_subtraction(self):
        """Removes 1,750 sector_1 jobs, without specifying the distribution across gridcells (so it is assumed equal)
        Test that the distribution (in %) of sector 1 jobs across gridcells before and after the subtraction are
        relatively equal.
        """
        storage = StorageFactory().get_storage('dict_storage')

        jobs_set_table_name = 'jobs_set'
        storage.write_table(table_name=jobs_set_table_name, table_data=self.jobs_data)
        jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(table_name=ect_set_table_name, table_data=self.annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name, what="employment")

        # unplace some jobs
        jobs_set.modify_attribute(name="grid_id", data=zeros(int(jobs_set.size()/2)), index=arange(int(jobs_set.size()/2)))
        #run model with input Datasets

        model = EmploymentTransitionModel()
        model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)
        results = jobs_set.size()
        should_be = [11250]
        self.assertEqual(ma.allequal(should_be, results), True, "Error")

        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            jobs_set_table_name = 'jobs_set'
            storage.write_table(
                table_name=jobs_set_table_name,
                table_data=self.jobs_data,
                )

            jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

            model = EmploymentTransitionModel()
            model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)
            # check that the distribution of jobs is the same before and after subtracting jobs
            results = self.get_count_all_sectors_and_gridcells(jobs_set)
            return results

        expected_results = array([4000.0/7000.0*5250.0, 1000, 1000, 2000.0/7000.0*5250.0, 1000,
                                  1000, 1000.0/7000.0*5250.0, 1000, 1000])

        self.run_stochastic_test(__file__, run_model, expected_results, 10)

        def run_model2():
            storage = StorageFactory().get_storage('dict_storage')

            jobs_set_table_name = 'jobs_set'
            storage.write_table(
                table_name=jobs_set_table_name,
                table_data=self.jobs_data,
                )

            jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

            model = EmploymentTransitionModel()
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
            table_name=jobs_set_table_name,
            table_data=self.jobs_data,
            )
        jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

        annual_employment_control_totals_data = self.annual_employment_control_totals_data
        annual_employment_control_totals_data["total_non_home_based_employment"] = array([8750, 3000])

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name=ect_set_table_name,
            table_data=annual_employment_control_totals_data,
            )
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name, what="employment")

        # run model
        model = EmploymentTransitionModel()
        model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)

        #check that there are indeed 14750 total jobs after running the model
        results = jobs_set.size()
        should_be = [14750]
        self.assertEqual(ma.allequal(should_be, results), True, "Error")

        #check that total #jobs within each sector are close to what was set in the control_totals
        results = self.get_count_all_sectors(jobs_set)
        should_be = [8750.0, 3000, 3000]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

        #check that the number of unplaced jobs is the number of new jobs created (1750)
        results = where(jobs_set.get_attribute("grid_id")<=0)[0].size
        should_be = [1750.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

        # test distribution of building type
        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            jobs_set_table_name = 'jobs_set'
            storage.write_table(
                table_name=jobs_set_table_name,
                table_data=self.jobs_data
                )
            jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

            model = EmploymentTransitionModel()
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
        expected_results = array([3500.0/7000.0*8750.0, 900, 3500.0/7000.0*8750.0, 1800, 0, 300])
        #print expected_results
        self.run_stochastic_test(__file__, run_model, expected_results, 10)

        # check data types
        self.assertEqual(jobs_set.get_attribute("sector_id").dtype, int32,
             "Error in data type of the new job set. Should be: int32, is: %s" % str(jobs_set.get_attribute("sector_id").dtype))
        self.assertEqual(jobs_set.get_attribute("building_type").dtype, int8,
             "Error in data type of the new job set. Should be: int8, is: %s" % str(jobs_set.get_attribute("building_type").dtype))

    def test_unplaced_jobs_after_job_addition(self):
        """The initial jobs table is now adjusted to include 2000 unplaced jobs.
        Add 1,750 new jobs and ensure that the number of unplaced jobs after the addition
        is exactly 3,750 because this model is not responsible for placing jobs, only for creating them.
        """
        # create and populate jobs table for model input
        add_jobs_data = {
            "job_id": arange(13001, 15001),
            "grid_id": array(2000*[0]),
            "sector_id": array(2000*[1]),
            "building_type": array(2000*[Constants._industrial_code])
            }
        annual_employment_control_totals_data = self.annual_employment_control_totals_data
        annual_employment_control_totals_data["total_non_home_based_employment"] = array([10750, 3000])

        storage = StorageFactory().get_storage('dict_storage')

        jobs_set_table_name = 'jobs_set'
        storage.write_table(
            table_name=jobs_set_table_name,
            table_data=self.jobs_data
            )
        jobs_set = JobDataset(in_storage=storage, in_table_name=jobs_set_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name=ect_set_table_name,
            table_data=annual_employment_control_totals_data,
            )
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name, what="employment")

        jobs_set.add_elements(add_jobs_data)

        # run model with input databases
        model = EmploymentTransitionModel()
        model.run(year=2000, job_set=jobs_set, control_totals=ect_set, job_building_types=self.job_building_types)

        #check that there are indeed 16750 total jobs after running the model
        results = jobs_set.size()
        should_be = [16750]
        self.assertEqual(ma.allequal(should_be, results), True, "Error")

        #check that the number of unplaced jobs is the number of new jobs created + number of unplaced jobs before running model
        results = where(jobs_set.get_attribute("grid_id")<=0)[0].size
        should_be = [3750.0]

        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

    def get_count_all_sectors_and_gridcells(self, job_set):
        res = zeros(len(self.possible_grid_ids) * len(self.possible_sector_ids))
        i=0
        for grid_id in self.possible_grid_ids:
            tmp = where(job_set.get_attribute("grid_id") == grid_id, 1,0)
            for sector_id in self.possible_sector_ids:
                res[i] = logical_and(where(job_set.get_attribute("sector_id") == sector_id, 1,0), tmp).sum()
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
