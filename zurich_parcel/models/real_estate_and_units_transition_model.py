# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset, DatasetSubset
from numpy import array, where, ones, logical_and, logical_not
from numpy import arange, concatenate, resize, int32, searchsorted, cumsum
from opus_core.models.model import Model
from opus_core.logger import logger, log_block
from opus_core.sampling_toolbox import sample_replace
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from opus_core.misc import ismember
import re

try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
except:
    PrettyTable = None



class RealEstateTransitionModel(Model):
    """
    """
    
    model_name = "Real Estate and Units Transition Model"
    model_short_name = "RETM"
    
    def __init__(self, target_vancy_dataset=None, model_name=None, model_short_name=None,
                 control_totals=None, employment_control_totals=None, building_sqft_per_job=None, sectors=None):
        self.target_vancy_dataset = target_vancy_dataset
        self.control_totals = control_totals
        self.employment_control_totals = employment_control_totals
        self.building_sqft_per_job = building_sqft_per_job
        self.sectors = sectors
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
        
#        import pydevd;
#        pydevd.settrace()
        
    def run(self, realestate_dataset,
            living_units_dataset,
            year=None, 
            occupied_spaces_variable="occupied_units",
            total_spaces_variable="total_units",
            target_attribute_name='target_vacancy_rate',
            sample_from_dataset = None,
            living_units_from_dataset = None,
            sample_filter="",
            reset_attribute_value={}, 
            year_built = 'year_built',
            dataset_pool=None,
            append_to_realestate_dataset = False,
            table_name = "development_projects",
            dataset_name = "development_project",
            id_name = 'development_project_id',
            **kwargs):
        """         
        sample_filter attribute/variable indicates which records in the dataset are eligible in the sampling for removal or cloning
        append_to_realestate_dataset - whether to append the new dataset to realestate_dataset
        """
        
        if self.target_vancy_dataset is None:
            raise RuntimeError, "target_vacancy_rate dataset is unspecified."
        
        if not sample_from_dataset or not living_units_from_dataset:
            logger.log_note('No development projects or no living units of development projects to sample from. Development projects are taken from building dataset and thus living units from living_units dataset.')
            sample_from_dataset = realestate_dataset
            living_units_from_dataset = living_units_dataset
            
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()
        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = where(self.target_vancy_dataset.get_attribute('year')==year)[0]
        target_vacancy_for_this_year = DatasetSubset(self.target_vancy_dataset, this_year_index)
        
        column_names = list(set( self.target_vancy_dataset.get_known_attribute_names() ) - set( [ target_attribute_name, occupied_spaces_variable, total_spaces_variable, 'year', '_hidden_id_'] ))
        column_names.sort(reverse=True)
        column_values = dict([ (name, target_vacancy_for_this_year.get_attribute(name)) for name in column_names + [target_attribute_name]])
        
        
        independent_variables = list(set([re.sub('_max$', '', re.sub('_min$', '', col)) for col in column_names]))
        sample_dataset_known_attributes = sample_from_dataset.get_known_attribute_names()
        for attribute in independent_variables:
            if attribute not in sample_dataset_known_attributes:
                sample_from_dataset.compute_one_variable_with_unknown_package(attribute, dataset_pool=dataset_pool)
        sample_dataset_known_attributes = sample_from_dataset.get_known_attribute_names() #update after compute
                
        if sample_filter:
            short_name = VariableName(sample_filter).get_alias()
            if short_name not in sample_dataset_known_attributes:
                filter_indicator = sample_from_dataset.compute_variables(sample_filter, dataset_pool=dataset_pool)
            else:
                filter_indicator = sample_from_dataset.get_attribute(short_name)
        else:
            filter_indicator = 1
                
        sampled_index = array([], dtype=int32)

        #log header
        if PrettyTable is not None:
            status_log = PrettyTable()
            status_log.set_field_names(column_names + ["actual", "target", "expected", "difference", "action"])
        else:
            logger.log_status("\t".join(column_names + ["actual", "target", "expected", "difference", "action"]))
        error_log = ''
        for index in range(target_vacancy_for_this_year.size()):
            sample_indicator = ones( sample_from_dataset.size(), dtype='bool' )
            criterion = {}   # for logging
            for attribute in independent_variables:
                if attribute in sample_dataset_known_attributes:
                    sample_attribute = sample_from_dataset.get_attribute(attribute)
                else:
                    raise ValueError, "attribute %s used in target vacancy dataset can not be found in dataset %s" % (attribute, realestate_dataset.get_dataset_name())
                
                if attribute + '_min' in column_names:
                    amin = target_vacancy_for_this_year.get_attribute(attribute+'_min')[index] 
                    criterion.update({attribute + '_min':amin})
                    if amin != -1:
                        sample_indicator *= sample_attribute >= amin
                if attribute + '_max' in column_names: 
                    amax = target_vacancy_for_this_year.get_attribute(attribute+'_max')[index]
                    criterion.update({attribute + '_max':amax}) 
                    if amax != -1:
                        sample_indicator *= sample_attribute <= amax
                if attribute in column_names: 
                    aval = column_values[attribute][index] 
                    criterion.update({attribute:aval}) 
                    if aval == -1:
                        continue
                    elif aval == -2:  ##treat -2 in control totals column as complement set, i.e. all other values not already specified in this column
                        sample_indicator *= logical_not(ismember(sample_attribute, column_values[attribute]))
                    else:
                        sample_indicator *= sample_attribute == aval
                        
            this_total_spaces_variable, this_occupied_spaces_variable = total_spaces_variable, occupied_spaces_variable
            ## total/occupied_spaces_variable can be specified either as a universal name for all realestate 
            ## or in targe_vacancy_rate dataset for each vacancy category
            if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_occupied_spaces_variable = target_vacancy_for_this_year.get_attribute(occupied_spaces_variable)[index]

            if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_total_spaces_variable = target_vacancy_for_this_year.get_attribute(total_spaces_variable)[index]
            
            this_total_spaces_variable += '_' + str(criterion[col])
            this_occupied_spaces_variable += '_' + str(criterion[col])
            
            logger.be_quiet() #temporarily disable logging
            realestate_dataset.compute_one_variable_with_unknown_package(this_occupied_spaces_variable, dataset_pool=dataset_pool)
            realestate_dataset.compute_one_variable_with_unknown_package(this_total_spaces_variable, dataset_pool=dataset_pool)
            sample_from_dataset.compute_one_variable_with_unknown_package(this_total_spaces_variable, dataset_pool=dataset_pool)
            logger.talk()
            
            actual_num = (realestate_dataset.get_attribute(this_total_spaces_variable)).sum()
            #target_num is obsolete with this version.
            target_num = int(round( (realestate_dataset.get_attribute(this_occupied_spaces_variable)).sum() /\
                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index])))
            '''If the target vacancy is very small and the inflow to the region big it is not enough to check
            only the current simulation year's vacancy. The simulation is more robust if the BTM is anticipating the
            next year's population (of households and jobs).
            This version calculates the non residential spaces based on sqft requirements of jobs per sector. 
            #TODO: Make code more general to cover various stratifications in the real estate market.
            '''
            if criterion[col] == 0:
                """ Option without demography model
                idx = where(self.control_totals.get_attribute("year")==year + 1)[0]
                this_years_control_totals = DatasetSubset(self.control_totals, idx)
                expected_num = int(round( this_years_control_totals.get_attribute('total_number_of_households').sum() /\
                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index])))""" 
                hh_dataset = dataset_pool.get_dataset( 'household' )
                number_of_hh = hh_dataset.size()
                expected_num = int(round( number_of_hh /\
                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index]))) 
            if criterion[col] > 0:
                # Getting control totals per sector in a dictionary
                idx = where(self.employment_control_totals.get_attribute("year")==year)[0] # Create index to get the subset of control totals for the next simulation year.
                this_years_control_totals = DatasetSubset(self.employment_control_totals, idx) # Create the subset of control totals.
                idx_non_home_based = where(logical_and(this_years_control_totals['home_based_status'] == 0,this_years_control_totals['sector_id'] == criterion[col]))[0] # Create index of non home based control totals in current sector. Only non home based jobs are supported. TODO: Support home based jobs.
                this_years_control_totals = DatasetSubset(this_years_control_totals, idx_non_home_based)
