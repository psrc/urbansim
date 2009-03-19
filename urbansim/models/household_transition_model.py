# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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

class HouseholdTransitionModel(Model):
    """Creates and removes households from household_set. New households are duplicated from the existing households, keeping 
       the joint distribution of all characteristics. 
    """

    model_name = "Household Transition Model"

    def __init__(self, location_id_name="grid_id", debuglevel=0):
        self.debug = DebugPrinter(debuglevel)
        self.location_id_name = location_id_name

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
        idx = where(control_totals.get_attribute("year")==year)[0]
        self.control_totals_for_this_year = DatasetSubset(control_totals, idx)
        self._do_run_for_this_year(household_set)
        return self._update_household_set(household_set)
        
    def _update_household_set(self, household_set):
        index_of_duplicated_hhs = household_set.duplicate_rows(self.mapping_existing_hhs_to_new_hhs)
        household_set.modify_attribute(name=self.location_id_name, data=-1 * ones((index_of_duplicated_hhs.size,), 
                                                                              dtype=household_set.get_data_type(self.location_id_name)),
                                                                          index=index_of_duplicated_hhs)
        household_set.remove_elements(self.remove_households)
        if self.new_households[self.location_id_name].size > 0:
            max_id = household_set.get_id_attribute().max()
            self.new_households[self.household_id_name]=concatenate((self.new_households[self.household_id_name],
                                                             arange(max_id+1, max_id+self.new_households[self.location_id_name].size+1)))
            household_set.add_elements(self.new_households, require_all_attributes=False)

        difference = household_set.size()-self.household_size
        self.debug.print_debug("Difference in number of households: %s"
            " (original %s, new %s, created %s, deleted %s)"
                % (difference,
                   self.household_size,
                   household_set.size(),
                   self.new_households[self.household_id_name].size + self.mapping_existing_hhs_to_new_hhs.size,
                   self.remove_households.size),
            3)
        if self.location_id_name in household_set.get_attribute_names():
            self.debug.print_debug("Number of unplaced households: %s"
                % where(household_set.get_attribute(self.location_id_name) <=0)[0].size,
                3)
        return difference

    def _do_initialize_for_run(self, household_set):
        self.household_id_name = household_set.get_id_name()[0]
        self.new_households = {
           self.location_id_name:array([], dtype=household_set.get_data_type(self.location_id_name, int32)),
           self.household_id_name:array([], dtype=household_set.get_data_type(self.household_id_name, int32))
                   }
        self.remove_households = array([], dtype='int32')
        self.household_size = household_set.size()
        self.max_id = household_set.get_id_attribute().max()
        self.arrays_from_categories = {}
        self.arrays_from_categories_mapping = {}
        self.mapping_existing_hhs_to_new_hhs = array([], dtype=household_set.get_data_type(self.household_id_name, int32))
        
    def _do_run_for_this_year(self, household_set):
        self.household_set = household_set
        groups = self.control_totals_for_this_year.get_id_attribute()
        self.create_arrays_from_categories(self.household_set)

        all_characteristics = self.arrays_from_categories.keys()
        self.household_set.load_dataset_if_not_loaded(attributes = all_characteristics) # prevents from lazy loading to save runtime
        idx_shape = []
        number_of_combinations=1
        num_attributes=len(all_characteristics)
        for iattr in range(num_attributes):
            attr = all_characteristics[iattr]
            max_bins = self.arrays_from_categories[attr].max()+1
            idx_shape.append(max_bins)
            number_of_combinations=number_of_combinations*max_bins
            if attr not in self.new_households.keys():
                self.new_households[attr] = array([], dtype=self.household_set.get_data_type(attr, float32))

        self.number_of_combinations = int(number_of_combinations)
        idx_tmp = indices(tuple(idx_shape))
        
        categories_index = zeros((self.number_of_combinations,num_attributes))

        for i in range(num_attributes): #create indices of all combinations
            categories_index[:,i] = idx_tmp[i].ravel()

        categories_index_mapping = {}
        for i in range(self.number_of_combinations):
            categories_index_mapping[tuple(categories_index[i,].tolist())] = i

        def get_category(values):
            bins = map(lambda x, y: self.arrays_from_categories[x][int(y)], all_characteristics, values)
            try:
                return categories_index_mapping[tuple(bins)]
            except KeyError, msg: 
                where_error = where(array(bins) == -1)[0]
                if where_error.size > 0:
                    raise KeyError, \
                        "Invalid value of %s for attribute %s. It is not included in the characteristics groups." % (
                                                                               array(values)[where_error], 
                                                                               array(all_characteristics)[where_error])
                raise KeyError, msg

        if num_attributes > 0:
            # the next array must be a copy of the household values, otherwise, it changes the original values
            values_array = reshape(array(self.household_set.get_attribute(all_characteristics[0])), (self.household_set.size(),1))
            if num_attributes > 1:
                for attr in all_characteristics[1:]:
                    values_array = concatenate((values_array, reshape(array(self.household_set.get_attribute(attr)),
                                                                      (self.household_set.size(),1))), axis=1)
            for i in range(values_array.shape[1]):
                if values_array[:,i].max() > 10000:
                    values_array[:,i] = values_array[:,i]/10
                values_array[:,i] = clip(values_array[:,i], 0, self.arrays_from_categories[all_characteristics[i]].size-1)
    
            # determine for each household to what category it belongs to
            self.household_categories = array(map(lambda x: get_category(x), values_array)) # performance bottleneck
    
            number_of_households_in_categories = array(ndimage_sum(ones((self.household_categories.size,)),
                                                                    labels=self.household_categories+1,
                                                                    index = arange(self.number_of_combinations)+1))
        else:
            # no marginal characteristics; consider just one group
            self.household_categories = zeros(self.household_set.size(), dtype='int32')
            number_of_households_in_categories = array([self.household_set.size()])

        g=arange(num_attributes)

        #iterate over marginal characteristics
        for group in groups:
            if groups.ndim <= 1: # there is only one group (no marginal char.)
                id = group
            else:
                id = tuple(group.tolist())
            group_element = self.control_totals_for_this_year.get_data_element_by_id(id)
            total = group_element.total_number_of_households
            for i in range(g.size):
                g[i] = eval("group_element."+self.arrays_from_categories.keys()[i])
            if g.size <= 0:
                l = ones((number_of_households_in_categories.size,))
            else:
                l = categories_index[:,0] == g[0]
                for i in range(1,num_attributes):
                    l = logical_and(l, categories_index[:,i] == g[i])
            # l has 1's for combinations of this group
            number_in_group = array(ndimage_sum(number_of_households_in_categories, labels=l, index = 1))
            diff = int(total - number_in_group)
            if diff < 0: # households to be removed
                is_in_group = l[self.household_categories]
                w = where(is_in_group)[0]
                sample_array, non_placed, size_non_placed = \
                    get_array_without_non_placed_agents(self.household_set, w, -1*diff,
                                                          self.location_id_name)
                self.remove_households = concatenate((self.remove_households, non_placed, sample_noreplace(sample_array,
                                                                                   max(0,abs(diff)-size_non_placed))))
            if diff > 0: # households to be created
                self._create_households(diff, l)
            
    def _create_households(self, diff, l):
        # sample existing households to copy
        is_hh_in_group = l[self.household_categories]
        consider_hhs_idx = where(is_hh_in_group)[0]
        if consider_hhs_idx.size > 0:
            sample_from_existing_hhs = sample_replace(consider_hhs_idx, diff)
            self.mapping_existing_hhs_to_new_hhs = concatenate((self.mapping_existing_hhs_to_new_hhs, sample_from_existing_hhs))
        # If there are no households in that category, no new households are created
            

    def create_arrays_from_categories(self, household_set):
        # cleanup in case there was a previous run
        for attr in self.arrays_from_categories.keys():
            del self.arrays_from_categories[attr]  
            if attr in self.arrays_from_categories_mapping.keys():
                del self.arrays_from_categories_mapping[attr]
            
        self.arrays_from_categories = {}
        self.arrays_from_categories_mapping = {}

        mins = self.characteristics.get_attribute("min").astype(int32)
        maxs = self.characteristics.get_attribute("max").astype(int32)
        for attr in self.marginal_characteristic_names:
            if attr not in self.scaled_characteristic_names:
                bins = self.control_totals_for_this_year.get_attribute(attr)
                if bins.size == 0:
                    continue
                unique_bins = unique_values(bins)
                max_of_attr = unique_bins.max()
                self.arrays_from_categories[attr] = zeros((max_of_attr+1,))
                self.arrays_from_categories[attr][unique_bins] = unique_bins
            else:
                idx = where(self.all_categories == attr)[0]
                maximal_of_min = mins[idx].max()
                this_min = mins[idx].min()
                max_from_data = maximal_of_min
                if household_set.size() > 0:
                    max_from_data = household_set.get_attribute(attr).max()
                    if max_from_data > maximal_of_min:
                        # -1 in maximum is replaced by maximum from the data
                        maxs[idx[where(maxs[idx] < 0)]] = max_from_data
                if max_from_data <= maximal_of_min:
                    # there is no maximum in the data for the largest category,
                    # therefore determine the absolute maximum from the average bin range
                    if idx.size == 1:
                        category_range = maximal_of_min - this_min
                    else:
                        category_range = (maximal_of_min - this_min)/(idx.size-1)
                    maxs[idx[where(maxs[idx] < 0)]] = maximal_of_min + 2*category_range
    
                if maximal_of_min > 10000: # applies for income (internally it is divided by 10, modulo is added to the mins)
                    maxs[idx] = maxs[idx]/10
                    modulo = mins[idx] % 10
                    mins[idx] = where(modulo > 0, mins[idx]/10 + 1, mins[idx]/10)
    
                max_of_attr = maxs[idx].max()
                self.arrays_from_categories[attr] = resize(array([-1], dtype='int32'), int(max_of_attr)+1)
                self.arrays_from_categories_mapping[attr] = zeros((idx.size,2))
                sortidx = mins[idx].argsort() # the categories must be sorted
                j=0
                for i in idx[sortidx]:
                    self.arrays_from_categories[attr][mins[i]:(maxs[i]+1)] = j
                    self.arrays_from_categories_mapping[attr][j,:] = array([mins[i], maxs[i]])
                    j+=1



    def prepare_for_run(self, storage, **kwargs):
        from urbansim.datasets.control_total_dataset import ControlTotalDataset
        from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset
        from urbansim.models.employment_transition_model import sample_control_totals
        control_totals = ControlTotalDataset(in_storage=storage, what="household")
        characteristics = HouseholdCharacteristicDataset(in_storage=storage)
        sample_control_totals(storage, control_totals, **kwargs)
        return (control_totals, characteristics)

