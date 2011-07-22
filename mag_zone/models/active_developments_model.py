# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset, DatasetSubset
from numpy import where, minimum, array, in1d
from prettytable import PrettyTable
from opus_core.misc import DebugPrinter


class ActiveDevelopmentsModel(Model):
    """
    Note: do not use yet, code still in progress
    """

    model_name = "Active Developments Model"
    model_short_name = "ADM"

    def __init__(self, debuglevel=1):
        self.debug = DebugPrinter(debuglevel)
        self.debuglevel = debuglevel

    def run(self, percent_active_development=100, year=None):
        # General TODO:
        #    - deal with target_vacancies table with subarea_ids in it
        #        - do i need to worry about it if this column is present?
        #    - create unit tests
        #    - test with non-residential development
        #    - test ADM with other zone models
        #    - test ADM with developments that began prior to the base_year
        #    - deal with redevelopment here at all?

        # LIST OF MODEL ASSUMPTIONS:
        #    - TODO: can i generalize the need for these pre-defined variables?
        #    - the model expects variables to exist that correspond to this naming pattern
        #      for every is_developing building_type_name in the building_types dataset:
        #        - total_<building_type_name>_units_col
        #        - occupied_<building_type_name>_units_col
        #    - building_type_name must be unique, lowercase, contain no spaces
        #    - target_vacancy.is_developing defines which building_types are considered

        # CURRENT LIST OF KNOWN ISSUES:
        #    - 


        # Get current simulation year
        if year is None:
            simulation_year = SimulationState().get_current_time()

        # Get the percent_active_development
        # convert it to a float
        percent_active_development = percent_active_development / 100.0

        # Get the dataset pool
        dataset_pool = SessionConfiguration().get_dataset_pool()

        # get the active_developments dataset, subset it for actually active projects
        # compute some variables
        developments_dataset = dataset_pool.get_dataset('active_developments')
        active_developments_capacity = developments_dataset.compute_variables(['mag_zone.active_development.capacity_this_year'])
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
        developing_building_type_ids = target_vacancies_for_this_year.get_attribute('building_type_id')
        target_vacancy_rates = target_vacancies_for_this_year.get_attribute('target_vacancy')

        # build a dictionary containing building_type_id:{'target_vacancy_rate':<float>}
        developing_building_types_info = {}
        counter = 0
        for developing_building_type in developing_building_type_ids:
            developing_building_types_info[developing_building_type] = {'target_vacancy_rate':target_vacancy_rates[counter]}
            counter += 1
        # debug help
        if self.debuglevel > 0:
            self.debug_printer('developing_building_types_info', developing_building_types_info)

        # get the building_types dataset
        building_types_dataset = dataset_pool.get_dataset('building_type')
        # get the attribute names
        # I don't think this next line is used at all:
        #building_types_dataset_attribute_names = building_types_dataset.get_attribute_names()

        # get only the developing building types
        developing_types_index = where(building_types_dataset.get_attribute('is_developing_type')==1)[0]
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
                logger.log_warning('There is a mismatch in the building_type_ids between those in the target_vacancies dataset and the developing types in the building_types dataset.')
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


        # build a list of total and occupied units variables to compute of the form
        #     ['occupied_rsf_units_col','total_rsf_units_col', ...]
        # The variables that this section creates and computes need to be defined in the buildings
        #     dataset aliases.py file
        building_variables = []
        for building_type_id,dict_of_info in developing_building_types_info.iteritems():
            total, occupied = 'total_%s_units_col' % dict_of_info['building_type_name'], 'occupied_%s_units_col' % dict_of_info['building_type_name']
            building_variables.append(total)
            building_variables.append(occupied)
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
        status_log.set_field_names(["Type",
                                    "Name",
                                    "Occ Units",
                                    "Tot Units",
                                    "Cur Vac Rate",
                                    "Target Units",
                                    "Target Vac Rate",
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
            # TODO: do i need to create 1 additional unit where the type is residential?
            if developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']] < 1:
                #build nothing
                developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = 0
            else:
                #build the difference * the percent_active_development
                developing_building_types_info[developing_building_type]['%s_action' % developing_building_types_info[developing_building_type]['building_type_name']] = \
                    int(developing_building_types_info[developing_building_type]['%s_diff' % developing_building_types_info[developing_building_type]['building_type_name']] * percent_active_development)

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
            developing_building_types_info[developing_building_type]['action_to_take_this_year'] = actual_action

            # create status line for logging
            status_line = [developing_building_type,
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
                print 'current_built_units'
                print current_built_units
                print 'action_array'
                print action_array
                new_built_units = current_built_units + action_array
                # update the current_built_units column with new values
                developments_building_ids = developments_dataset.get_attribute('building_id')
                building_ids_to_be_updated = developments_building_ids[active_developments_index][indx]
                if self.debuglevel > 0:
                    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                    self.debug_printer('building_ids_to_be_updated', building_ids_to_be_updated)
                    print building_ids_to_be_updated.size
                building_ids_to_be_updated_index_on_developments = in1d(developments_building_ids,building_ids_to_be_updated)
                developments_dataset.set_values_of_one_attribute('current_built_units',new_built_units,building_ids_to_be_updated_index_on_developments)

                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('new_built_units', new_built_units)
                    print new_built_units.size
                    print new_built_units.sum()


                # update the relevant units column on the buildings dataset with new units
                #building_ids = buildings_dataset.get_attribute('building_id')
                #building_ids_to_be_updated = building_ids[active_developments_index][indx]
                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('building_ids_to_be_updated', building_ids_to_be_updated)
                    print building_ids_to_be_updated.size

                #TRY THIS from add_projects_to_buildings_model
                #building_index = where(building_identifier==this_identifier)[0]
                #MY OLD LINE:
                #building_ids_to_be_updated_index_on_buildings = in1d(building_ids,building_ids_to_be_updated)
                #MY NEW LINE:
                building_ids_to_be_updated_index_on_buildings = buildings_dataset.get_id_index(building_ids_to_be_updated)
                # debug help
                if self.debuglevel > 0:
                    self.debug_printer('building_ids_to_be_updated_index_on_buildings', building_ids_to_be_updated_index_on_buildings)
                    #print "THis many are TRUE: %s" % building_ids_to_be_updated_index_on_buildings.tolist().count(True)
                    print "building_ids_to_be_updated_index_on_buildings.size = %s" % building_ids_to_be_updated_index_on_buildings.size 
                if developing_building_types_info[developing_building_type]['is_residential']:
                    buildings_dataset.set_values_of_one_attribute('residential_units',new_built_units,building_ids_to_be_updated_index_on_buildings)
                else:
                    buildings_dataset.set_values_of_one_attribute('non_residential_sqft',new_built_units,building_ids_to_be_updated_index_on_buildings)

        #dataset_pool.flush_loaded_datasets()


    def debug_printer(self, name, item_to_print):
        self.debug.print_debug('\n*** BEGIN DEBUG INFO:', self.debuglevel)
        self.debug.print_debug('Printing: %s' % name, self.debuglevel)
        if isinstance(item_to_print, dict):
            try:
                from json import dumps
                self.debug.print_debug(dumps(item_to_print, indent=4), self.debuglevel)
            except:
                for key1,value1 in item_to_print.iteritems():
                    self.debug.print_debug('primary dict key = %s' % key1, 1)
                    for key2,value2 in value1.iteritems():
                        self.debug.print_debug('%s : %s' % (key2,value2), 1)
        else:
            self.debug.print_debug(item_to_print, self.debuglevel)
        self.debug.print_debug('END DEBUG INFO ***\n', self.debuglevel)


    def lesser(self,x,y):
        if x-y > 0:
            return y
        else:
            return x



from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from numpy import array

class ActiveDevelopmentsModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        active_developments_data= {
                    'active_development_id' : array([1,2]),
                    'building_id' : array([1,2]),
                    'start_year' : array([]),
                    'building_type_id' : array([]),
                    'build_out_capacity' : array([]),
                    'max_annual_capacity' : array([]),
                    'current_built_units' : array([]),
                    'other_spaces_name' : array([]),
                    'other_spaces' : array([]),
                                   }
        buildings_data = {
                    'building_id' : array([1,2]),
                    '' : array([]),
                    '' : array([]),
                          }
        building_types_data = {
                    'building_type_id' : array([1,2]),
                    'building_type_name' : array(['rsf','rmf']),
                    'is_residential' : array([1,1]),
                               }
        target_vacacy_data = {
                    'year' : array([2010,2010]),
                    'target_vacancy' : array([0.05,0.05]),
                    'building_type_id' : array([1,2]),
                    'is_residential' : array([1,1]),
                              }

        storage = StorageFactory().get_storage('dict_storage')

    def test_one_test(self):
        print ''

if __name__=="__main__":
    opus_unittest.main()
