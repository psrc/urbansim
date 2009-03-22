# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from numpy import arange, array, where, logical_and, concatenate
from opus_core.misc import get_distinct_names, unique_values
from opus_core.datasets.dataset import DatasetSubset
from opus_core.variables.attribute_type import AttributeType
from opus_core.logger import logger
from urbansim.models.household_transition_model import HouseholdTransitionModel
from copy import copy

class RegionalHouseholdTransitionModel(HouseholdTransitionModel):
    """Creates and removes households from household_set. It runs the urbansim HTM with control totals for each region."""

    model_name = "Regional Household Transition Model"

    def run(self, year, household_set, control_totals, characteristics, resources=None):
        self._do_initialize_for_run(household_set)
        control_totals.get_attribute("total_number_of_households") # to make sure they are loaded
        self.characteristics = characteristics
        self.all_categories = self.characteristics.get_attribute("characteristic")
        self.all_categories = array(map(lambda x: x.lower(), self.all_categories))
        self.scaled_characteristic_names = get_distinct_names(self.all_categories).tolist()
        self.marginal_characteristic_names = copy(control_totals.get_id_name())
        index_year = self.marginal_characteristic_names.index("year")
        self.marginal_characteristic_names.remove("year")
        self.marginal_characteristic_names.remove("large_area_id")
        large_area_ids = control_totals.get_attribute("large_area_id")
        households_large_area_ids = household_set.compute_variables("washtenaw.household.large_area_id")
        unique_large_areas = unique_values(large_area_ids)
        is_year = control_totals.get_attribute("year")==year
        all_households_index = arange(household_set.size())
        for area in unique_large_areas:
            idx = where(logical_and(is_year, large_area_ids == area))[0]
            self.control_totals_for_this_year = DatasetSubset(control_totals, idx)
            households_index = where(households_large_area_ids == area)[0]
            households_for_this_area = DatasetSubset(household_set, households_index)
            logger.log_status("HTM for area %s (currently %s households)" % (area, households_for_this_area.size()))
            last_remove_idx = self.remove_households.size
            last_new_hhs_idx = self.mapping_existing_hhs_to_new_hhs.size
            self._do_run_for_this_year(households_for_this_area)
            add_hhs_size = self.new_households[self.location_id_name].size-self.new_households["large_area_id"].size
            remove_hhs_size = self.remove_households.size-last_remove_idx
            logger.log_status("add %s, remove %s, total %s" % (add_hhs_size, remove_hhs_size,
                                                               households_for_this_area.size()+add_hhs_size-remove_hhs_size
                                                               ))
            self.new_households["large_area_id"] = concatenate((self.new_households["large_area_id"],
                                            array(add_hhs_size*[area], dtype="int32")))
            # transform indices of removing households into indices of the whole dataset
            self.remove_households[last_remove_idx:self.remove_households.size] = all_households_index[households_index[self.remove_households[last_remove_idx:self.remove_households.size]]]
            # do the same for households to be duplicated
            self.mapping_existing_hhs_to_new_hhs[last_new_hhs_idx:self.mapping_existing_hhs_to_new_hhs.size] = all_households_index[households_index[self.mapping_existing_hhs_to_new_hhs[last_new_hhs_idx:self.mapping_existing_hhs_to_new_hhs.size]]]
            
        self._update_household_set(household_set)
        idx_new_households = arange(household_set.size()-self.new_households["large_area_id"].size, household_set.size())
        households_large_area_ids = household_set.compute_variables("washtenaw.household.large_area_id")
        households_large_area_ids[idx_new_households] = self.new_households["large_area_id"]
        household_set.delete_one_attribute("large_area_id")
        household_set.add_attribute(households_large_area_ids, "large_area_id", metadata=AttributeType.PRIMARY)
        # return an index of new households
        return idx_new_households

    def _do_initialize_for_run(self, household_set):
        HouseholdTransitionModel._do_initialize_for_run(self, household_set)
        self.new_households["large_area_id"] = array([], dtype="int32")




