#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter, remove_from_array, get_distinct_names, unique_values
from opus_core.datasets.dataset import DatasetSubset
from urbansim.models.employment_transition_model import get_array_without_non_placed_agents
from numpy import arange, array, where, int8, zeros, ones, compress, logical_and, resize
from numpy import indices, bool8, int32, float32, reshape, clip, take, logical_not, argsort, concatenate
from scipy.ndimage import sum as ndimage_sum
from opus_core.sampling_toolbox import sample_replace, sample_noreplace, probsample_replace
from opus_core.storage_factory import StorageFactory
from opus_core.model import Model
from copy import copy
from time import time
from urbansim.models.household_transition_model import HouseholdTransitionModel as USHouseholdTransitionModel

class HouseholdTransitionModel(USHouseholdTransitionModel):
    """Creates and removes households from household_set. Also updates the persons table."""

    model_name = "Household Transition Model with Persons Update"
    location_id_name = "building_id"

    def run(self, year, household_set, person_set, control_totals, characteristics, resources=None):
        self.person_set = person_set
        return USHouseholdTransitionModel.run(self, year, household_set, control_totals, characteristics, resources=resources)
        
    def _update_household_set(self, household_set):
        """Updates also person set."""
        hh_ids_to_copy = household_set.get_id_attribute()[self.mapping_existing_hhs_to_new_hhs]
        result = USHouseholdTransitionModel._update_household_set(self, household_set)
        # remove person that have non-existing households
        person_attr_index = household_set.try_get_id_index(self.person_set.get_attribute(household_set.get_id_name()[0]), return_value_if_not_found=-9)
        eliminate_index = where(person_attr_index==-9)[0]
        self.person_set.remove_elements(eliminate_index)

        person_attr_index = household_set.get_id_index(self.person_set.get_attribute(household_set.get_id_name()[0]))
        hhs_to_duplicate = zeros(household_set.size(), dtype='bool8')
        hhs_to_duplicate[self.mapping_existing_hhs_to_new_hhs] = True
        
        persons_to_duplicate = zeros(self.person_set.size(), dtype='bool8')
        persons_to_duplicate[hhs_to_duplicate[person_attr_index]] = True
        if persons_to_duplicate.sum() <= 0:
            return result
        new_persons_idx = self.person_set.duplicate_rows(where(persons_to_duplicate))
        self.person_set.modify_attribute(name='job_id', data=zeros(new_persons_idx.size, dtype=self.person_set.get_data_type('job_id')), index=new_persons_idx)
        npersons_in_hhs = household_set.get_attribute_by_index('persons', self.mapping_existing_hhs_to_new_hhs)
        hh_ids = array([], dtype='int32')
        for i in arange(hh_ids_to_copy.size):
            hh_ids = concatenate((hh_ids, array([hh_ids_to_copy[i]]*npersons_in_hhs[i])))
        self.person_set.modify_attribute(name='household_id', data=hh_ids, index=new_persons_idx)
        return result


from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from numpy import array, logical_and
from numpy import ma
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim_parcel.datasets.person_dataset import PersonDataset
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset

