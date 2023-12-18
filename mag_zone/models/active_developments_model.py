# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset, DatasetSubset
from numpy import where, minimum, array, in1d, unique1d
from prettytable import PrettyTable
from opus_core.misc import DebugPrinter


class ActiveDevelopmentsModel(Model):
    """
    
    If you have questions, contact Jesse Ayers at MAG:  jayers@azmag.gov
    
    """

    model_name = "Active Developments Model"
    model_short_name = "ADM"

    def __init__(self, debuglevel=0):
        self.debug = DebugPrinter(debuglevel)
        self.debuglevel = debuglevel

    def run(self, percent_active_development=100, build_minimum_units=False, year=None, start_year=None,
            dataset_pool=None,
            capacity_this_year_variable='mag_zone.active_development.capacity_this_year'):
        # General TODO:
        #    - deal w/ "other_spaces" columns
        #    - look at generalizing the weight used when building units
        #    - build unit test for minimum build feature

        # LIST OF MODEL ASSUMPTIONS:
        #    - TODO: can i generalize the need for these pre-defined variables?
        #    - the model expects variables to exist that correspond to this naming pattern
        #      for every is_developing building_type_name in the building_types dataset:
        #        - total_<building_type_name>_units_col
        #        - occupied_<building_type_name>_units_col
        #    - building_type_name must be unique, lowercase, contain no spaces
        #    - target_vacancy.is_developing defines which building_types are considered
        
        # Minimum build feature
        #    - The user can specify 2 additional columns in the building_types dataset:
        #        - adm_minimum_annual_build_units
        #        - adm_minimum_annual_build_max_year
        #    - If these fields are present, and the "build_minimum_units" run option is set to True
        #        - The model will utilize the information in the fields to build the minimum # of units annually 
        #          specified in the building_types table up to the maximum year specified in the table.  This feature
        #          is designed to simulate the case when demand is too low to build new units, some will be built anyway
        
        # CURRENT LIST OF KNOWN ISSUES:
        #    - 


        # Get current simulation year
        if year is None:
            simulation_year = SimulationState().get_current_time()
        else:
            simulation_year = year
        
        # only run if start_year
        if start_year:
            if start_year > simulation_year:
                return
        
        # Get the percent_active_development
        # convert it to a float
        percent_active_development = percent_active_development / 100.0

        # Get the dataset pool
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()
        else:
            dataset_pool = dataset_pool

        # get the active_developments dataset, subset it for actually active projects
        # compute some variables
        developments_dataset = dataset_pool.get_dataset('active_developments')
        active_developments_capacity = developments_dataset.compute_variables([capacity_this_year_variable])
        # TODO: need to further filter active developments, not only by start_year<=simulation_year,
        #       but also by whether they are built out, etc.
        active_developments_index = where(developments_dataset.get_attribute('start_year')<=simulation_year)[0]
        active_developments_capacity_this_year = active_developments_capacity[active_developments_index]
        # debug help
        self.debug.print_debug('\n*** BEGIN DEBUG INFO:', 1)
        self.debug.print_debug('len(active_developments_index) = %s' % len(active_developments_index), 1)
        self.debug.print_debug('len(active_developments_index) = %s' % len(active_developments_index), 1)
        self.debug.print_debug('len(active_developments_capacity_this_year) = %s' % len(active_developments_capacity_this_year), 1)
        self.debug.print_debug('END DEBUG INFO ***\n', 1)

        # get the target_vacancy_rates dataset
        target_vacancy_rates_dataset = dataset_pool.get_dataset('target_vacancy')
        # get target vacancy rates for this simulation_year
        this_year_index = where(target_vacancy_rates_dataset.get_attribute('year')==simulation_year)[0]
        target_vacancies_for_this_year = DatasetSubset(target_vacancy_rates_dataset, this_year_index)
        # get some columns
        bldg_types = target_vacancies_for_this_year.get_attribute('building_type_id')
        tgt_vacancies = target_vacancies_for_this_year.get_attribute('target_vacancy')
        # get unique building types
        unique_building_types = unique1d(bldg_types)
        # build a dictionary containing building_type_id:{'target_vacancy_rate':<float>}
        developing_building_types_info = {}
        for unique_building_type in unique_building_types:
            unique_building_type_index = where(bldg_types==unique_building_type)[0]
            developing_building_types_info[unique_building_type] = {'target_vacancy_rate':tgt_vacancies[unique_building_type_index].mean()}
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('developing_building_types_info', developing_building_types_info)

        # get the building_types dataset
        building_types_dataset = dataset_pool.get_dataset('building_type')
        # get the attribute names
        # I don't think this next line is used at all:
        #building_types_dataset_attribute_names = building_types_dataset.get_attribute_names()

        # get only the developing building types
        developing_types_index = where(building_types_dataset.get_attribute('is_developing')==1)[0]
        developing_building_types_dataset = DatasetSubset(building_types_dataset, developing_types_index)
        # calculate active development capacity this simulation_year
        developing_building_type_ids = developing_building_types_dataset.get_attribute('building_type_id')
        building_type_names = developing_building_types_dataset.get_attribute('building_type_name')

        # add building_type_name to the dictionary
        # now the dictionary takes the form of: 
        #    building_type_id:{'target_vacancy_rate':<float>,'building_type_name':<string>}
        counter = 0
        for developing_building_type_id in developing_building_type_ids:
            try:
                developing_building_types_info[developing_building_type_id]['building_type_name'] = building_type_names[counter]
                counter += 1
            except:
                logger.log_warning('You may have a mismatch in the building_type_ids between those in the target_vacancies dataset and the developing types in the building_types dataset.')
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('developing_building_types_info', developing_building_types_info)


        # add 'is_residential' to the developing_building_types_info dictionary
        # now the dictionary takes the form of: 
        #    building_type_id:{'target_vacancy_rate':<float>,'building_type_name':<string>,'is_residential':<integer>}
        for developing_building_type in developing_building_types_info:
            indx = where(building_types_dataset.get_attribute('building_type_id')==developing_building_type)[0]
            developing_building_types_info[developing_building_type]['is_residential'] = building_types_dataset.get_attribute('is_residential')[indx][0]
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('developing_building_types_info', developing_building_types_info)
            
        # add 'adm_minimum_annual_build_units' and 'adm_minimum_annual_build_max_year' to the developing_building_types_info dictionary
        # now the dictionary takes the form of:
        #    building_type_id:{'':<float>,'building_type_name':<string>,'is_residential':<integer>,'adm_minimum_annual_build_units':<integer>, 'adm_minimum_annual_build_max_units':<integer>}
        if build_minimum_units:
            try:
                for developing_building_type in developing_building_types_info:
                    indx = where(building_types_dataset.get_attribute('building_type_id')==developing_building_type)[0]
                    developing_building_types_info[developing_building_type]['adm_minimum_annual_build_units'] = building_types_dataset.get_attribute('adm_minimum_annual_build_units')[indx][0]
                for developing_building_type in developing_building_types_info:
                    indx = where(building_types_dataset.get_attribute('building_type_id')==developing_building_type)[0]
                    developing_building_types_info[developing_building_type]['adm_minimum_annual_build_max_year'] = building_types_dataset.get_attribute('adm_minimum_annual_build_max_year')[indx][0]
            except:
                logger.log_error('\n\nYou have the option "build_minimum_units" set to "True" but appear to be missing the "adm_minimum_annual_build_units" and "adm_minimum_annual_build_max_year" units in your "building_types" dataset.\n')
                return

        # build a list of total and occupied units variables to compute of the form
        #     ['occupied_rsf_units_col','total_rsf_units_col', ...]
        # The variables that this section creates and computes need to be defined in the buildings
        #     dataset aliases.py file        
        building_variables = []
        for building_type_id,dict_of_info in developing_building_types_info.items():
            try:
                total, occupied = 'total_%s_units_col' % dict_of_info['building_type_name'], 'occupied_%s_units_col' % dict_of_info['building_type_name']
                building_variables.append(total)
                building_variables.append(occupied)
            except:
                logger.log_warning('You may have a mismatch in the building_type_ids between those in the target_vacancies dataset and the developing types in the building_types dataset.')                
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('building_variables', building_variables)


        # get the buildings dataset
        buildings_dataset = dataset_pool.get_dataset('building')
        # compute total and occupied units variables
        buildings_dataset.compute_variables(building_variables)
        # sum up those variables into a dictionary of the form:
        #    {'occupied_rsf_units':<integer>, 'total_rsf_units':<integer>, ...}
        total_and_occupied_variable_sums = {}
        for building_variable in building_variables:
            summed_attribute = buildings_dataset.get_attribute('%s' % building_variable).sum()
            total_and_occupied_variable_sums[building_variable.replace('_col','')] = summed_attribute
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('total_and_occupied_variable_sums', total_and_occupied_variable_sums)


        # set up a table to log into
        status_log = PrettyTable()
        status_log.set_field_names([#"Type",
                                    "Name",
                                    "Occ Units",
                                    "Tot Units",
                                    "CurrentVR",
                                    "Target Units",
                                    "TargetVR",
                                    "Difference",
                                    "Max Act Dev Action",
                                    "Avail Act Dev",
                                    "Build Action"])

        # compute target units, vacancy rates, etc
        # go over each developing building type and compute target units, differences, total development required, 
        #    available capacity in active_developments, and action to take in active_developments
        for developing_building_type in developing_building_types_info:
            # compute target variables
            # compute target variables into developing_building_types_info dict
            developing_building_types_info[developing_building_type]['target_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']] = \
                int(round(total_and_occupied_variable_sums['occupied_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']] \
                          / (1 - developing_building_types_info[developing_building_type]['target_vacancy_rate'])))

            # compute difference variables
            # compute difference variables into developing_building_types_info dict
            developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']] = \
                developing_building_types_info[developing_building_type]['target_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']] - \
                    total_and_occupied_variable_sums['total_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']]

            # compute action variables
            # if the computed difference is  0 or negative (no demand for units of this type):
            if developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']] < 1:
                # consider whether to build the minimum units
                # check simulation year against maximum annual build year
                if build_minimum_units and developing_building_types_info[developing_building_type]['adm_minimum_annual_build_max_year'] >= simulation_year:
                    # build minimum
                    developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = \
                        developing_building_types_info[developing_building_type]['adm_minimum_annual_build_units']
                else:
                    #build nothing
                    developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = 0
            # the computed difference is positive (demand for units of this type)
            # decide how much to build, the actual number demanded, or the minimum
            else:
                # compute the difference * the percent_active_development
                diff_with_pct_active = int(developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']] * percent_active_development)
                # if the diff_with_pct_active is greater than the minimum development:
                if build_minimum_units and diff_with_pct_active > developing_building_types_info[developing_building_type]['adm_minimum_annual_build_units']:
                    # just build the diff_with_pct_active
                    developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = diff_with_pct_active
                # the pct_diff_with_pct_active < minimum build and the max year for annual build is appropriate:
                elif build_minimum_units and developing_building_types_info[developing_building_type]['adm_minimum_annual_build_max_year'] >= simulation_year:
                    # build the minimum
                    developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = \
                        developing_building_types_info[developing_building_type]['adm_minimum_annual_build_units']
                # last case is the demand < minimum, but the simulation year > max year:
                else:
                    # build the pct_diff_with_pct_active
                    developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = diff_with_pct_active

            # compute how much development is available in active developments
            # add this information to the developing_building_types_info dictionary:
            #     building_type_id:{'target_vacancy_rate':<float>,'building_type_name':<string>,'available_active_capacity_this_year':<integer>}
            indx = where(developments_dataset.get_attribute('building_type_id')[active_developments_index]==developing_building_type)
            developing_building_types_info[developing_building_type]['active_developments_capacity_this_year_index'] = indx
            developing_building_types_info[developing_building_type]['available_active_capacity_this_year'] = active_developments_capacity_this_year[indx].sum()

            # compute actual action to take
            action = developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']]
            available = developing_building_types_info[developing_building_type]['available_active_capacity_this_year']
            actual_action = self.lesser(action,available)
            # revise actual action if minimum build units is in effect:
            if build_minimum_units and developing_building_types_info[developing_building_type]['adm_minimum_annual_build_max_year'] >= simulation_year:
                actual_action = self.greater(actual_action,developing_building_types_info[developing_building_type]['adm_minimum_annual_build_units'])
            developing_building_types_info[developing_building_type]['action_to_take_this_year'] = actual_action

            # create status line for logging
            status_line = [#developing_building_type,
                           developing_building_types_info[developing_building_type]['building_type_name'],
                           total_and_occupied_variable_sums['occupied_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']],
                           total_and_occupied_variable_sums['total_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']],
                           round(1 - (total_and_occupied_variable_sums['occupied_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']] / \
                                total_and_occupied_variable_sums['total_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']] \
                                ),4),
                           developing_building_types_info[developing_building_type]['target_%s_units' % developing_building_types_info[developing_building_type]['building_type_name']],
                           developing_building_types_info[developing_building_type]['target_vacancy_rate'],
                           developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']],
                           developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']],
                           developing_building_types_info[developing_building_type]['available_active_capacity_this_year'],
                           actual_action
                           ]
            status_log.add_row(status_line)
        
        # print the status table to the log
        logger.log_status(status_log)

        # debug help
        if self.debuglevel > 0:
            self.debug_printer('developing_building_types_info', developing_building_types_info)

        # update the active_developments and buildings datasets with new units
        for developing_building_type in developing_building_types_info:
            if developing_building_types_info[developing_building_type]['action_to_take_this_year'] > 0:
                # update 'current_built_units' column in active_developments dataset

                # get the index of the records of the current developing_building_type
                indx = developing_building_types_info[developing_building_type]['active_developments_capacity_this_year_index']
                # get the total number of units to build this year
                total_action = developing_building_types_info[developing_building_type]['action_to_take_this_year']
                # compute the weight as build_out capacity - current_built_units
                buildout_capacity = developments_dataset.get_attribute('build_out_capacity')[active_developments_index][indx]
                current_built_units = developments_dataset.get_attribute('current_built_units')[active_developments_index][indx]
                weights = buildout_capacity - current_built_units
                weights_sum = float(weights.sum())
                weight_array = weights/weights_sum
                # distribute the total to build against the weight
                action_array = (total_action * weight_array).astype('int32')
                new_built_units = current_built_units + action_array
                # make sure we are not going to build more than the buildout_capacity
                check = buildout_capacity - new_built_units
                check_lt_zero = where(check<0)
                if check_lt_zero[0].size>0:
                    # We have a problem, set the new_built_units = the buildout_capacity
                    #  for those records where we are blowing the buildout of the development
                    new_built_units[check_lt_zero] = buildout_capacity[check_lt_zero]
                # update the current_built_units column with new values
                developments_building_ids = developments_dataset.get_attribute('building_id')
                building_ids_to_be_updated = developments_building_ids[active_developments_index][indx]
                if self.debuglevel > 0:
                    self.debug_printer('building_ids_to_be_updated', building_ids_to_be_updated)
                building_ids_to_be_updated_index_on_developments = in1d(developments_building_ids,building_ids_to_be_updated)
                developments_dataset.set_values_of_one_attribute('current_built_units',new_built_units,building_ids_to_be_updated_index_on_developments)
                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('new_built_units', new_built_units)

                # update the relevant units column on the buildings dataset with new units
                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('building_ids_to_be_updated', building_ids_to_be_updated)
                building_ids_to_be_updated_index_on_buildings = buildings_dataset.get_id_index(building_ids_to_be_updated)
                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('building_ids_to_be_updated_index_on_buildings', building_ids_to_be_updated_index_on_buildings)
                if developing_building_types_info[developing_building_type]['is_residential']:
                    buildings_dataset.set_values_of_one_attribute('residential_units',new_built_units,building_ids_to_be_updated_index_on_buildings)
                else:
                    buildings_dataset.set_values_of_one_attribute('non_residential_sqft',new_built_units,building_ids_to_be_updated_index_on_buildings)


    def debug_printer(self, name, item_to_print):
        self.debug.print_debug('\n*** BEGIN DEBUG INFO:', self.debuglevel)
        self.debug.print_debug('Printing: %s' % name, self.debuglevel)
        if isinstance(item_to_print, dict):
            try:
                from json import dumps
                self.debug.print_debug(dumps(item_to_print, indent=4), self.debuglevel)
            except:
                for key1,value1 in item_to_print.items():
                    self.debug.print_debug('primary dict key = %s' % key1, 1)
                    for key2,value2 in value1.items():
                        self.debug.print_debug('%s : %s' % (key2,value2), 1)
        else:
            self.debug.print_debug(item_to_print, self.debuglevel)
        self.debug.print_debug('END DEBUG INFO ***\n', self.debuglevel)


    def lesser(self,x,y):
        if x-y > 0:
            return y
        else:
            return x

    def greater(self,x,y):
        if x-y < 0:
            return y
        else:
            return x


