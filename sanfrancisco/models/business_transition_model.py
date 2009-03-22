# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.misc import DebugPrinter, unique_values
from opus_core.model import Model
from numpy import arange, array, where, int8, zeros, ones, compress, int32, concatenate
from numpy import logical_not, cumsum
from numpy.random import permutation
from opus_core.sampling_toolbox import sample_noreplace, probsample_replace
from opus_core.logger import logger

class BusinessTransitionModel(Model):
    """Creates and removes businesses from business_set."""
    
    model_name = "Business Transition Model"
    location_id_name = "building_id"
    variable_package = "sanfrancisco"
    
    def __init__(self, debuglevel=0):
        self.debug = DebugPrinter(debuglevel)
        
    def run(self, year, business_set, 
            control_totals, 
            dataset_pool=None, 
            resources=None):
        self.business_id_name = business_set.get_id_name()[0]
        control_for_businesses = False # If this is False, it is controlled for jobs
        if "total_number_of_businesses" in control_totals.get_known_attribute_names():
            control_for_businesses = True
            control_totals.get_attribute("total_number_of_businesses")
        else:
            control_totals.get_attribute("total_number_of_jobs")
        idx = where(control_totals.get_attribute("year")==year)
        sectors = unique_values(control_totals.get_attribute_by_index("sector_id", idx))
        self.max_id = business_set.get_id_attribute().max()
        business_size = business_set.size()
        self.new_businesses = {self.location_id_name:array([], dtype='int32'), 
                          "sector_id":array([], dtype='int32'),
                          self.business_id_name:array([], dtype='int32'), 
                          "sqft":array([], dtype=int32),
                          "employment":array([], dtype=int32),}

        business_set.compute_variables(
            map(lambda x: "%s.%s.is_of_sector_%s" 
                    % (self.variable_package, business_set.get_dataset_name(), x), sectors), 
                dataset_pool=dataset_pool, resources = resources)
        self.remove_businesses = array([], dtype='int32')
            
        for sector in sectors:
            b_is_in_sector = business_set.get_attribute("is_of_sector_%s" % sector)
            if control_for_businesses:
                total_businesses = control_totals.get_data_element_by_id((year,sector)).total_number_of_businesses
                diff = int(total_businesses - b_is_in_sector.astype(int8).sum())
                self._do_sector_for_businesses(sector, diff, business_set, b_is_in_sector)
            else:
                total_jobs = control_totals.get_data_element_by_id((year,sector)).total_number_of_jobs
                diff = int(total_jobs - business_set.get_attribute_by_index("employment", b_is_in_sector).sum())
                self._do_sector_for_jobs(sector, diff, business_set, b_is_in_sector)
             
        business_set.remove_elements(self.remove_businesses)
        business_set.add_elements(self.new_businesses, require_all_attributes=False)
        difference = business_set.size()-business_size
        self.debug.print_debug("Difference in number of businesses: %s (original %s,"
            " new %s, created %s, deleted %s)" 
                % (difference, 
                   business_size, 
                   business_set.size(), 
                   self.new_businesses[self.business_id_name].size, 
                   self.remove_businesses.size), 
            3)
        self.debug.print_debug("Number of unplaced businesses: %s" 
            % where(business_set.get_attribute(self.location_id_name) <=0)[0].size, 
            3)
        return difference
    
    def _do_sector_for_businesses(self, sector, diff, business_set, is_in_sector):
        available_business_index = where(is_in_sector)[0]
        if diff < 0: #
            sample_array, non_placed, size_non_placed = \
                get_array_without_non_placed_agents(business_set, available_business_index, -1*diff, 
                                                     self.location_id_name)
            self.remove_businesses = concatenate((self.remove_businesses, non_placed, 
                                       sample_noreplace(sample_array, max(0,abs(diff)-size_non_placed))))
                            
        if diff > 0: #
            self.new_businesses[self.location_id_name]=concatenate((self.new_businesses[self.location_id_name],zeros((diff,))))
            self.new_businesses["sector_id"]=concatenate((self.new_businesses["sector_id"], sector*ones((diff,))))
            sampled_business = probsample_replace(available_business_index, diff, None)
            self.new_businesses["sqft"] = concatenate((self.new_businesses["sqft"],
                                                 business_set.get_attribute("sqft")[sampled_business]))
            self.new_businesses["employment"] = concatenate((self.new_businesses["employment"],
                                                       business_set.get_attribute("employment")[sampled_business]))
            
            new_max_id = self.max_id+diff
            self.new_businesses[self.business_id_name]=concatenate((self.new_businesses[self.business_id_name], 
                                                                    arange(self.max_id+1, new_max_id+1)))
            self.max_id = new_max_id
                
    def _do_sector_for_jobs(self, sector, diff, business_set, b_is_in_sector):
        # diff is a difference in jobs (not businesses)
        employment = business_set.get_attribute('employment')
        available_business_index = where(b_is_in_sector)[0]
        if diff < 0: #
            placed, non_placed, size_non_placed = \
                get_array_without_non_placed_agents(business_set, available_business_index, -1*available_business_index.size, 
                                                     self.location_id_name)
            consider_for_removing = concatenate((permutation(non_placed), permutation(placed)))
            empl_cumsum = cumsum(employment[consider_for_removing])
            remove_b = consider_for_removing[empl_cumsum <= abs(diff)]
            self.remove_businesses = concatenate((self.remove_businesses, remove_b))
                            
        if diff > 0: #
            total_empl_added = 0
            sampled_business = array([], dtype=int32)
            while total_empl_added < diff:
                consider_for_duplicating = permutation(available_business_index)
                empl_cumsum = cumsum(employment[consider_for_duplicating])
                sampled_business = concatenate((sampled_business, consider_for_duplicating[empl_cumsum+total_empl_added <= diff]))
                if empl_cumsum[-1]+total_empl_added > diff:
                    break
                total_empl_added += employment[sampled_business].sum()

            self.new_businesses[self.location_id_name]=concatenate((self.new_businesses[self.location_id_name],zeros((sampled_business.size,))))
            self.new_businesses["sector_id"]=concatenate((self.new_businesses["sector_id"], sector*ones((sampled_business.size,))))
            self.new_businesses["sqft"] = concatenate((self.new_businesses["sqft"],
                                                 business_set.get_attribute("sqft")[sampled_business]))
            self.new_businesses["employment"] = concatenate((self.new_businesses["employment"],
                                                       employment[sampled_business]))
            
            new_max_id = self.max_id+sampled_business.size
            self.new_businesses[self.business_id_name]=concatenate((self.new_businesses[self.business_id_name], 
                                                                    arange(self.max_id+1, new_max_id+1)))
            self.max_id = new_max_id
            
    def prepare_for_run(self, storage, in_table_name, id_name, **kwargs):
        from urbansim.datasets.control_total_dataset import ControlTotalDataset
        control_totals = ControlTotalDataset(in_storage=storage, 
                                             in_table_name=in_table_name,
                                             id_name=id_name
                                         )
        return control_totals
    
    
