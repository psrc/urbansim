# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset, DatasetSubset
from numpy import array, where, ones, zeros, logical_and, logical_not
from numpy import arange, concatenate, resize, int32, float64, searchsorted, cumsum
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_replace
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from opus_core.misc import ismember
import re

try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
    import prettytable
except:
    PrettyTable = None

class RealEstateTransitionModel(Model):
    """
    """
    
    model_name = "Real Estate Transition Model"
    model_short_name = "RETM"
    
    def __init__(self, target_vancy_dataset=None, model_name=None, model_short_name=None):
        self.target_vancy_dataset = target_vancy_dataset
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
        
    def run(self, realestate_dataset,
            year=None, 
            occupied_spaces_variable="occupied_units",
            total_spaces_variable="total_units",
            target_attribute_name='target_vacancy_rate',
            sample_from_dataset = None,
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
        
        if not sample_from_dataset:
            sample_from_dataset = realestate_dataset
            
        #if dataset_pool is None:
        #    dataset_pool = SessionConfiguration().get_dataset_pool()
        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = where(self.target_vancy_dataset.get_attribute('year')==year)[0]
        target_vacancy_for_this_year = DatasetSubset(self.target_vancy_dataset, this_year_index)
        
        column_names = list(set( self.target_vancy_dataset.get_known_attribute_names() ) - set( [ target_attribute_name, occupied_spaces_variable, total_spaces_variable, 'year', '_hidden_id_'] ))
        column_names.sort(reverse=True)
        column_values = dict([ (name, target_vacancy_for_this_year.get_attribute(name)) for name in column_names + [target_attribute_name]])
        
        independent_variables = list(set([re.sub('_max$', '', re.sub('_min$', '', col)) for col in column_names]))
        dataset_known_attributes = realestate_dataset.get_known_attribute_names()
        sample_dataset_known_attributes = sample_from_dataset.get_known_attribute_names()
        for variable in independent_variables:
            if variable not in dataset_known_attributes:
                realestate_dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)
            if variable not in sample_dataset_known_attributes:
                sample_from_dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)
                
        dataset_known_attributes = realestate_dataset.get_known_attribute_names() #update after compute
        if sample_filter:
            short_name = VariableName(sample_filter).get_alias()
            if short_name not in dataset_known_attributes:
                filter_indicator = sample_from_dataset.compute_variables(sample_filter, dataset_pool=dataset_pool)
            else:
                filter_indicator = sample_from_dataset.get_attribute(short_name)
        else:
            filter_indicator = 1
                
        sampled_index = array([], dtype=int32)

        #log header
        if PrettyTable is not None:
            status_log = PrettyTable()
            if prettytable.__version__ >= 0.6: # compatibility issue
                status_log.field_names = column_names + ["actual", "target", "difference", "action"]
            else:
                status_log.set_field_names(column_names + ["actual", "target", "difference", "action"])
        else:
            logger.log_status("\t".join(column_names + ["actual", "target", "difference", "action"]))
        error_log = ''
        for index in range(target_vacancy_for_this_year.size()):
            this_sampled_index = array([], dtype=int32)
            indicator = ones( realestate_dataset.size(), dtype='bool' )
            sample_indicator = ones( sample_from_dataset.size(), dtype='bool' )
            criterion = {}   # for logging
            for attribute in independent_variables:
                if attribute in dataset_known_attributes:
                    dataset_attribute = realestate_dataset.get_attribute(attribute)
                    sample_attribute = sample_from_dataset.get_attribute(attribute)
                else:
                    raise ValueError, "attribute %s used in target vacancy dataset can not be found in dataset %s" % (attribute, realestate_dataset.get_dataset_name())
                
                if attribute + '_min' in column_names:
                    amin = target_vacancy_for_this_year.get_attribute(attribute+'_min')[index] 
                    criterion.update({attribute + '_min':amin})
                    if amin != -1:
                        indicator *= dataset_attribute >= amin
                        sample_indicator *= sample_attribute >= amin
                if attribute + '_max' in column_names: 
                    amax = target_vacancy_for_this_year.get_attribute(attribute+'_max')[index]
                    criterion.update({attribute + '_max':amax}) 
                    if amax != -1:
                        indicator *= dataset_attribute <= amax
                        sample_indicator *= sample_attribute <= amax
                if attribute in column_names: 
                    aval = column_values[attribute][index] 
                    criterion.update({attribute:aval}) 
                    if aval == -1:
                        continue
                    elif aval == -2:  ##treat -2 in control totals column as complement set, i.e. all other values not already specified in this column
                        indicator *= logical_not(ismember(dataset_attribute, column_values[attribute]))
                        sample_indicator *= logical_not(ismember(sample_attribute, column_values[attribute]))
                    else:
                        indicator *= dataset_attribute == aval
                        sample_indicator *= sample_attribute == aval
                        
            this_total_spaces_variable, this_occupied_spaces_variable = total_spaces_variable, occupied_spaces_variable
            ## total/occupied_spaces_variable can be specified either as a universal name for all realestate 
            ## or in targe_vacancy_rate dataset for each vacancy category
            if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_occupied_spaces_variable = target_vacancy_for_this_year.get_attribute(occupied_spaces_variable)[index]

            if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_total_spaces_variable = target_vacancy_for_this_year.get_attribute(total_spaces_variable)[index]
            
            logger.be_quiet() #temporarily disable logging
            realestate_dataset.compute_one_variable_with_unknown_package(this_occupied_spaces_variable, dataset_pool=dataset_pool)
            realestate_dataset.compute_one_variable_with_unknown_package(this_total_spaces_variable, dataset_pool=dataset_pool)
            sample_from_dataset.compute_one_variable_with_unknown_package(this_total_spaces_variable, dataset_pool=dataset_pool)
            logger.talk()
            
            actual_num = (indicator * realestate_dataset.get_attribute(this_total_spaces_variable)).sum()
            target_num = int(round( (indicator * realestate_dataset.get_attribute(this_occupied_spaces_variable)).sum() /\
                                    (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index]) 
                            ))
            diff = target_num - actual_num
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
            cat += [str(actual_num), str(target_num), str(diff), action]
            
            if PrettyTable is not None:
                status_log.add_row(cat)
            else:                
                logger.log_status("\t".join(cat))
            
        if PrettyTable is not None:
            logger.log_status("\n" + status_log.get_string())
        if error_log:
            logger.log_error(error_log)
            
        result_data = {}
        result_dataset = None
        index = array([], dtype='int32')
        if sampled_index.size > 0:
            ### ideally duplicate_rows() is all needed to add newly cloned rows
            ### to be more cautious, copy the data to be cloned, remove elements, then append the cloned data
            ##realestate_dataset.duplicate_rows(sampled_index)
            result_data.setdefault(year_built, resize(year, sampled_index.size).astype('int32'))
            ## also add 'independent_variables' to the new dataset
            for attribute in set(sample_from_dataset.get_primary_attribute_names() + independent_variables):
                if reset_attribute_value.has_key(attribute):
                    result_data[attribute] = resize(array(reset_attribute_value[attribute]), sampled_index.size)
                else:
                    result_data[attribute] = sample_from_dataset.get_attribute_by_index(attribute, sampled_index)
        
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
                index = realestate_dataset.add_elements(result_data, require_all_attributes=False,
                                                        change_ids_if_not_unique=True)                
            result_dataset = realestate_dataset
        
        return (result_dataset, index)
    
    def prepare_for_run(self, dataset_name=None, table_name=None, storage=None):
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
            
        return dataset
    
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function, like synchronizing persons with households table
        """
        pass

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.simulation_state import SimulationState
from urbansim.building.aliases import aliases
from opus_core.resources import Resources

aliases += [
            "occupied_sqft = numpy.clip(building.number_of_agents(job) * building.disaggregate(building_sqft_per_job.building_sqft_per_job), 0, building.non_residential_sqft)",
            "number_of_households = building.number_of_agents(household)",
            ]

class RETMTests(StochasticTestCase):

    def setUp( self ):
        SimulationState().set_current_time(2000)
        self.storage = StorageFactory().get_storage('dict_storage')

        self.storage.write_table(
            table_name='development_event_history',
            table_data={
                "zone_id":arange( 1, 100+1 ),
                "scheduled_year":array( 100*[1999] ),
                "building_type_id": array(30*[1] + 35*[2] + 35*[4]),
                "residential_units":array( 65*[0] + 35*[50] ),
                "non_residential_sqft":array( 65*[500] + 35*[0] )
                }
            )
        self.storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": arange( 1, 10+1 ),
                }
            )
        self.storage.write_table(
            table_name='buildings',
            table_data={
                "building_id": arange(1,31), # 1 building per building_type and zone
                "zone_id": array( [1, 1, 1,  2, 2,  2, 3, 3, 3, 4, 4, 4, 5, 5, 5,  6, 6,  6,  7, 7,  7, 8,  8, 8, 9,  9, 9, 10,10,10] ),
                "building_type_id": array(10*[1,2,4]),
                "residential_units": array(10*[0, 0, 100]),
                "non_residential_sqft": array(10*[100,150,0])
                }
            )
        self.storage.write_table(
            table_name='building_types',
            table_data={
                "building_type_id": arange(1,5),
                "building_type_name": array(['commercial', 'industrial','governmental', 'residential']),
                "is_residential": array([0,0,0,1])
                }
            )
#            create 1000 households, 100 in each of the 10 zones.
#            there will initially be 100 vacant residential units in each zone.
        self.storage.write_table(
            table_name='households',
            table_data={
                "household_id":arange( 1, 1000+1 ),
                "building_id": array(100 * range(3,31,3))
                }
            )
#            create 250 commercial jobs
        self.storage.write_table(
            table_name='jobs',
            table_data={
                "job_id":arange( 1, 250+1 ),
                "building_id":array( 20*range(1,31,3) + 5*range(2,32,3) ),
                "home_based":array( 250*[0] ),
                }
            )
        self.storage.write_table(
            table_name = "building_sqft_per_job",
            table_data = {
                   "building_id":          array([1,  2, 4, 5, 7, 8,10, 11,13,14,16,17,19,20,22,23,25,26,28, 29]),
                   "zone_id":              array([1,  1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]),
                   "building_type_id":     array([1,  2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,  1,  2]),
                   "building_sqft_per_job":array([10, 5, 8, 6, 20,10,10,20,10,20,10,20,10,20,10,20,10,20,10, 20]),
            }
        )  
        self.dataset_pool = DatasetPool(package_order=['urbansim_zone', 'urbansim_parcel', "urbansim"],
                                        storage=self.storage)

        self.compute_resources = Resources({})

    def test_no_development_with_zero_target_vacancy( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the results returned (which represents development projects) should be empty.
        In fact anytime the target vacancy rate is strictly less than the current vacancy rate,
        then no development should ever occur.
        """

        """specify that the target vacancies for the year 2000 should be 0% for both
        residential and non-residential. with these constrains, no new development projects
        should be spawned for any set of agents."""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000, 2000, 2000] ),
                "building_type_id": array([1,2,4]), 
                "occupied_units": array(['occupied_sqft', 'occupied_sqft', 'number_of_households']),
                "total_units":    array(['non_residential_sqft', 'non_residential_sqft', 'residential_units']),
                "target_vacancy":array( [0.0, 0, 0] ),
                }
            )

        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
                           year = 2000,
                           occupied_spaces_variable = 'occupied_units',
                           total_spaces_variable = 'total_units',
                           target_attribute_name = 'target_vacancy',
                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources)

        self.assertEqual( results, None,
                         "Nothing should've been added/developed" )
        
    def test_no_development_with_zero_target_vacancy_return_full_dataset( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the results returned (which represents development projects) should be empty.
        In fact anytime the target vacancy rate is strictly less than the current vacancy rate,
        then no development should ever occur.
        """

        """specify that the target vacancies for the year 2000 should be 0% for both
        residential and non-residential. with these constrains, no new development projects
        should be spawned for any set of agents."""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000, 2000, 2000] ),
                "building_type_id": array([1,2,4]), 
                "occupied_units": array(['occupied_sqft', 'occupied_sqft', 'number_of_households']),
                "total_units":    array(['non_residential_sqft', 'non_residential_sqft', 'residential_units']),
                "target_vacancy":array( [0.0, 0, 0] ),
                }
            )

        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
                           year = 2000,
                           occupied_spaces_variable = 'occupied_units',
                           total_spaces_variable = 'total_units',
                           target_attribute_name = 'target_vacancy',
                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
                           dataset_pool=self.dataset_pool,
                           append_to_realestate_dataset=True,
                           resources=self.compute_resources)

        self.assertEqual( results.size(), 30)
        
        self.assertEqual( index.size, 0,
                         "Nothing should've been added/developed" )

    def test_development_with_nonzero_target_vacancy_and_equal_history( self ):
        """Test basic cases, where current residential vacancy = 50%, target residential vacancy is 75%,
        current commercial vacancy is 75%, and target nonresidential vacancy is 50%.
        Residential development projects should occur, and none for nonresidential"""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001, 2001, 2001] ),
                "building_type_id": array([1,2,4]), 
                "occupied_units": array(['occupied_sqft', 'occupied_sqft', 'number_of_households']),
                "total_units":    array(['non_residential_sqft', 'non_residential_sqft', 'residential_units']),
                "target_total_vacancy":array( [0.5, 0.40, 0.75] )
                }
            )
        
        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
                           year = 2001,
                           occupied_spaces_variable = 'occupied_units',
                           total_spaces_variable = 'total_units',
                           target_attribute_name = 'target_total_vacancy',
                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
                           dataset_pool=self.dataset_pool,
                           append_to_realestate_dataset=True,
                           resources=self.compute_resources)

        number_of_new_residential_units = results.get_attribute( 'residential_units' )[index].sum()
        self.assertEqual( number_of_new_residential_units, 3000)
        
        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==1))[index].sum()
        should_be = 1000
        self.assertEqual(new_sqft, should_be)
        
        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==2))[index].sum()
        should_be = 0
        self.assertEqual(new_sqft, should_be)

    def test_universal_spaces_variable( self ):
        """
        occupied_spaces_variable and total_spaces_variable specified with arguments of the run method,
        instead of as attribute of target_vacancy_rates.  Results should be the same as the above unittest,
        except for residential building_type (building_type_id=4)
        """
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001, 2001] ),
                "building_type_id": array([1,2]), 
                "target_total_vacancy":array( [0.5, 0.40] )
                }
            )
        
        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
                           year = 2001,
                           occupied_spaces_variable = 'occupied_sqft',
                           total_spaces_variable = 'non_residential_sqft',
                           target_attribute_name = 'target_total_vacancy',
                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources)

        number_of_new_residential_units = results.get_attribute( 'residential_units' ).sum()
        should_be = 0
        self.assertEqual( number_of_new_residential_units, should_be )
        
        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==1)).sum()
        should_be = 1000
        self.assertEqual(new_sqft, should_be)
        
        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==2)).sum()
        should_be = 0
        self.assertEqual(new_sqft, should_be)        
        
    def test_development_with_99_percent_target_vacancy_and_equal_history( self ):
        """Not too different from the basic case above, just trying the other extreme.
        """
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001, 2001, 2001] ),
                "building_type_id": array([1,2,4]), 
                "occupied_units": array(['occupied_sqft', 'occupied_sqft', 'number_of_households']),
                "total_units":    array(['non_residential_sqft', 'non_residential_sqft', 'residential_units']),
                "target_total_vacancy":array( [0.999, 0.999, 0.999] )
                }
            )

        dptm = RealEstateTransitionModel(target_vancy_dataset=self.dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = self.dataset_pool.get_dataset('building'),
                           year = 2001,
                           occupied_spaces_variable = 'occupied_units',
                           total_spaces_variable = 'total_units',
                           target_attribute_name = 'target_total_vacancy',
                           sample_from_dataset = self.dataset_pool.get_dataset('development_event_history'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources)

        number_of_new_residential_units = results.get_attribute( 'residential_units' ).sum()
        should_be = 999000
        self.assertEqual( number_of_new_residential_units, should_be)

        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==1)).sum()
        should_be = 999000
        self.assertEqual(new_sqft, should_be)
        
        new_sqft = (results.get_attribute( 'non_residential_sqft' ) * (results.get_attribute('building_type_id')==2)).sum()
        should_be = 803500
        self.assertEqual(new_sqft, should_be)

if __name__=="__main__":
    opus_unittest.main()