from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from numpy import array, logical_and, int32, int8, zeros
from numpy import ma
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset
from urbansim.datasets.control_total_dataset import ControlTotalDataset
class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        #1) 3000 households in large_area=1 with age_of_head < 50, income < 40,000, persons < 3.
        #2) 3000 households in large_area=2 with age_of_head < 50, income < 40,000, persons < 3.
        #3) 1000 households in large_area=1 with age_of_head < 50, income < 40,000, persons >= 3.
        #4) 1000 households in large_area=2 with age_of_head < 50, income < 40,000, persons >= 3.
        #5) 1500 households in large_area=1 with age_of_head < 50, income >= 40,000, persons < 3.
        #6) 1500 households in large_area=2 with age_of_head < 50, income >= 40,000, persons < 3.
        #7) 2000 households in large_area=1 with age_of_head < 50, income >= 40,000, persons >= 3.
        #8) 2000 households in large_area=2 with age_of_head < 50, income >= 40,000, persons >= 3.
        #9) 1000 households in large_area=1 with age_of_head >= 50, income < 40,000, persons < 3.
        #10) 1000 households in large_area=2 with age_of_head >= 50, income < 40,000, persons < 3.
        #11) 2500 households in large_area=1 with age_of_head >= 50, income < 40,000, persons >= 3.
        #12) 2500 households in large_area=2 with age_of_head >= 50, income < 40,000, persons >= 3.
        #13) 1500 households in large_area=1 with age_of_head >= 50, income >= 40,000, persons < 3.
        #14) 1500 households in large_area=2 with age_of_head >= 50, income >= 40,000, persons < 3.
        #15) 4000 households in large_area=1 with age_of_head >= 50, income >= 40,000, persons >= 3.
        #16) 4000 households in large_area=2 with age_of_head >= 50, income >= 40,000, persons >= 3.

        self.households_data = {
            "household_id":arange(33000)+1,
            "grid_id":       array(6000*[1] + 2000*[2] + 3000*[3] + 4000*[4] + 2000*[5] + 5000*[6] +
                                3000*[10]+ 8000*[100], dtype=int32),
            "large_area_id": array(3000*[1] + 3000*[2]+ 1000*[1] + 1000*[2] + 1500*[1] + 1500*[2] + 
                                   2000*[1] + 2000*[2] + 1000*[1] + 1000*[2] + 2500*[1] + + 2500*[2] + 
                                1500*[1]+  1500*[2]+ 4000*[1] + 4000*[2], dtype=int32),
            "age_of_head": array(6000*[40] + 2000*[45] + 3000*[25] + 4000*[35] + 2000*[50] + 5000*[60] +
                                3000*[75]+ 8000*[65], dtype=int32),
            "income": array(6000*[35000] + 2000*[25000] + 3000*[40000] + 4000*[50000] + 2000*[20000] +
                                5000*[25000] + 3000*[45000]+ 8000*[55000], dtype=int32),
            "persons": array(6000*[2] + 2000*[3] + 3000*[1] + 4000*[6] + 2000*[1] + 5000*[4] +
                                3000*[1]+ 8000*[5], dtype=int8),
            }
        self.household_characteristics_for_ht_data = {
            "characteristic": array(2*['age_of_head'] + 2*['income'] + 2*['persons']),
            "min": array([0, 50, 0, 40000, 0, 3]),
            "max": array([49, 100, 39999, -1, 2, -1])
            }

    def test_same_distribution_after_household_addition(self):
        """Using the control_totals and no marginal characteristics,
        add households and ensure that the distribution within each group stays the same
        """

        annual_household_control_totals_data = {
            "year": array([2000, 2000]),
            "total_number_of_households": array([20000, 30000]),
            "large_area_id": array([1,2])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name = 'hh_set', table_data = self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')
        
        storage.write_table(table_name = 'hct_set', table_data = annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household")

        storage.write_table(table_name = 'hc_set', table_data = self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = RegionalHouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are 20000 (area 1) and 30000 (area 2) total households after running the model
        areas = hh_set.get_attribute("large_area_id")
        results = array([0,0])
        for iarea in [0,1]:
            results[iarea] = where(areas == [1,2][iarea])[0].size
        should_be = [20000, 30000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of unplaced households is exactly the number of new households created
        results = where(hh_set.get_attribute("grid_id")<=0)[0].size
        should_be = [17000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group and each area is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = array([
                    # area 1 
                     3000.0/16500.0*20000.0, 1000.0/16500.0*20000.0, 1500.0/16500.0*20000.0, 2000.0/16500.0*20000.0,
                     1000.0/16500.0*20000.0, 2500.0/16500.0*20000.0, 1500.0/16500.0*20000.0, 4000.0/16500.0*20000.0,
                     # area 2
                     3000.0/16500.0*30000.0, 1000.0/16500.0*30000.0, 1500.0/16500.0*30000.0, 2000.0/16500.0*30000.0,
                     1000.0/16500.0*30000.0, 2500.0/16500.0*30000.0, 1500.0/16500.0*30000.0, 4000.0/16500.0*30000.0])
        self.assertEqual(ma.allclose(results, should_be, rtol=0.1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        # check the types of the attributes
        self.assertEqual(hh_set.get_attribute("age_of_head").dtype, int32,
                         "Error in data type of the new household set. Should be: int32, is: %s" % str(hh_set.get_attribute("age_of_head").dtype))
        self.assertEqual(hh_set.get_attribute("income").dtype, int32,
                         "Error in data type of the new household set. Should be: int32, is: %s" % str(hh_set.get_attribute("income").dtype))
        self.assertEqual(hh_set.get_attribute("persons").dtype, int8,
                         "Error in data type of the new household set. Should be: int8, is: %s" % str(hh_set.get_attribute("persons").dtype))

    def test_same_distribution_after_household_subtraction(self):
        """Using the control_totals and no marginal characteristics,
        subtract households and ensure that the distribution within each group stays the same
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000]),
            "total_number_of_households": array([8000, 12000]),
             "large_area_id": array([1,2])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name = 'hh_set', table_data = self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name = 'hct_set', table_data = annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household")

        storage.write_table(table_name = 'hc_set', table_data = self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = RegionalHouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 8000 (area 1) and 12000 (area 2) total households after running the model
        areas = hh_set.get_attribute("large_area_id")
        results = array([0,0])
        for iarea in [0,1]:
            results[iarea] = where(areas == [1,2][iarea])[0].size
        should_be = [8000, 12000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = array([# area 1 
                     3000.0/16500.0*8000.0, 1000.0/16500.0*8000.0, 1500.0/16500.0*8000.0, 2000.0/16500.0*8000.0,
                     1000.0/16500.0*8000.0, 2500.0/16500.0*8000.0, 1500.0/16500.0*8000.0, 4000.0/16500.0*8000.0,
                     # area 2
                     3000.0/16500.0*12000.0, 1000.0/16500.0*12000.0, 1500.0/16500.0*12000.0, 2000.0/16500.0*12000.0,
                     1000.0/16500.0*12000.0, 2500.0/16500.0*12000.0, 1500.0/16500.0*12000.0, 4000.0/16500.0*12000.0])
        self.assertEqual(ma.allclose(results, should_be, rtol=0.1),
                         True, "Error, should_be: %s,\n but result: %s" % (should_be, results))

    def test_controlling_with_one_marginal_characteristic(self):
        """Using the age_of_head as a marginal characteristic, which would partition the 8 groups into two larger groups
        (those with age_of_head < 40 and >= 40), ensure that the control totals are met and that the distribution within
        each large group is the same before and after running the model
        """

        #IMPORTANT: marginal characteristics grouping indices have to start at 0!
        #i.e. below, there is one marg. char. "age_of_head". here we indicate that the first "large group" (groups 1-4),
        #consisting of those groups with age_of_head < 40 should total 25000 households after running this model for one year,
        #and the second large group, those groups with age_of_head > 40, should total 15000 households
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "age_of_head": array([0, 1, 0, 1]),
            "total_number_of_households": array([20000, 10000, 5000, 5000]),
            "large_area_id": array([1, 1, 2, 2] )                                   
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name = 'hh_set', table_data = self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name = 'hct_set', table_data = annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household')

        storage.write_table(table_name = 'hc_set', table_data = self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = RegionalHouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 40000 total households after running the model
        areas = hh_set.get_attribute("large_area_id")
        results = array([0,0])
        for iarea in [0,1]:
            results[iarea] = where(areas == [1,2][iarea])[0].size
        should_be = [30000, 10000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of households within the groups correspond to the control totals
        results = self.get_count_all_groups(hh_set)
        should_be = [20000, 10000, 5000, 5000]
        idx1 = arange(0,4)
        idx2 = arange(4,8)
        idx3 = arange(8,12)
        idx4 = arange(12,16)
        self.assertEqual(ma.allclose([results[idx1].sum(), results[idx2].sum(), results[idx3].sum(), results[idx4].sum()], should_be, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, 
                                 array([results[idx1].sum(), results[idx2].sum(), results[idx3].sum(), results[idx4].sum()])))

        #check that the distribution of households within the groups are the same before and after
        #running the model, respectively

        should_be = [# area 1 
                     3000.0/7500.0*20000.0, 1000.0/7500.0*20000.0, 1500.0/7500.0*20000.0, 2000.0/7500.0*20000.0,
                     1000.0/9000.0*10000.0, 2500.0/9000.0*10000.0, 1500.0/9000.0*10000.0, 4000.0/9000.0*10000.0,
                     # area 2
                     3000.0/7500.0*5000.0, 1000.0/7500.0*5000.0, 1500.0/7500.0*5000.0, 2000.0/7500.0*5000.0,
                     1000.0/9000.0*5000.0, 2500.0/9000.0*5000.0, 1500.0/9000.0*5000.0, 4000.0/9000.0*5000.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def get_count_all_groups(self, hh_set):
        res = zeros(16)
        i=0
        for area in [1,2]:
            is_area = hh_set.get_attribute('large_area_id') == area
            for age_conditional in ["<", ">="]:
                tmp1 = eval("hh_set.get_attribute('age_of_head') %s 50" % age_conditional)
                for income_conditional in ["<", ">="]:
                    tmp2 = logical_and(tmp1, eval("hh_set.get_attribute('income') %s 40000" % income_conditional))
                    for persons_conditional in ["<", ">="]:
                        tmp3 = logical_and(tmp2, eval("hh_set.get_attribute('persons') %s 3" % persons_conditional))
                        res[i] = (logical_and(tmp3, is_area)).sum()
                        i+=1
        return res

if __name__=='__main__':
    opus_unittest.main()