from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import array

class ActiveDevelopmentsModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        # set up test data
        active_developments_data= {
                    'active_developments_id' : array([1,2,3,4]),
                    'building_id' : array([1,2,3,4]),
                    'start_year' : array([2010,2010,2010,2010]),
                    'building_type_id' : array([1,2,3,4]),
                    'build_out_capacity' : array([104,1052,10316,103211]),
                    'max_annual_capacity' : array([4,52,516,4211]),
                    'current_built_units' : array([100,1000,10000,99000]),
                                   }
        buildings_data = {
                    'building_id' : array([1,2,3,4]),
                    'building_type_id' : array([1,2,3,4]),
                    'residential_units' : array([100,1000,0,0]),
                    'residential_units_capacity' : array([104,1052,0,0]),
                    'non_residential_sqft' : array([0,0,10000,100000]),
                    'non_residential_sqft_capacity' : array([0,0,10316,103211]),
                    'total_rsf_units_col' : array([100.0,0,0,0]),
                    'occupied_rsf_units_col' : array([99.0,0,0,0]),
                    'total_rmf_units_col' : array([0,1000.0,0,0]),
                    'occupied_rmf_units_col' : array([0,999.0,0,0]),
                    'total_ret_units_col' : array([0,0,10000.0,0]),
                    'occupied_ret_units_col' : array([0,0,9800.0,0]),
                    'total_ind_units_col' : array([0,0,0,100000.0]),
                    'occupied_ind_units_col' : array([0,0,0,99000.0]),
                          }
        building_types_data = {
                    'building_type_id' : array([1,2,3,4]),
                    'building_type_name' : array(['rsf','rmf','ret','ind']),
                    'is_residential' : array([1,1,0,0]),
                    'is_developing' : array([1,1,1,1]),
                               }
        target_vacacy_data = {
                    'target_vacancy_id' : array([1,2,3,4]),
                    'year' : array([2010,2010,2010,2010]),
                    'target_vacancy' : array([0.05,0.05,0.05,0.05]),
                    'building_type_id' : array([1,2,3,4]),
                    'is_residential' : array([1,1,0,0]),
                              }
        
        # set up storage and a dataset pool
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'active_developments', table_data = active_developments_data)
        storage.write_table(table_name = 'buildings', table_data = buildings_data)
        storage.write_table(table_name = 'building_types', table_data = building_types_data)
        storage.write_table(table_name = 'target_vacancies', table_data = target_vacacy_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['opus_core'])
        self.buildings = self.dataset_pool.get_dataset('building')
        self.active_developments = self.dataset_pool.get_dataset('active_developments')

    def test_residential_building_types(self):
        # set up and run the model
        model = ActiveDevelopmentsModel(debuglevel=0)
        capacity_this_year = 'numpy.minimum((active_developments.build_out_capacity - active_developments.current_built_units),active_developments.max_annual_capacity)'
        model.run(year=2010, dataset_pool=self.dataset_pool, capacity_this_year_variable=capacity_this_year, build_minimum_units=False)
        
        # Check that the buildings dataset was updated properly
        buildings_result = self.buildings.get_attribute('residential_units')
        self.assertEqual(buildings_result[self.buildings.get_attribute('building_type_id')==1] == 104, True)
        self.assertEqual(buildings_result[self.buildings.get_attribute('building_type_id')==2] == 1052, True)
        
        # Check that the active_developments dataset was updated properly
        active_developments_result = self.active_developments.get_attribute('current_built_units')
        self.assertEqual(active_developments_result[self.active_developments.get_attribute('building_type_id')==1] == 104, True)
        self.assertEqual(active_developments_result[self.active_developments.get_attribute('building_type_id')==2] == 1052, True)
        
    def test_non_residential_types(self):
        # set up and run the model
        model = ActiveDevelopmentsModel(debuglevel=0)
        capacity_this_year = 'numpy.minimum((active_developments.build_out_capacity - active_developments.current_built_units),active_developments.max_annual_capacity)'
        model.run(year=2010, dataset_pool=self.dataset_pool, capacity_this_year_variable=capacity_this_year, build_minimum_units=False)
        
        # Check that the buildings dataset was updated properly       
        buildings_result = self.buildings.get_attribute('non_residential_sqft')
        print(buildings_result)
        self.assertEqual(buildings_result[self.buildings.get_attribute('building_type_id')==3] == 10316, True)
        self.assertEqual(buildings_result[self.buildings.get_attribute('building_type_id')==4] == 103211, True)        

        # Check that the active_developments dataset was updated properly
        active_developments_result = self.active_developments.get_attribute('current_built_units')
        self.assertEqual(active_developments_result[self.active_developments.get_attribute('building_type_id')==3] == 10316, True)
        self.assertEqual(active_developments_result[self.active_developments.get_attribute('building_type_id')==4] == 103211, True)


if __name__=="__main__":
    opus_unittest.main()