#                idx_current_sector = where(this_years_control_totals['sector_id'] == criterion[col])[0]
                next_years_jobs = this_years_control_totals['number_of_jobs']
                controled_sectors = this_years_control_totals['sector_id']                
                sector_job_totals = dict(zip(controled_sectors, next_years_jobs.T)) # creating dictionary with sector id's as key and number of jobs as values to ensure multiplication with right requiremtents.

                # Getting infos on required sqft per sector. 
#                a_zone_id = min(self.building_sqft_per_job['zone_id']) # Get a zone number from the definition table. Here choose to take the minimum which is arbitrary. This code assumes constant sqft requirements in all zones. TODO: Support different sqft requirements per zone.
#                idx_zone = where(self.building_sqft_per_job['zone_id'] == a_zone_id)[0]
#                subset_sqft_per_job = DatasetSubset(self.building_sqft_per_job, idx_zone)
#                sqft_per_job = subset_sqft_per_job['building_sqft_per_job']
#                sectors_with_requirements = subset_sqft_per_job['sector_id']
#                requirements_by_sector = dict(zip(sectors_with_requirements, sqft_per_job.T))
#                
#                needed_sqft_over_all_sectors = sector_job_totals[criterion[col]] * requirements_by_sector[criterion[col]]
#                expected_num = int(round( needed_sqft_over_all_sectors /\
#                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index])))
                
                idx_sector = where(self.sectors['sector_id'] == criterion[col])
                subset_sqft_per_job_sector = DatasetSubset(self.sectors, idx_sector)
                needed_sqft_current_sector = sector_job_totals[criterion[col]] * subset_sqft_per_job_sector.get_attribute('sqm_per_job')
                expected_num = int(round( needed_sqft_current_sector /\
                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index])))

            diff = expected_num - actual_num
            
            #Previous version which is checking the current years occupation.
            #diff = target_num - actual_num
            
            this_sampled_index = array([], dtype=int32)
            if diff > 0:
                total_spaces_in_sample_dataset = sample_from_dataset.get_attribute(this_total_spaces_variable)
                legit_index = where(logical_and(sample_indicator, filter_indicator) * total_spaces_in_sample_dataset > 0)[0]
                if legit_index.size > 0:
                    mean_size = total_spaces_in_sample_dataset[legit_index].mean()
                    num_of_projects_to_sample = int( diff / mean_size )
                    ##sampled at least 1 project when diff > 0, otherwise it is a endless loop when num_of_projects_to_sample = 0
                    num_of_projects_to_sample = num_of_projects_to_sample if num_of_projects_to_sample > 0 else 1
                    while total_spaces_in_sample_dataset[this_sampled_index].sum() < diff:
                        lucky_index = sample_replace(legit_index, num_of_projects_to_sample)
                        this_sampled_index = concatenate((this_sampled_index, lucky_index))
                    this_sampled_index = this_sampled_index[0:(1+searchsorted(cumsum(total_spaces_in_sample_dataset[this_sampled_index]), diff))]
                    sampled_index = concatenate((sampled_index, this_sampled_index))
                else:
                    error_log += "There is nothing to sample from %s and no new development will happen for " % sample_from_dataset.get_dataset_name() + \
                              ','.join([col+"="+str(criterion[col]) for col in column_names]) + '\n'
            #if diff < 0: #TODO demolition; not yet supported
            
            ##log status
            action = "0"
            if this_sampled_index.size > 0:
                action_num = total_spaces_in_sample_dataset[this_sampled_index].sum()
                if diff > 0: action = "+" + str(action_num)
                if diff < 0: action = "-" + str(action_num)
            cat = [ str(criterion[col]) for col in column_names]
            cat += [str(actual_num), str(target_num), str(expected_num), str(diff), action]
            
            if PrettyTable is not None:
                status_log.add_row(cat)
            else:                
                logger.log_status("\t".join(cat))
            
        if PrettyTable is not None:
            logger.log_status("\n" + status_log.get_string())
        if error_log:
            logger.log_error(error_log)
        
        
        #logger.log_note("Updating attributes of %s sampled development events." % sampled_index.size)
        result_data = {}
        result_dataset = None
        index = array([], dtype='int32')
        if sampled_index.size > 0:
            ### ideally duplicate_rows() is all needed to add newly cloned rows
            ### to be more cautious, copy the data to be cloned, remove elements, then append the cloned data
            ##realestate_dataset.duplicate_rows(sampled_index)
            #result_data.setdefault(year_built, resize(year, sampled_index.size).astype('int32')) # Reset the year_built attribute. Uncommented because it is overwritten in the for loop afterwards.
            ## also add 'independent_variables' to the new dataset
            for attribute in set(sample_from_dataset.get_primary_attribute_names() + independent_variables):
                if reset_attribute_value.has_key(attribute):
                    result_data[attribute] = resize(array(reset_attribute_value[attribute]), sampled_index.size)
                else:
                    result_data[attribute] = sample_from_dataset.get_attribute_by_index(attribute, sampled_index)
            # Reset the year_built attribute.
            result_data['year_built'] = resize(year, sampled_index.size).astype('int32')
            # TODO: Uncomment the following three lines to reset land_area, tax_exempt, zgde. Test still to be done. parcel_id should be changed by location choice model.
            #result_data['land_area'] = resize(-1, sampled_index.size).astype('int32')
            #result_data['tax_exempt'] = resize(-1, sampled_index.size).astype('int32')
            #result_data['zgde'] = resize(-1, sampled_index.size).astype('int32')
            
            if id_name and result_data and id_name not in result_data:
                result_data[id_name] = arange(sampled_index.size, dtype='int32') + 1
            storage = StorageFactory().get_storage('dict_storage')
            storage.write_table(table_name=table_name, table_data=result_data)
            
            result_dataset = Dataset(id_name = id_name,
                                      in_storage = storage,
                                      in_table_name = table_name,
                                      dataset_name = dataset_name
                                      )
            index = arange(result_dataset.size())

        if append_to_realestate_dataset:
            if len(result_data) > 0:
                logger.start_block('Appending development events and living units')
                logger.log_note("Append %d sampled development events to real estate dataset." % len(result_data[result_data.keys()[0]]))
                index = realestate_dataset.add_elements(result_data, require_all_attributes=False,
                                                        change_ids_if_not_unique=True)
                logger.start_block('Creating id mapping')
                # remember the ids from the development_event_history dataset.
                mapping_new_old = self.get_mapping_of_old_ids_to_new_ids(result_data, realestate_dataset, index)
                logger.end_block()
                
                '''Getting living units associated to selected development events by iterating over the mapping dictionary and 
                selecting each time all the living units according to the old building ids.
                The living units are then added to selected_living_units_dict which is then
                added to living_units dataset. A dictionary is needed to use the add_elements method.
                Creating a dictionary also clones the records. The subset is only a view on the original table.'''
                selected_living_units_dict = {}
                counter = 0
                for new_id in mapping_new_old:
                    if counter == 0:
                        logger.log_note("Log assignment of every 100th development event")
                    counter +=1
                    if counter % 100 == 0:
                        logger.log_note("Assembling living units for development event %s" % new_id)
                    sel_index = [i for i in range(0, len(living_units_from_dataset['building_id'])) if living_units_from_dataset['building_id'][i] == mapping_new_old[new_id]]
                    living_units_this_sampled_building = DatasetSubset(living_units_from_dataset, sel_index) 
                    if len(selected_living_units_dict) == 0:
                        logger.start_block('Assign new building id')
                        for attribute_name in living_units_this_sampled_building.get_primary_attribute_names():
                            column = living_units_this_sampled_building.get_attribute(attribute_name)
                            if attribute_name == 'building_id':
                                new_ids = array(living_units_this_sampled_building.size() * [new_id], dtype=int32)
                                selected_living_units_dict.update({attribute_name: new_ids})
                            else:
                                selected_living_units_dict.update({attribute_name: column})
                        logger.end_block()
                    else:
                        this_living_units_dict ={}
                        for attribute_name in living_units_this_sampled_building.get_primary_attribute_names():
                            column = living_units_this_sampled_building.get_attribute(attribute_name)
                            if attribute_name == 'building_id':
                                new_ids = array(living_units_this_sampled_building.size() * [new_id], dtype=int32)
                                this_living_units_dict.update({attribute_name: new_ids})
                            else:
                                this_living_units_dict.update({attribute_name: column})
                        for attribute_name in living_units_this_sampled_building.get_primary_attribute_names():
                            selected_living_units_dict[attribute_name] = concatenate([selected_living_units_dict[attribute_name], this_living_units_dict[attribute_name]])
                # Reset year_built attribute of living units
                selected_living_units_dict['year_built'] = resize(year, len(selected_living_units_dict['year_built'])).astype('int32')
                # TODO: Uncomment the following two lines to reset rent_price, zgde. Test still to be done
                # selected_living_units_dict['rent_price'] = resize(-1, len(selected_living_units_dict['rent_price'])).astype('int32')
                # selected_living_units_dict['zgde'] = resize(-1, len(selected_living_units_dict['zgde'])).astype('int32')


                
                index_units = living_units_dataset.add_elements(selected_living_units_dict, require_all_attributes=False,
                                                        change_ids_if_not_unique=True)
                
                # Check consistency of buildings and living units. All living units must belong to a building
                if SimulationState().get_current_time() - SimulationState().get_start_time() == 1:
                    for building_id in living_units_dataset['building_id']:
                        if building_id not in realestate_dataset['building_id']:
                            logger.log_warning('Living unit with building_id %d has no corresponding building.' % (building_id))
                        # Uncomment next line to enforce consistency of living units and building dataset. Then you may uncomment the two previous lines.
