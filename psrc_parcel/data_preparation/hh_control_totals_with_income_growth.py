# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, array, where, zeros, ones, logical_and, reshape, concatenate, clip, indices
from scipy.ndimage import sum as ndimage_sum
from copy import copy
from urbansim.models.household_transition_model import HouseholdTransitionModel

class HHControlTotalsWithIncomeGrowth(HouseholdTransitionModel):

    model_name = "HHControlTotalsWithIncomeGrowth"
        
    def __init__(self, income_growth_factor, **kwargs):
        HouseholdTransitionModel.__init__(self, **kwargs)
        self.income_growth_factor = income_growth_factor
        
    def run(self, year, household_set, control_totals, *args, **kwargs):
        self.control_totals = control_totals
        HouseholdTransitionModel.run(self, year, household_set, control_totals, *args, **kwargs)
        
    def _update_household_set(self, household_set):
        self.control_totals.load_and_flush_dataset()
        return None

    def _do_initialize_for_run(self, household_set):
        new_income = household_set['income']*self.income_growth_factor
        household_set['income'] = new_income
        HouseholdTransitionModel._do_initialize_for_run(self, household_set)
        if not "total_number_of_households_orig" in self.control_totals.get_known_attribute_names():
            orig_values = self.control_totals.get_attribute("total_number_of_households").copy()
            self.control_totals.add_primary_attribute(data=orig_values,
                                                      name="total_number_of_households_orig")


                
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
                self.new_households[attr] = array([], dtype=self.household_set.get_data_type(attr, "float32"))

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
            self.control_totals.set_value_of_attribute_by_id("total_number_of_households", number_in_group, id)

    def prepare_for_run(self, base_storage, run_storage):
        from urbansim.datasets.control_total_dataset import ControlTotalDataset
        from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset
        control_totals = ControlTotalDataset(in_storage=run_storage, what="household")
        characteristics = HouseholdCharacteristicDataset(in_storage=base_storage)
        return (control_totals, characteristics)
    
    