def create_scaled_array(characteristics, agent_set):
    scaled_array={}
    if "characteristic_opus" in characteristics.get_known_attribute_names():
        all_categories = characteristics.get_attribute("characteristic_opus") # to be changed to 'characteristic'
    else:
        all_categories = characteristics.get_attribute("characteristic")
    all_categories = array(all_categories.amap(lambda x: x.lower()))
    categories = get_distinct_names(all_categories)
    mins = characteristics.get_attribute("min")
    maxs = characteristics.get_attribute("max")
    for cat in categories:
        idx = where(all_categories == cat)[0]
        scaled_array[cat+"_index_mapping"] = {}
        scaled_array[cat+"_index"] = {}
        j=0
        for i in idx:
            this_min = mins[i]
            this_max = maxs[i]
            is_in_cat = reshape(array(agent_set.get_attribute(cat) >= this_min), shape=(1,agent_set.size()))
            if not scaled_array.has_key(cat):
                scaled_array[cat] = is_in_cat
            else:
                scaled_array[cat] = concatenate((scaled_array[cat], is_in_cat))
            if this_max >= 0: # there is a maximum
                scaled_array[cat][j,:] = logical_and(scaled_array[cat][j,:], array(agent_set.get_attribute(cat) <= this_max))
            scaled_array[cat+"_index_mapping"][(this_min, this_max)] = j
            scaled_array[cat+"_index"][j] = (this_min, this_max)

            j+=1
    return (scaled_array, categories)