#                        assert(building_id in realestate_dataset['building_id']), 'Living unit with building_id %d has no corresponding building.' % (building_id)

            result_dataset = realestate_dataset
        logger.end_block()

        # It is recommended to derive all variables of buildings in relation to living units via expression variables.
        # However, if the building dataset contains attributes derived from living units these attributes should be consistent
        # with the living units table. Below an example.
        # Residential_units attribute of each building should be consistent with the number of living units associated.
#        self.check_consistency_of_living_units_per_building(realestate_dataset, living_units_dataset, mapping_new_old)

        return (result_dataset, index)
    
    def get_number_of_associated_living_units(self, building_id, living_units_dataset):
        return list(living_units_dataset['building_id']).count(building_id)
    
    def get_mapping_of_old_ids_to_new_ids(self, old_dict, new_dataset, new_index):
        old_ids = old_dict['building_id']
        # get_new_ids_of_added_buildings
        new_buildings_with_new_ids = DatasetSubset(new_dataset, new_index)
        new_ids = new_buildings_with_new_ids['building_id']
        new_ids_to_old_ids_mapping = dict(zip(new_ids, old_ids))
        return new_ids_to_old_ids_mapping
    
    def check_consistency_of_living_units_per_building(self, realestate_dataset, living_units_dataset, mapping_new_old):
        for building_id in realestate_dataset['building_id']:
            if not self.get_number_of_associated_living_units(building_id, living_units_dataset) == realestate_dataset.get_attribute_by_id('residential_units', building_id):
                residential_units = self.get_number_of_associated_living_units(building_id, living_units_dataset)
                if realestate_dataset.id_mapping_type == 'D':
                    realestate_dataset.set_value_of_attribute_by_id('residential_units', residential_units, building_id)
                else:
                    realestate_dataset.set_value_of_attribute_by_id('residential_units', residential_units, realestate_dataset._get_one_id_index(building_id))
                if building_id in mapping_new_old:
                    logger.log_warning('Attribute residential_units of the development_event_history record with building_id %d had to be reset.' % (mapping_new_old[building_id]))
                else:
                    logger.log_warning('Attribute residential_units of building record with building_id %d had to be reset.' % (building_id))
        assert(self.get_number_of_associated_living_units(building_id, living_units_dataset) == realestate_dataset.get_attribute_by_id('residential_units', building_id))


    def prepare_for_run(self, dataset_name=None, table_name=None, storage=None):
        '''Load target vacancies table.'''
        if (storage is None) or ((table_name is None) and (dataset_name is None)):
            dataset_pool = SessionConfiguration().get_dataset_pool()
            dataset = dataset_pool.get_dataset( 'target_vacancy' )
            return dataset
        
        if not dataset_name:
            dataset_name = DatasetFactory().dataset_name_for_table(table_name)
        
        dataset = DatasetFactory().search_for_dataset(dataset_name,
                                                      package_order=SessionConfiguration().package_order,
                                                      arguments={'in_storage':storage, 
                                                                 'in_table_name':table_name,
                                                                 'id_name':[]
                                                                 }
                                                      )
        if self.target_vancy_dataset is None:
            self.target_vancy_dataset = dataset
        
        '''Load household control totals table. Purpose: Anticipation of next year's household number.
        '''