class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        #1) 6000 households with age_of_head < 50, income < 40,000, persons < 3.
        #2) 2000 households with age_of_head < 50, income < 40,000, persons >= 3.
        #3) 3000 households with age_of_head < 50, income >= 40,000, persons < 3.
        #4) 4000 households with age_of_head < 50, income >= 40,000, persons >= 3.
        #5) 2000 households with age_of_head >= 50, income < 40,000, persons < 3.
        #6) 5000 households with age_of_head >= 50, income < 40,000, persons >= 3.
        #7) 3000 households with age_of_head >= 50, income >= 40,000, persons < 3.
        #8) 8000 households with age_of_head >= 50, income >= 40,000, persons >= 3.

        self.households_data = {
            "household_id":arange(33000)+1,
            "building_id": array(6000*[1] + 2000*[2] + 3000*[3] + 4000*[4] + 2000*[5] + 5000*[6] +
                                3000*[10]+ 8000*[100], dtype=int32),
            "age_of_head": array(6000*[40] + 2000*[45] + 3000*[25] + 4000*[35] + 2000*[50] + 5000*[60] +
                                3000*[75]+ 8000*[65], dtype=int32),
            "income": array(6000*[35000] + 2000*[25000] + 3000*[40000] + 4000*[50000] + 2000*[20000] +
                                5000*[25000] + 3000*[45000]+ 8000*[55000], dtype=int32),
            "persons": array(6000*[2] + 2000*[3] + 3000*[1] + 4000*[6] + 2000*[1] + 5000*[4] +
                                3000*[1]+ 8000*[5], dtype=int8)
            }
        self.household_characteristics_for_ht_data = {
            "characteristic": array(2*['age_of_head'] + 2*['income'] + 2*['persons']),
            "min": array([50, 0, 0, 40000, 0, 3]), # the first and second category of age_of_head is switched to test a row invariance 
            "max": array([100, 49, 39999, -1, 2, -1])
            }
        self.person_data = {
            "person_id": array([1,2]),
            "household_id": array([5,7]),
            "job_id": array([30, 50]),
                           }

    def test_same_distribution_after_household_addition(self):
        """Using the control_totals and no marginal characteristics,
        add households and ensure that the distribution within each group stays the same
        """

        annual_household_control_totals_data = {
            "year": array([2000]),
            "total_number_of_households": array([50000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household", id_name="year")

        storage.write_table(table_name='hc_set', table_data=self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = HouseholdTransitionModel()
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 50000 total households after running the model
        results = hh_set.size()
        should_be = [50000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of unplaced households is exactly the number of new households created
        results = where(hh_set.get_attribute("building_id")<=0)[0].size
        should_be = [17000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = array([6000.0/33000.0*50000.0, 2000.0/33000.0*50000.0, 3000.0/33000.0*50000.0, 4000.0/33000.0*50000.0,
                     2000.0/33000.0*50000.0, 5000.0/33000.0*50000.0, 3000.0/33000.0*50000.0, 8000.0/33000.0*50000.0])
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
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
            "year": array([2000]),
            "total_number_of_households": array([20000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household", id_name="year")

        storage.write_table(table_name='hc_set', table_data=self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        model = HouseholdTransitionModel()
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 20000 total households after running the model
        results = hh_set.size()
        should_be = [20000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households in each group is the same as before running the model
        results = self.get_count_all_groups(hh_set)
        should_be = [6000.0/33000.0*20000.0, 2000.0/33000.0*20000.0, 3000.0/33000.0*20000.0, 4000.0/33000.0*20000.0,
                     2000.0/33000.0*20000.0, 5000.0/33000.0*20000.0, 3000.0/33000.0*20000.0, 8000.0/33000.0*20000.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
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
            "year": array([2000, 2000]),
            "age_of_head": array([0,1]),
            "total_number_of_households": array([25000, 15000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['year' ,'age_of_head'])

        storage.write_table(table_name='hc_set', table_data=self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        model = HouseholdTransitionModel()
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 40000 total households after running the model
        results = hh_set.size()
        should_be = [40000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the total number of households within first four groups increased by 10000
        #and that the total number of households within last four groups decreased by 3000
        results = self.get_count_all_groups(hh_set)
        should_be = [25000, 15000]
        self.assertEqual(ma.allclose([sum(results[0:4]), sum(results[4:8])], should_be, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the distribution of households within groups 1-4 and 5-8 are the same before and after
        #running the model, respectively

        should_be = [6000.0/15000.0*25000.0, 2000.0/15000.0*25000.0, 3000.0/15000.0*25000.0, 4000.0/15000.0*25000.0,
                     2000.0/18000.0*15000.0, 5000.0/18000.0*15000.0, 3000.0/18000.0*15000.0, 8000.0/18000.0*15000.0]
        self.assertEqual(ma.allclose(results, should_be, rtol=0.05),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_controlling_with_three_marginal_characteristics(self):
        """Controlling with all three possible marginal characteristics in this example, age_of_head, income, and persons,
        this would partition the 8 groups into the same 8 groups, and with a control total specified for each group, we must
        ensure that the control totals for each group exactly meet the specifications.
        """

        #IMPORTANT: marginal characteristics grouping indices have to start at 0!
        annual_household_control_totals_data = {
            "year": array(8*[2000]),
            "age_of_head": array(4*[0] + 4*[1]),
            "income": array(2*[0] + 2*[1] + 2*[0] + 2*[1]),
            "persons": array([0,1,0,1,0,1,0,1]),
            "total_number_of_households": array([4000, 5000, 1000, 3000, 0, 6000, 3000, 8000])
            }
        #size of columns was not even, removed last element of min and max
        household_characteristics_for_ht_data = {
            "characteristic": array(2*['age_of_head'] + 2*['income'] + 2*['persons']),
            "min": array([0, 50, 0, 40000, 0, 3]),
            "max": array([49, 100, 39999, -1, 2, -1]) 
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['year' ,'age_of_head', 'income', 'persons'])

        storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        # unplace some households
        where10 = where(hh_set.get_attribute("building_id")<>10)[0]
        hh_set.modify_attribute(name="building_id", data=zeros(where10.size), index=where10)

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        model = HouseholdTransitionModel()
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 33000 total households after running the model
        results = hh_set.size()
        should_be = [30000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of households in each group exactly match the control totals specified
        results = self.get_count_all_groups(hh_set)
        should_be = [4000, 5000, 1000, 3000, 0, 6000, 3000, 8000]
        self.assertEqual(ma.allclose(results, should_be),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def get_count_all_groups(self, hh_set):
        res = zeros(8)
        i=0
        for age_conditional in ["<", ">="]:
            tmp1 = eval("where(hh_set.get_attribute('age_of_head') %s 50, 1,0)" % age_conditional)
            for income_conditional in ["<", ">="]:
                tmp2 = logical_and(tmp1, eval("where(hh_set.get_attribute('income') %s 40000, 1,0)" % income_conditional))
                for persons_conditional in ["<", ">="]:
                    tmp3 = logical_and(tmp2, eval("where(hh_set.get_attribute('persons') %s 3, 1,0)" % persons_conditional))
                    res[i] = tmp3.sum()
                    i+=1
        return res

    def test_controlling_income(self):
        """ Controls for one marginal characteristics, namely income.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000, 2001, 2001, 2001, 2001, 2002, 2002, 2002, 2002]),
            "income": array([0,1,2,3,0,1,2,3, 0,1,2,3]),
            "total_number_of_households": array([25013, 21513, 18227, 18493, # 2000
                                                 10055, 15003, 17999, 17654, # 2001
                                                 15678, 14001, 20432, 14500]) # 2002
            }

        household_characteristics_for_ht_data = {
            "characteristic": array(4*['income']),
            "min": array([0, 40000, 120000, 70000]), # category 120000 has index 3 and category 70000 has index 2 
            "max": array([39999, 69999, -1, 119999]) # (testing row invariance)
            }
        hc_sorted_index = array([0,1,3,2])
        households_data = {
            "household_id":arange(20000)+1,
            "building_id": array(19950*[1] + 50*[0]),
            "income": array(1000*[1000] + 1000*[10000] + 2000*[20000] + 1000*[35000] + 2000*[45000] +
                                1000*[50000] + 2000*[67000]+ 2000*[90000] + 1000*[100005] + 2000*[110003] +
                                1000*[120000] + 1000*[200000] + 2000*[500000] + 1000*[630000]),
            "persons": array(3000*[2] + 2000*[3] + 1000*[1] + 1000*[6] + 1000*[1] + 1000*[4] +
                                3000*[1]+ 8000*[5], dtype=int8)
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['year' ,'income'])

        storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        model = HouseholdTransitionModel(debuglevel=3)
        # this run should add households in all four categories
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        results = hh_set.size()
        should_be = [83246]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('income') <= 
                                            hc_set.get_attribute("max")[hc_sorted_index[0]], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('income') >= 
                                           hc_set.get_attribute("min")[hc_sorted_index[i]], 1,0),
                                     where(hh_set.get_attribute('income') <= 
                                           hc_set.get_attribute("max")[hc_sorted_index[i]], 1,0)).sum()
        results[-1] = where(hh_set.get_attribute('income') >= hc_set.get_attribute("min")[hc_sorted_index[-1]], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:4]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        model.run(year=2001, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[4:8]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('income') <= 
                                            hc_set.get_attribute("max")[hc_sorted_index[0]], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('income') >= 
                                           hc_set.get_attribute("min")[hc_sorted_index[i]], 1,0),
                                     where(hh_set.get_attribute('income') <= 
                                           hc_set.get_attribute("max")[hc_sorted_index[i]], 1,0)).sum()
        results[-1] = where(hh_set.get_attribute('income') >= hc_set.get_attribute("min")[hc_sorted_index[-1]], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[4:8]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        model.run(year=2002, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[8:13]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('income') <= hc_set.get_attribute("max")[hc_sorted_index[0]], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('income') >= 
                                           hc_set.get_attribute("min")[hc_sorted_index[i]], 1,0),
                                     where(hh_set.get_attribute('income') <= 
                                           hc_set.get_attribute("max")[hc_sorted_index[i]], 1,0)).sum()
        results[-1] = where(hh_set.get_attribute('income') >= hc_set.get_attribute("min")[hc_sorted_index[-1]], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[8:13]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_controlling_age_of_head(self):
        """ Controls for one marginal characteristics, namely age_of_head.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002]),
            "age_of_head": array([0,1,2,0,1,2, 0,1,2]),
            "total_number_of_households": array([25013, 21513, 18227,  # 2000
                                                 10055, 15003, 17999, # 2001
                                                 15678, 14001, 20432]) # 2002
            }

        household_characteristics_for_ht_data = {
            "characteristic": array(3*['age_of_head']),
            "min": array([0, 35, 65]),
            "max": array([34, 64, -1])
            }

        households_data = {
            "household_id":arange(15000)+1,
            "building_id": array(15000*[1]),
            "age_of_head": array(1000*[25] + 1000*[28] + 2000*[32] + 1000*[34] +
                            2000*[35] + 1000*[40] + 1000*[54]+ 1000*[62] +
                            1000*[65] + 1000*[68] + 2000*[71] + 1000*[98]),
            "persons": array(1000*[2] + 2000*[3] + 1000*[1] + 1000*[6] + 1000*[1] + 1000*[4] +
                                3000*[1]+ 5000*[5], dtype=int8)
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household',
                                      id_name=['year' ,'age_of_head'])

        storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        storage.write_table(table_name='prs_set', table_data=self.person_data)
        prs_set = PersonDataset(in_storage=storage, in_table_name='prs_set')
        
        model = HouseholdTransitionModel(debuglevel=3)
        # this run should add households in all four categories
        model.run(year=2000, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[0], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[i], 1,0),
                                 where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[i], 1,0)).sum()
        results[hc_set.size()-1] = where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[hc_set.size()-1], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        model.run(year=2001, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[3:6]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[0], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[i], 1,0),
                                 where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[i], 1,0)).sum()
        results[hc_set.size()-1] = where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[hc_set.size()-1], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[3:6]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        model.run(year=2002, person_set=prs_set, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[6:9]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(hc_set.size(), dtype=int32)
        results[0] = where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[0], 1,0).sum()
        for i in range(1, hc_set.size()-1):
            results[i] = logical_and(where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[i], 1,0),
                                 where(hh_set.get_attribute('age_of_head') <= hc_set.get_attribute("max")[i], 1,0)).sum()
        results[hc_set.size()-1] = where(hh_set.get_attribute('age_of_head') >= hc_set.get_attribute("min")[hc_set.size()-1], 1,0).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[6:9]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
if __name__=='__main__':
    opus_unittest.main()