from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from numpy import array, logical_and
from numpy import ma
from urbansim.datasets.household_dataset import HouseholdDataset
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
            "grid_id": array(6000*[1] + 2000*[2] + 3000*[3] + 4000*[4] + 2000*[5] + 5000*[6] +
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

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what="household", id_name="year")

        storage.write_table(table_name='hc_set', table_data=self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = HouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

        #check that there are indeed 50000 total households after running the model
        results = hh_set.size()
        should_be = [50000]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        #check that the number of unplaced households is exactly the number of new households created
        results = where(hh_set.get_attribute("grid_id")<=0)[0].size
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

        model = HouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

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

        model = HouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

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
        where10 = where(hh_set.get_attribute("grid_id")<>10)[0]
        hh_set.modify_attribute(name="grid_id", data=zeros(where10.size), index=where10)

        model = HouseholdTransitionModel()
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

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
            "grid_id": array(19950*[1] + 50*[0]),
            "income": array(1000*[1000] + 1000*[10000] + 2000*[20000] + 1000*[35000] + 2000*[45000] +
                                1000*[50000] + 2000*[67000]+ 2000*[90000] + 1000*[100005] + 2000*[110003] +
                                1000*[120000] + 1000*[200000] + 2000*[500000] + 1000*[630000])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=['year' ,'income'])

        storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = HouseholdTransitionModel(debuglevel=3)
        # this run should add households in all four categories
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

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
        model.run(year=2001, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
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
        model.run(year=2002, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
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
            "grid_id": array(15000*[1]),
            "age_of_head": array(1000*[25] + 1000*[28] + 2000*[32] + 1000*[34] +
                            2000*[35] + 1000*[40] + 1000*[54]+ 1000*[62] +
                            1000*[65] + 1000*[68] + 2000*[71] + 1000*[98])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household',
                                      id_name=['year' ,'age_of_head'])

        storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = HouseholdTransitionModel(debuglevel=3)
        # this run should add households in all four categories
        model.run(year=2000, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)

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
        model.run(year=2001, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
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
        model.run(year=2002, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
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