#        control_totals_dataset = DatasetFactory().search_for_dataset('control_totals',
#                                                      package_order=SessionConfiguration().package_order,
#                                                      arguments={'in_storage':storage, 
#                                                                 'in_table_name':'annual_household_control_totals',
#                                                                 'id_name':[]
#                                                                 }
#                                                      )
#        
#        if self.control_totals is None:
#            self.control_totals = control_totals_dataset
            
        '''Load employment control totals table and building_sqft_per_job table. Purpose: Anticipation of next year's employment number.
        '''
        employment_control_totals_dataset = DatasetFactory().search_for_dataset('control_totals',
                                                      package_order=SessionConfiguration().package_order,
                                                      arguments={'in_storage':storage, 
                                                                 'in_table_name':'annual_employment_control_totals',
                                                                 'id_name':[]
                                                                 }
                                                      )
        
        if self.employment_control_totals is None:
            self.employment_control_totals = employment_control_totals_dataset
            
        building_sqft_per_job = DatasetFactory().search_for_dataset('control_totals',
                                                      package_order=SessionConfiguration().package_order,
                                                      arguments={'in_storage':storage, 
                                                                 'in_table_name':'building_sqft_per_job',
                                                                 'id_name':[]
                                                                 }
                                                      )
        if self.building_sqft_per_job is None:
            self.building_sqft_per_job = building_sqft_per_job
            
        sectors = DatasetFactory().search_for_dataset('control_totals',
                                                      package_order=SessionConfiguration().package_order,
                                                      arguments={'in_storage':storage, 
                                                                 'in_table_name':'sectors',
                                                                 'id_name':[]
                                                                 }
                                                      )
        if self.sectors is None:
            self.sectors = sectors     
