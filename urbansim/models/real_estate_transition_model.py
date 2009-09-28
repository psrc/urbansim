# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset, DatasetSubset
from numpy import array, where, ones, zeros, setdiff1d, logical_and
from numpy import arange, concatenate, resize, int32, float64
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_replace
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
import re

class RealEstateTransitionModel(Model):
    """ The model behind household transition model and employment transition
    model
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
            dataset_pool=None,  **kwargs):
        """ sample_filter attribute/variable indicates which records in the dataset are eligible in the sampling for removal or cloning
        ## TODO: enable arguments to discard attributes in sample_from_dataset
        """
        
        if sample_from_dataset:
            self.sample_from_dataset = sample_from_dataset
        else:
            sample_from_dataset = realestate_dataset
        #if dataset_pool is None:
        #    dataset_pool = SessionConfiguration().get_dataset_pool()
        if year is None:
            year = SimulationState().get_current_time()
        this_year_index = where(self.target_vancy_dataset.get_attribute('year')==year)[0]
        target_vacancy_for_this_year = DatasetSubset(self.target_vancy_dataset, this_year_index)
        
        column_names = list(set( self.target_vancy_dataset.get_known_attribute_names() ) - set( [ target_attribute_name, 'year', '_hidden_id_'] ))
        column_names.sort()
        column_values = dict([ (name, target_vacancy_for_this_year.get_attribute(name)) for name in column_names + [target_attribute_name]])
        
        independent_variables = list(set([re.sub('_max$', '', re.sub('_min$', '', col)) for col in column_names]))
        dataset_known_attributes = realestate_dataset.get_known_attribute_names()
        for variable in independent_variables + [occupied_spaces_variable, total_spaces_variable]:
            if variable not in dataset_known_attributes:
                realestate_dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)
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
        logger.log_status("\t".join(column_names + ["actual", "target", "difference", "action"]))
        for index in range(target_vacancy_for_this_year.size()):
            this_sampled_index = array([], dtype=int32)
            indicator = ones( realestate_dataset.size(), dtype='bool' )
            sample_indicator = ones( sample_from_dataset.size(), dtype='bool' )
            criterion = {} 
            for attribute in independent_variables:
                if attribute in dataset_known_attributes:
                    dataset_attribute = realestate_dataset.get_attribute(attribute)
                    sample_attribute = sample_from_dataset.get_attribute(attribute)
                else:
                    raise ValueError, "attribute %s used in control total dataset can not be found in dataset %s" % (attribute, realestate_dataset.get_dataset_name())
                
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
                        complement_values = setdiff1d( dataset_attribute, column_values[attribute] )
                        has_one_of_the_complement_value = zeros(dataset_attribute.size, dtype='bool')
                        for value in complement_values:
                            has_one_of_the_complement_value += dataset_attribute == value
                        indicator *= has_one_of_the_complement_value
                        ##TODO sample_indicator:
                    else:
                        indicator *= dataset_attribute == aval
                        sample_indicator *= sample_attribute == aval
                        
            actual_num = (indicator * realestate_dataset.get_attribute(total_spaces_variable)).sum()
            target_num = (indicator * realestate_dataset.get_attribute(occupied_spaces_variable)).sum() /\
                         (1 - target_vacancy_for_this_year.get_attribute(target_attribute_name)[index])
            diff = target_num - actual_num
            if diff > 0:
                total_spaces_in_sample_dataset = sample_from_dataset.get_attribute(total_spaces_variable)
                legit_index = where(logical_and(sample_indicator, filter_indicator))[0]
                mean_size = total_spaces_in_sample_dataset[legit_index].mean()
                # Ensure that there are some development projects to choose from
                num_of_projects_to_sample = max( 10, int( diff / mean_size ))
                while total_spaces_in_sample_dataset[this_sampled_index].sum() < diff:
                    lucky_index = sample_replace(legit_index, num_of_projects_to_sample)
                    this_sampled_index = concatenate((this_sampled_index, lucky_index))
                sampled_index = concatenate((sampled_index, this_sampled_index))
            #if diff < 0: #demolition; not yet supported
            
                ##log status
                action = "0"
                if this_sampled_index.size > 0:
                    action_num = total_spaces_in_sample_dataset[this_sampled_index].sum()
                    if diff > 0: action = "+" + str(action_num)
                    if diff < 0: action = "-" + str(action_num)
                cat = [ str(criterion[col]) for col in column_names]
                cat += [str(actual_num), str(target_num), str(diff), action]
                logger.log_status("\t".join(cat))
            
        project_data = {}
        project_dataset = None
        if sampled_index.size > 0:
            ### ideally duplicate_rows() is all needed to add newly cloned rows
            ### to be more cautious, copy the data to be cloned, remove elements, then append the cloned data
            ##realestate_dataset.duplicate_rows(sampled_index)
            logger.log_status()
            for attribute in sample_from_dataset.get_primary_attribute_names():
                if reset_attribute_value.has_key(attribute):
                    project_data[attribute] = resize(array(reset_attribute_value[attribute]), sampled_index.size)
                else:
                    project_data[attribute] = sample_from_dataset.get_attribute_by_index(attribute, sampled_index)
        
            storage = StorageFactory().get_storage('dict_storage')
            storage.write_table(table_name='development_projects', table_data=project_data)
    
            project_dataset = Dataset(id_name = [],
                                      in_storage = storage,
                                      in_table_name = "development_projects",
                                      dataset_name = "development_project"
                                      )
        
        return project_dataset
    
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
        return dataset
    
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function, like synchronizing persons with households table
        """
        pass

## TODO: add unittests