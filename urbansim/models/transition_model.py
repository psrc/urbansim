# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import DatasetSubset
from numpy import array, where, ones, zeros, setdiff1d, logical_and
from numpy import arange, concatenate, resize, int32, float64, ceil
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_noreplace, sample_replace
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
import re

try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
except:
    PrettyTable = None
    
class TransitionModel(Model):
    """ The generic model behind household transition model and employment transition
    model
    """
    
    model_name = "Transition Model"
    model_short_name = "TM"
    
    def __init__(self, dataset, 
                 dataset_accounting_attribute=None,
                 control_total_dataset=None, 
                 model_name=None, 
                 model_short_name=None,
                 **kwargs):
        self.dataset = dataset
        self.dataset_accounting_attribute = dataset_accounting_attribute
        self.control_totals = control_total_dataset
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
        
    def run(self, year=None, 
            target_attribute_name='number_of_households', 
            sample_filter="", 
            reset_dataset_attribute_value={}, 
            dataset_pool=None,  **kwargs):
        """ sample_filter attribute/variable indicates which records in the dataset are eligible in the sampling for removal or cloning
        """
        #if dataset_pool is None:
        #    dataset_pool = SessionConfiguration().get_dataset_pool()

        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = where(self.control_totals.get_attribute('year')==year)[0]
        control_totals_for_this_year = DatasetSubset(self.control_totals, this_year_index)
        column_names = list(set( self.control_totals.get_known_attribute_names() ) - set( [ target_attribute_name, 'year', '_hidden_id_'] ))
        column_names.sort(reverse=True)
        column_values = dict([ (name, control_totals_for_this_year.get_attribute(name)) for name in column_names + [target_attribute_name]])
        
        independent_variables = list(set([re.sub('_max$', '', re.sub('_min$', '', col)) for col in column_names]))
        dataset_known_attributes = self.dataset.get_known_attribute_names()
        for variable in independent_variables:
            if variable not in dataset_known_attributes:
                self.dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)
        dataset_known_attributes = self.dataset.get_known_attribute_names() #update after compute
        if sample_filter:
            short_name = VariableName(sample_filter).get_alias()
            if short_name not in dataset_known_attributes:
                filter_indicator = self.dataset.compute_variables(sample_filter, dataset_pool=dataset_pool)
            else:
                filter_indicator = self.dataset.get_attribute(short_name)
        else:
            filter_indicator = 1

        to_be_cloned = array([], dtype=int32)
        to_be_removed = array([], dtype=int32)
        #log header
        if PrettyTable is not None:
            status_log = PrettyTable()
            status_log.set_field_names(column_names + ["actual", "target", "difference", "action"])
        else:        
            logger.log_status("\t".join(column_names + ["actual", "target", "difference", "action"]))
        error_log = ''
        for index in range(control_totals_for_this_year.size()):
            lucky_index = None
            indicator = ones( self.dataset.size(), dtype='bool' )
            criterion = {}
            for attribute in independent_variables:
                if attribute in dataset_known_attributes:
                    dataset_attribute = self.dataset.get_attribute(attribute)
                else:
                    raise ValueError, "attribute %s used in control total dataset can not be found in dataset %s" % (attribute, self.dataset.get_dataset_name())
                if attribute + '_min' in column_names:
                    amin = column_values[attribute + '_min'][index]
                    criterion.update({attribute + '_min':amin})
                    if amin != -1:
                        indicator *= dataset_attribute >= amin
                if attribute + '_max' in column_names: 
                    amax = column_values[attribute+'_max'][index]
                    criterion.update({attribute + '_max':amax}) 
                    if amax != -1:
                        indicator *= dataset_attribute <= amax
                if attribute in column_names: 
                    aval = column_values[attribute][index] 
                    criterion.update({attribute:aval}) 
                    if aval == -1:
                        continue
                    elif aval == -2:   ##treat -2 in control totals column as complement set, i.e. all other values not already specified in this column
                        complement_values = setdiff1d( dataset_attribute, column_values[attribute] )
                        has_one_of_the_complement_value = zeros(dataset_attribute.size, dtype='bool')
                        for value in complement_values:
                            has_one_of_the_complement_value += dataset_attribute == value
                        indicator *= has_one_of_the_complement_value
                    else:
                        indicator *= dataset_attribute == aval
                        
            target_num = column_values[target_attribute_name][index]
            ## if accounting attribute is None, count number of agents with indicator = True 
            if self.dataset_accounting_attribute is None:
                actual_num = indicator.sum()
                action_num = 0
                diff = target_num - actual_num
                if actual_num != target_num:
                    legit_index = where(logical_and(indicator, filter_indicator))[0]
                    if legit_index.size > 0:                    
                        if actual_num < target_num:
                            lucky_index = sample_replace(legit_index, target_num - actual_num)
                            to_be_cloned = concatenate((to_be_cloned, lucky_index))
                        elif actual_num > target_num:
                            lucky_index = sample_noreplace(legit_index, actual_num-target_num)
                            to_be_removed = concatenate((to_be_removed, lucky_index))
                        action_num = lucky_index.size
                    else:
                        error_log += "There is nothing to sample from %s and no action will happen for " % self.dataset.get_dataset_name() + \
                                  ','.join([col+"="+str(criterion[col]) for col in column_names]) + '\n'
                        
            else: 
                ## sum accounting attribute for agents with indicator = True; 
                ## assume dataset_accouting_attribute is a primary attribute 
                accounting = self.dataset.get_attribute(self.dataset_accounting_attribute) * indicator
                actual_num = accounting.sum()
                mean_size = float(actual_num) / indicator.sum()
                action_num = 0
                diff = target_num - actual_num
                if actual_num != target_num:
                    legit_index = where(logical_and(indicator, filter_indicator))[0]
                    if legit_index.size > 0:
                        while actual_num + action_num < target_num:
                            lucky_index = sample_replace(legit_index, ceil((target_num - actual_num - action_num)/mean_size) )
                            action_num += accounting[lucky_index].sum()
                            to_be_cloned = concatenate((to_be_cloned, lucky_index))
                        while actual_num - action_num > target_num:
                            lucky_index = sample_noreplace(legit_index, ceil((actual_num - target_num - action_num)/mean_size) )
                            action_num += accounting[lucky_index].sum()
                            to_be_removed = concatenate((to_be_removed, lucky_index))                
                    else:
                        error_log += "There is nothing to sample from %s and no action will happen for " % self.dataset.get_dataset_name() + \
                                  ','.join([col+"="+str(criterion[col]) for col in column_names]) + '\n'
            
            ##log status
            action = "0"
            if lucky_index is not None:                    
                if actual_num < target_num: action = "+" + str(action_num)
                if actual_num > target_num: action = "-" + str(action_num)
                    
            cat = [ str(criterion[col]) for col in column_names]
            cat += [str(actual_num), str(target_num), str(diff), action]
            if PrettyTable is not None:
                status_log.add_row(cat)
            else:
                logger.log_status("\t".join(cat))

        if PrettyTable is not None:
            logger.log_status("\n" + status_log.get_string())
        if error_log:
            logger.log_error(error_log)
                    
        clone_data = {}
        if to_be_cloned.size > 0:
            ### ideally duplicate_rows() is all needed to add newly cloned rows
            ### to be more cautious, copy the data to be cloned, remove elements, then append the cloned data
            ##self.dataset.duplicate_rows(to_be_cloned)
            logger.log_status()
            for attribute in dataset_known_attributes:
                if reset_dataset_attribute_value.has_key(attribute):
                    clone_data[attribute] = resize(array(reset_dataset_attribute_value[attribute]), to_be_cloned.size)
                else:
                    clone_data[attribute] = self.dataset.get_attribute_by_index(attribute, to_be_cloned)
                    
        self.post_run(self.dataset, to_be_cloned, to_be_removed, **kwargs)
        
        if to_be_removed.size > 0:
            logger.log_status()
            self.dataset.remove_elements(to_be_removed)
            
        if clone_data:
            self.dataset.add_elements(data=clone_data, change_ids_if_not_unique=True)
            
        return self.dataset
    
    def prepare_for_run(self, control_total_dataset_name=None, control_total_table=None, control_total_storage=None):
        if (control_total_storage is None) or ((control_total_table is None) and (control_total_dataset_name is None)):
            dataset_pool = SessionConfiguration().get_dataset_pool()
            self.control_totals = dataset_pool.get_dataset( 'annual_%s_control_total' % self.dataset.get_dataset_name() )
            return self.control_totals
        
        if not control_total_dataset_name:
            control_total_dataset_name = DatasetFactory().dataset_name_for_table(control_total_table)
        
        self.control_totals = DatasetFactory().search_for_dataset(control_total_dataset_name,
                                                                  package_order=SessionConfiguration().package_order,
                                                                  arguments={'in_storage':control_total_storage, 
                                                                             'in_table_name':control_total_table,
                                                                             'id_name':[]
                                                                             }
                                                                  )
        return self.control_totals
    
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function, like synchronizing persons with households table
        """
        pass
                
from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from numpy import array, logical_and, int32, int8
from numpy import ma
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim_parcel.datasets.business_dataset import BusinessDataset
from opus_core.storage_factory import StorageFactory
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

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

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

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

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
            "age_of_head_min": array([ 50,  0]),
            "age_of_head_max": array([100, 49]),
            "total_number_of_households": array([15000, 25000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        storage.write_table(table_name='hc_set', table_data=self.household_characteristics_for_ht_data)
        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

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
            #"age_of_head": array(4*[0] + 4*[1]),
            "age_of_head_min": array([ 0, 0, 0, 0, 50, 50, 50, 50]),
            "age_of_head_max": array([49,49,49,49,100,100,100,100]),
            #"income": array(2*[0] + 2*[1] + 2*[0] + 2*[1]),
            "income_min": array([    0,    0,40000,40000,    0,    0,40000,40000]),
            "income_max": array([39999,39999,   -1,   -1,39999,39999,   -1,   -1]),
            #"persons": array([0,1,0,1,0,1,0,1]),
            "persons_min": array([0, 3,0, 3,0, 3,0, 3]),
            "persons_max": array([2,-1,2,-1,2,-1,2,-1]),
            "total_number_of_households": array([4000, 5000, 1000, 3000, 0, 6000, 3000, 8000])
            }
        ##size of columns was not even, removed last element of min and max
        #household_characteristics_for_ht_data = {
            #"characteristic": array(2*['age_of_head'] + 2*['income'] + 2*['persons']),
            #"min": array([0, 50, 0, 40000, 0, 3]),
            #"max": array([49, 100, 39999, -1, 2, -1]) 
            #}
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=self.households_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')

        storage.write_table(table_name='hct_set', table_data=annual_household_control_totals_data)
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        #storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        #hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        # unplace some households
        where10 = where(hh_set.get_attribute("grid_id")<>10)[0]
        hh_set.modify_attribute(name="grid_id", data=zeros(where10.size), index=where10)

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

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
            #"income": array([0,1,2,3,0,1,2,3, 0,1,2,3]),
            "income_min": array([    0,40000, 70000,120000,     0,40000, 70000,120000,     0,40000, 70000,120000]),
            "income_max": array([39999,69999,119999,    -1, 39999,69999,119999,    -1, 39999,69999,119999,    -1]),
            "total_number_of_households": array([25013, 21513, 18227, 18493, # 2000   
                                                 10055, 15003, 17999, 17654, # 2001
                                                 15678, 14001, 20432, 14500]) # 2002
            }

        #household_characteristics_for_ht_data = {
            #"characteristic": array(4*['income']),
            #"min": array([0, 40000, 120000, 70000]), # category 120000 has index 3 and category 70000 has index 2 
            #"max": array([39999, 69999, -1, 119999]) # (testing row invariance)
            #}
        #hc_sorted_index = array([0,1,3,2])
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
        hct_set = ControlTotalDataset(in_storage=storage, in_table_name='hct_set', what='household', id_name=[])

        #storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        #hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        results = hh_set.size()
        should_be = [83246]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 4
        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+1]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:4]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        #model.run(year=2001, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2001, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[4:8]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[4]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+4],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i+4]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+5]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[4:8]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        #model.run(year=2002, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2002, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[8:12]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[8]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+8],
                                     hh_set.get_attribute('income') <= hct_set.get_attribute("income_max")[i+8]).sum()
        results[-1] = (hh_set.get_attribute('income') >= hct_set.get_attribute("income_min")[i+9]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[8:12]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_controlling_age_of_head(self):
        """ Controls for one marginal characteristics, namely age_of_head.
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002]),
            #"age_of_head": array([0,1,2,0,1,2, 0,1,2]),
            "age_of_head_min": array([ 0,35,65,  0,35,65,  0,35,65]),
            "age_of_head_max": array([34,64,-1, 34,64,-1, 34,64,-1]),
            "total_number_of_households": array([25013, 21513, 18227,  # 2000
                                                 10055, 15003, 17999, # 2001
                                                 15678, 14001, 20432]) # 2002
            }

        #household_characteristics_for_ht_data = {
            #"characteristic": array(3*['age_of_head']),
            #"min": array([0, 35, 65]),
            #"max": array([34, 64, -1])
            #}

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
                                      id_name=[])

        #storage.write_table(table_name='hc_set', table_data=household_characteristics_for_ht_data)
        #hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')
        
        model = TransitionModel(hh_set, control_total_dataset=hct_set)
        model.run(year=2000, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})

        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+1]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        #model.run(year=2001, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2001, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[3:6]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = (hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0]).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+3],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i+3]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+4]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[3:6]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        #model.run(year=2002, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2002, target_attribute_name="total_number_of_households", reset_dataset_attribute_value={'grid_id':-1})
        results = hh_set.size()
        should_be = [(hct_set.get_attribute("total_number_of_households")[6:9]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        results = zeros(cats, dtype=int32)
        results[0] = where(hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[0], 1,0).sum()
        for i in range(1, cats-1):
            results[i] = logical_and(hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+6],
                                     hh_set.get_attribute('age_of_head') <= hct_set.get_attribute("age_of_head_max")[i+6]).sum()
        results[-1] = (hh_set.get_attribute('age_of_head') >= hct_set.get_attribute("age_of_head_min")[i+7]).sum()
        should_be = hct_set.get_attribute("total_number_of_households")[6:9]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        
    def test_controlling_sector(self):
        """ Controls for one marginal characteristics, namely age_of_head.
        """
        annual_employment_control_totals_data = {
            "year": array([2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002]),
            "sector_id": array([ 1,2,3, 1,2,3,  1,2,3]),
            "number_of_jobs": array([25013, 21513, 18227,  # 2000
                                                 10055, 15003, 17999, # 2001
                                                 15678, 14001, 20432]) # 2002
            }


        jobs_data = {
            "job_id":arange(15000)+1,
            "grid_id": array(15000*[1]),
            "sector_id": array(1000*[1] + 1000*[1] + 2000*[1] + 1000*[1] +
                            2000*[2] + 1000*[2] + 1000*[2]+ 1000*[2] +
                            1000*[3] + 1000*[3] + 2000*[3] + 1000*[3])
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='job_set', table_data=jobs_data)
        job_set = JobDataset(in_storage=storage, in_table_name='job_set')

        storage.write_table(table_name='ect_set', table_data=annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name='ect_set', what='',
                                      id_name=[])

        
        model = TransitionModel(job_set, control_total_dataset=ect_set)
        model.run(year=2000, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})

        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should remove households in all four categories
        #model.run(year=2001, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2001, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[3:6]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i+3]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[3:6]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        # this run should add and remove households
        #model.run(year=2002, household_set=hh_set, control_totals=hct_set, characteristics=hc_set)
        model.run(year=2002, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})
        results = job_set.size()
        should_be = [(ect_set.get_attribute("number_of_jobs")[6:9]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=1e-1),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = (job_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i+6]).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[6:9]
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-6),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

    def test_accounting_attribute(self):
        """
        """
        annual_employment_control_totals_data = {
            "year":           array([2000,   2000,  2000,  2001]),
            "sector_id":      array([    1,     2,     3,     2]),
            "number_of_jobs": array([25013,  1513,  5000, 10055])
            }


        business_data = {
            "business_id":arange(1500)+1,
            "grid_id": array(1500*[1]),
            "sector_id": array(500*[1] +
                               500*[2] + 
                               500*[3]),
            "jobs":      array(500*[10] + 
                               500*[10] +
                               500*[10]),
                            
            }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='bs_set', table_data=business_data)
        bs_set = BusinessDataset(in_storage=storage, in_table_name='bs_set')

        storage.write_table(table_name='ect_set', table_data=annual_employment_control_totals_data)
        ect_set = ControlTotalDataset(in_storage=storage, in_table_name='ect_set', what='',
                                      id_name=[])

        model = TransitionModel(bs_set, dataset_accounting_attribute='jobs', control_total_dataset=ect_set)
        model.run(year=2000, target_attribute_name="number_of_jobs", reset_dataset_attribute_value={'grid_id':-1})

        results = bs_set.get_attribute('jobs').sum()
        should_be = [(ect_set.get_attribute("number_of_jobs")[0:3]).sum()]
        self.assertEqual(ma.allclose(should_be, results, rtol=10),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))
        
        cats = 3
        results = zeros(cats, dtype=int32)
        for i in range(0, cats):
            results[i] = ( bs_set.get_attribute('jobs')*(bs_set.get_attribute('sector_id') == ect_set.get_attribute("sector_id")[i])).sum()
        should_be = ect_set.get_attribute("number_of_jobs")[0:3]
        self.assertEqual(ma.allclose(results, should_be, rtol=10),
                         True, "Error, should_be: %s, but result: %s" % (should_be, results))

        
if __name__=='__main__':
    opus_unittest.main()