#        sectors = dataset_pool.get_dataset("sector")
#        name_equals_sector = sectors.get_attribute("name") == self.sector
#        name_equals_sector_indexes = where(name_equals_sector)
#        assert(len(name_equals_sector_indexes) == 1)
#        name_equals_sector_index = name_equals_sector_indexes[0]
#        sector_ids = sectors.get_attribute("sector_id")
#        sector_id = sector_ids[name_equals_sector_index][0]
                
        return dataset
        
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function, like synchronizing persons with households table
        """
        pass

#from opus_core.tests import opus_unittest
#from opus_core.datasets.dataset_pool import DatasetPool
#from opus_core.tests.stochastic_test_case import StochasticTestCase
#from opus_core.simulation_state import SimulationState
#from urbansim.building.aliases import aliases
#from opus_core.resources import Resources
#
#aliases += [
#            "occupied_sqft = numpy.clip(building.number_of_agents(job) * building.disaggregate(building_sqft_per_job.building_sqft_per_job), 0, building.non_residential_sqft)",
#            "number_of_households = building.number_of_agents(household)",
#            ]
#
#class RETMTests(StochasticTestCase):
#
#    def setUp( self ):
#        SimulationState().set_current_time(2000)
#        self.storage = StorageFactory().get_storage('dict_storage')
#
#        self.storage.write_table(
#            table_name='development_event_history',
#            table_data={
#                "building_id":          array([1 ,2, 3, 4]),
#                "zone_id":              array([1 ,2, 2, 2]),
#                "building_type_id":     array([1 ,2, 2, 1]),
#                "residential_units":    array([2 ,5, 3, 0]),
#                "non_residential_sqft": array([50,30,0, 50]),
#                "year_built":           array([2021, 2022, 2030, 2031]),
#                }
#            )
#        
#        self.storage.write_table(
#            table_name='living_units_history',
#            table_data={
#                'living_unit_id': array([211, 212, 221, 222, 223, 224, 225, 301, 302, 303]),
#                'building_id': array(2*[1] + 5*[2] + 3*[3]),
#                'year_built': array(2*[2021] + 5*[2022] + 3*[2030]),
#                'area': array(10*[60]),
#                'stories': array(10*[1]),
#                'rooms': array(10*[3]),
#                        }
#            )
#        
#        self.storage.write_table(
#            table_name='zones',
#            table_data={
#                "zone_id": arange( 1, 2+1),
#                }
#            )
#        
#        self.storage.write_table(
#            table_name='buildings',
#            table_data={
#                "building_id": array([1,2]), # 1 building per zone. each building is mixed in use
#                "zone_id": array( [1, 2] ),
#                "building_type_id": array([1,2]),
#                "residential_units": array([3, 7]),
#                "non_residential_sqft": array([150,50]),
#                "year_built": array(2*[1999]),
#                }
#            )
#        # Creating 10 living units. According to buildings table 3 units in building 1, 7 units in building 2. Year built is equal to the one of the building. Area, rooms and stories are dummies. 
#        self.storage.write_table(
#            table_name='living_units',
#            table_data={
#                'living_unit_id': arange(1, 10+1),
#                'building_id': array(3*[1] + 7*[2]),
#                'year_built': array(10*[1999]),
#                'area': array(10*[60]),
#                'stories': array(10*[1]),
#                'rooms': array(10*[3]),
#                        }
#            )
#
#        self.storage.write_table(
#            table_name='building_types',
#            table_data={
#                "building_type_id": arange(1,2+1),
#                "building_type_name": array(['commercial', 'residential']),
#                "is_residential": array([0,1]),
#                }
#            )
#
#
#        self.storage.write_table(
#            table_name='households',
#            table_data={
#                "household_id":arange( 1, 8+1),
#                "building_id": array(2*[1]+6*[2]),
#                }
#            )
#
#        self.storage.write_table(
#            table_name='jobs',
#            table_data={
#                "job_id":arange( 1, 11+1 ),
#                "building_id":  array(8*[1]       + 3*[2]      ),
#                "home_based":   array(11*[0]                   ),
#                "sector_id":    array(5*[2]+3*[1] + 1*[2]+2*[1]),
#                }
#            )
#        self.storage.write_table(
#            table_name = "building_sqft_per_job",
#            table_data = {
#                   "sector_id":           array([1 ,2 ,1 ,2 ]),
#                   "zone_id":              array([1 ,1 ,2 ,2 ]),
#                   "building_sqft_per_job":array([10,20,10,20]),
#            }
#        )  
#        self.storage.write_table(
#            table_name='annual_household_control_totals',
#            table_data={
#                    "annual_household_control_totals_id": arange(1, 5),
#                    "year":                       arange(2000, 2003+1),
#                    "total_number_of_households": array([8, 10, 12, 14]),
#            }
#        )
#        self.storage.write_table(
#            table_name='annual_employment_control_totals',
#            table_data={
#                        "annual_employment_control_totals_id": arange(0, 16),
#                        "home_based_status": array(8*[0] + 8*[1]),
#                        "number_of_jobs":    array([5,6] + [6,7] + [7,8] + [8,9] + 8*[0]),
#                        "sector_id":         array(2*(4*[1,2])),
#                        "year":              array(2*(2*[2000] + 2*[2001] + 2*[2002] + 2*[2003])),
#            }
#        )
#        self.dataset_pool = DatasetPool(package_order=['zurich_parcel', 'urbansim_parcel', "urbansim", "opus_core"],
#                                        storage=self.storage)
#
#        self.compute_resources = Resources({})
#        print "Setup finished."
#        
#    def test_transition_with_anticipation( self ):
#        """ Residential vacancy in zone 1 = 0.33333
#            Residential vacancy in zone 2 = 0.143
#            Non-residential vacancy in zone 1 = 0.13333
#            Non-residential vacancy in zone 2 = 0.2"""
#        self.storage.write_table(
#            table_name='target_vacancies',
#            table_data={
#                "year":array( 2*[2000, 2001, 2002, 2003] ),
#                "is_residential": array(4*[0] + 4*[1]), 
#                "target_vacancy_rate":array( 4*[0.2] + 4*[0.15] ),
#                }
#            )
#
#        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'),
#                                         control_totals=self.dataset_pool.get_dataset('annual_household_control_totals', {'id_name':[]}),
#                                         employment_control_totals=self.dataset_pool.get_dataset('annual_employment_control_totals', {'id_name':[]}),
#                                         building_sqft_per_job=self.dataset_pool.get_dataset('building_sqft_per_job', {'id_name':[]}),
#                                         )
#        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
#                                  living_units_dataset = self.dataset_pool.get_dataset('living_unit', {'id_name':['living_unit_id']}),
#                           year = 2000,
#                           occupied_spaces_variable = 'sc_occupied_spaces',
#                           total_spaces_variable = 'sc_total_spaces',
#                           target_attribute_name = 'target_vacancy_rate',
#                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
#                           living_units_from_dataset = self.dataset_pool.get_dataset('living_units_history', {'id_name':[]}),
#                           append_to_realestate_dataset = True,
#                           dataset_pool=self.dataset_pool,
#                           resources=self.compute_resources)
#        
#        new_buildings = DatasetSubset(results, index)
#        number_of_new_residential_units = results.get_attribute( 'residential_units' )[index].sum()
#        number_of_new_non_residential_units = results.get_attribute('non_residential_sqft')[index].sum()
#        self.assertEqual( number_of_new_residential_units, 5, 'Number of developed residential units does not match.')
#        self.assertEqual( number_of_new_non_residential_units, 80, 'Number of developed non-residential units does not match.')
#
#
#if __name__=="__main__":
#    opus_unittest.main()