def get_array_without_non_placed_agents(business_set, arr, max_value=None, location_id_name="building_id"):
    if location_id_name in business_set.get_known_attribute_names():
        non_placed = where(business_set.get_attribute_by_index(location_id_name, arr) <= 0)[0]
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
            

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from numpy import array, logical_and
from numpy import ma
from sanfrancisco.datasets.business_dataset import BusinessDataset
from urbansim.datasets.employment_control_total_dataset import EmploymentControlTotalDataset
from opus_core.storage_factory import StorageFactory


class Tests(StochasticTestCase):
    def setUp(self):
        self.possible_building_ids = [1,2,3]
        self.possible_sector_ids = [1,2,15]
        storage = StorageFactory().get_storage('dict_storage')

        self.business_data = {
             "business_id": arange(13000)+1,
             "building_id": array(6000*[1] + 4000*[2] + 3000*[3]),
             "sector_id": array(4000*[1] + 1000*[2] + 1000*[15] + 2000*[1] + 1000*[2] + 1000*[15] +
                            1000*[1] + 1000*[2] + 1000*[15], dtype=int32),
            "sqft": array(13000*[10]),
            "employment": array(4000*[10] + 1000*[20] + 1000*[150] + 2000*[1] + 1000*[2] + 1000*[15] +
                            1000*[100] + 1000*[200] + 1000*[30])
                              }
                    # sector 1:  4000*10 + 2000 + 1000*100 =    142000 jobs
                    # sector 2:  1000*20 + 1000*2 + 1000*200 =  222000
                    # sector 15: 1000*150 + 1000*15 + 1000*30 = 195000
        self.annual_business_control_totals_data = {
            "sector_id": array([1,2,15]),
            "year": array([2000,2000,2000]),
            "total_number_of_businesses" : array([5250,3000,2500])
            }
        
        self.annual_job_control_totals_data = {
            "sector_id": array([1,2,15]),
            "year": array([2000,2000,2000]),
            "total_number_of_jobs" : array([140000,222000,180000])
            }

    def test_same_distribution_after_business_subtraction_control_for_business(self):
        """Removes 1,750 sector_1 businesses and 500 sector 15 businesses.
        Test that the distribution (in %) of sector 1 businesses and sector 15 businesses across buildings before and after the subtraction are
        relatively equal.
        """
        storage = StorageFactory().get_storage('dict_storage')

        business_table_name = 'business_set'
        storage.write_table(table_name=business_table_name, table_data=self.business_data)
        business_set = BusinessDataset(in_storage=storage, in_table_name=business_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(table_name=ect_set_table_name, table_data=self.annual_business_control_totals_data)
        ect_set = EmploymentControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name)

        # unplace half of the  businesses
        business_set.modify_attribute(name="building_id", data=zeros(int(business_set.size()/2)), index=arange(int(business_set.size()/2)))
        #run model 
        model = BusinessTransitionModel()
        model.run(year=2000, business_set=business_set, control_totals=ect_set)
        results = business_set.size()
        should_be = [10750]
        self.assertEqual(ma.allequal(should_be, results), True, "Error in total number of businesses.")

        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            business_set_table_name = 'business_set'
            storage.write_table(
                table_name=business_set_table_name,
                table_data=self.business_data,
                )

            business_set = BusinessDataset(in_storage=storage, in_table_name=business_set_table_name)

            model = BusinessTransitionModel()
            model.run(year=2000, business_set=business_set, control_totals=ect_set)
            # check that the distribution of businesses is the same before and after subtracting businesses
            results = self.get_count_all_sectors_and_buildings(business_set)
            return results

        expected_results = array([4000.0/7000.0*5250.0, 1000, 1000.0/3000.0*2500, 2000.0/7000.0*5250.0, 1000,
                                  1000/3000.0*2500, 1000.0/7000.0*5250.0, 1000, 1000/3000.0*2500])

        self.run_stochastic_test(__file__, run_model, expected_results, 10)

    def test_same_distribution_after_business_subtraction_control_for_jobs(self):
        """Removes sector_1 and sector 15 businesses while controlling for total number of jobs.
        Test that the distribution (in %) of sector 1 and sector 15 employment across buildings before and after the subtraction are
        relatively equal.
        """
        storage = StorageFactory().get_storage('dict_storage')

        business_table_name = 'business_set'
        storage.write_table(table_name=business_table_name, table_data=self.business_data)
        business_set = BusinessDataset(in_storage=storage, in_table_name=business_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(table_name=ect_set_table_name, table_data=self.annual_job_control_totals_data)
        ect_set = EmploymentControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name)

        #run model 
        model = BusinessTransitionModel()
        model.run(year=2000, business_set=business_set, control_totals=ect_set)
        #Check the overall employment
        results = [business_set.get_attribute('employment').sum()]
        should_be = [542000] # 140000+222000+180000 = 542000
        self.assertEqual(results[0] >= should_be[0], True, 
                         "Error in total number of jobs. Should be >= %s, is %s " % (should_be[0], results[0]))
        #The difference should be not larger than the sum of maximum business employment over sectors (-> 100 + 200 + 150) 
        self.assertEqual(ma.allclose(should_be, results, atol=450), True, 
                         "Error in total number of jobs. Should be %s (up to 450), is %s " % (should_be[0], results[0]))

        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            business_set_table_name = 'business_set'
            storage.write_table(
                table_name=business_set_table_name,
                table_data=self.business_data,
                )

            business_set = BusinessDataset(in_storage=storage, in_table_name=business_set_table_name)

            model = BusinessTransitionModel()
            model.run(year=2000, business_set=business_set, control_totals=ect_set)
            # check that the distribution of businesses is the same before and after subtracting businesses
            results = self.get_job_count_all_sectors_and_buildings(business_set)
            return results
        expected_results = array([4000.0*10/142000.0*140000, 1000*20, 1000.0*150/195000.0*180000, 2000.0/142000.0*140000, 1000*2,
                                  1000*15/195000.0*180000, 1000.0*100/142000.0*140000, 1000*200, 1000*30/195000.0*180000])


        self.run_stochastic_test(__file__, run_model, expected_results, 10)


    def test_same_distribution_after_business_addition_control_for_business(self):
        """Add 1,750 new businesses of sector 1 and 1000 businesses of sector 2.
        Test that the total number of businesses in each sector after the addition matches the totals specified
        in annual_business_control_totals.
        Ensure that the number of unplaced businesses after the addition is exactly 2,750 because this model
        is not responsible for placing jobs, only for creating them.
        NOTE: unplaced businesses are indicated by building_id <= 0
        """
        storage = StorageFactory().get_storage('dict_storage')

        business_set_table_name = 'business_set'
        storage.write_table(
            table_name=business_set_table_name,
            table_data=self.business_data,
            )
        business_set = BusinessDataset(in_storage=storage, in_table_name=business_set_table_name)

        annual_employment_control_totals_data = self.annual_business_control_totals_data
        annual_employment_control_totals_data["total_number_of_businesses"] = array([8750, 4000, 3000])

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name=ect_set_table_name,
            table_data=annual_employment_control_totals_data,
            )
        ect_set = EmploymentControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name)

        # run model
        model = BusinessTransitionModel()
        model.run(year=2000, business_set=business_set, control_totals=ect_set)

        #check the total
        results = business_set.size()
        should_be = [15750]
        self.assertEqual(ma.allequal(should_be, results), True, "Error in total number of businesses.")

        #check that total #businesses within each sector are close to what was set in the control_totals
        results = self.get_count_all_sectors(business_set)
        should_be = [8750.0, 4000, 3000]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

        #check that the number of unplaced businesses is the number of new businesses created (2750)
        results = where(business_set.get_attribute("building_id")<=0)[0].size
        should_be = [2750.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

    def test_same_distribution_after_business_addition_and_subtraction_control_for_jobs(self):
        """Add new businesses of sector 1 and sector 2. Subtract all businesses of sector 15. The model
        is adding and subtracting businesses while controlling for total number of jobs.
        Test that the total number of jobs in each sector after the modification matches the totals specified
        in annual_jobs_control_totals.
        """
        storage = StorageFactory().get_storage('dict_storage')

        business_set_table_name = 'business_set'
        storage.write_table(
            table_name=business_set_table_name,
            table_data=self.business_data,
            )
        business_set = BusinessDataset(in_storage=storage, in_table_name=business_set_table_name)

        annual_employment_control_totals_data = self.annual_job_control_totals_data
        annual_employment_control_totals_data["total_number_of_jobs"] = array([150000,500000, 0])

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name=ect_set_table_name,
            table_data=annual_employment_control_totals_data,
            )
        ect_set = EmploymentControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name)

        # run model
        model = BusinessTransitionModel()
        model.run(year=2000, business_set=business_set, control_totals=ect_set)

        #check the total
        results = [business_set.get_attribute('employment').sum()]
        should_be = [650000]
        
        self.assertEqual(ma.allclose(should_be, results, atol=450), True, 
                         "Error in total number of jobs. Should be about %s, is %s." % (should_be[0],results[0]))

        #check that total # jobs within each sector are close to what was set in the control_totals
        results = self.get_job_count_all_sectors(business_set)
        should_be = [150000, 500000, 0]
        self.assertEqual(ma.allclose(results, should_be, atol=200), True)



    def test_unplaced_jobs_after_job_addition_control_for_business(self):
        """The initial business table is now adjusted to include 2000 unplaced businesses.
        Add 1,750 new businesses and ensure that the number of unplaced businesses after the addition
        is exactly 3,750 because this model is not responsible for placing jobs, only for creating them.
        """
        # create and populate jobs table for model input
        add_business_data = {
            "business_id": arange(13001, 15001),
            "building_id": array(2000*[0]),
            "sector_id": array(2000*[1]),
            "sqft": array(2000*[10]),
            "employment": array(2000*[100])
            }
        annual_employment_control_totals_data = self.annual_business_control_totals_data
        annual_employment_control_totals_data["total_number_of_businesses"] = array([10750, 3000, 3000])

        storage = StorageFactory().get_storage('dict_storage')

        business_set_table_name = 'business_set'
        storage.write_table(
            table_name=business_set_table_name,
            table_data=self.business_data
            )
        business_set = BusinessDataset(in_storage=storage, in_table_name=business_set_table_name)

        ect_set_table_name = 'ect_set'
        storage.write_table(
            table_name=ect_set_table_name,
            table_data=annual_employment_control_totals_data,
            )
        ect_set = EmploymentControlTotalDataset(in_storage=storage, in_table_name=ect_set_table_name)

        business_set.add_elements(add_business_data)

        # run model with input databases
        model = BusinessTransitionModel()
        model.run(year=2000, business_set=business_set, control_totals=ect_set)

        #check that there are indeed 16750 total businesses after running the model
        results = business_set.size()
        should_be = [16750]
        self.assertEqual(ma.allequal(should_be, results), True, "Error")

        #check that the number of unplaced businesses is the number of new businesses created + number of unplaced business before running model
        results = where(business_set.get_attribute("building_id")<=0)[0].size
        should_be = [3750.0]

        self.assertEqual(ma.allclose(results, should_be, rtol=0.00001), True)

    def get_count_all_sectors_and_buildings(self, business_set):
        res = zeros(len(self.possible_building_ids) * len(self.possible_sector_ids))
        i=0
        for building_id in self.possible_building_ids:
            tmp = where(business_set.get_attribute("building_id") == building_id, 1,0)
            for sector_id in self.possible_sector_ids:
                res[i] = logical_and(where(business_set.get_attribute("sector_id") == sector_id, 1,0), tmp).sum()
                i+=1
        return res
    
    def get_job_count_all_sectors_and_buildings(self, business_set):
        res = zeros(len(self.possible_building_ids) * len(self.possible_sector_ids))
        i=0
        for building_id in self.possible_building_ids:
            tmp = where(business_set.get_attribute("building_id") == building_id, 1,0)
            for sector_id in self.possible_sector_ids:
                res[i] = business_set.get_attribute('employment')[logical_and(where(business_set.get_attribute("sector_id") == sector_id, 1,0), tmp)].sum()
                i+=1
        return res

    def get_count_all_sectors(self, business_set):
        res = zeros(len(self.possible_sector_ids))
        i=0
        for sector_id in self.possible_sector_ids:
            res[i] = where(business_set.get_attribute("sector_id") == sector_id)[0].size
            i+=1
        return res
    
    def get_job_count_all_sectors(self, business_set):
        res = zeros(len(self.possible_sector_ids))
        i=0
        for sector_id in self.possible_sector_ids:
            res[i] = business_set.get_attribute('employment')[where(business_set.get_attribute("sector_id") == sector_id)].sum()
            i+=1
        return res

if __name__=='__main__':
    opus_unittest.main()
 