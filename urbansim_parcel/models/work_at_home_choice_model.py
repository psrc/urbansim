# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.choice_model import ChoiceModel
from opus_core.model import prepare_specification_and_coefficients
from opus_core.model import get_specification_for_estimation
from numpy import array, arange, where, ones, concatenate, logical_and
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.misc import unique_values
from opus_core.logger import logger

class WorkAtHomeChoiceModel(ChoiceModel):
    """
    This model first predicts the probability of workers working at home, 
    then assigns them to one of the home-based jobs 
    """
    model_name = "Work At Home Choice Model"
    model_short_name = "WAHCM"

    def __init__(self, choice_set, filter=None, choice_attribute_name='work_at_home', location_id_name='urbansim_parcel.person.building_id', **kwargs):
        self.job_set = choice_set
        self.filter = filter
        self.choice_attribute_name = choice_attribute_name
        self.location_id_name = location_id_name
        ChoiceModel.__init__(self, [0, 1], choice_attribute_name=choice_attribute_name, **kwargs)
        
    def run(self, run_choice_model=True, choose_job_only_in_residence_zone=False, *args, **kwargs):
        agent_set = kwargs['agent_set']
        if run_choice_model:
            choices = ChoiceModel.run(self, *args, **kwargs)
            #prob_work_at_home = self.upc_sequence.probabilities[:, 0]
                
            agent_set.set_values_of_one_attribute(self.choice_attribute_name, 
                                                  choices, 
                                                  index=kwargs['agents_index'])
            at_home_worker_index = kwargs['agents_index'][choices==1]
            logger.log_status("%s workers choose to work at home, %s workers chose to work out of home." % 
                              (where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 1)[0].size,
                               where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 0)[0].size))            
        else:
            at_home_worker_index = where(logical_and( 
                                                     agent_set.get_attribute(self.choice_attribute_name) == 1,
                                                     agent_set.get_attribute('job_id') <= 0
                                                     )
                                        )[0]
        
        if self.filter is not None:
            jobs_set_index = where( self.job_set.compute_variables(self.filter) )[0]
        else:
            jobs_set_index = arange( self.job_set.size() )
            
        logger.log_status("Total: %s workers work at home, (%s workers work out of home), will try to assign %s workers to %s jobs." % 
                          (where(agent_set.get_attribute(self.choice_attribute_name) == 1)[0].size,
                           where(agent_set.get_attribute(self.choice_attribute_name) == 0)[0].size,
                          at_home_worker_index.size,
                          jobs_set_index.size
                          ))

        if not choose_job_only_in_residence_zone:
            assigned_worker_index, assigned_job_index = self._assign_job_to_worker(at_home_worker_index, jobs_set_index)
        else:
            agent_set.compute_variables("urbansim_parcel.person.zone_id")
            self.job_set.compute_variables("urbansim_parcel.job.zone_id")
            agent_zone_ids = agent_set.get_attribute_by_index('zone_id', at_home_worker_index)
            job_zone_ids = self.job_set.get_attribute_by_index('zone_id', jobs_set_index)
            unique_zones = unique_values(job_zone_ids)
            assigned_worker_index = array([], dtype="int32")
            assigned_job_index = array([], dtype="int32")
            for this_zone in unique_zones:
                logger.log_status("zone_id: %s" % this_zone)
                if this_zone <= 0: continue
                at_home_worker_in_this_zone = where(agent_zone_ids == this_zone)[0]
                job_set_in_this_zone = where(job_zone_ids == this_zone)[0]
                assigned_worker_in_this_zone, assigned_job_set_in_this_zone = self._assign_job_to_worker(at_home_worker_in_this_zone, job_set_in_this_zone)
                assigned_worker_index = concatenate((assigned_worker_index, at_home_worker_index[assigned_worker_in_this_zone]))
                assigned_job_index = concatenate((assigned_job_index, jobs_set_index[assigned_job_set_in_this_zone]))

        ## each worker can only be assigned to 1 job
        #assert assigned_worker_index.size == unique_values(assigned_worker_index).size
        agent_set.set_values_of_one_attribute(self.job_set.get_id_name()[0], 
                                              self.job_set.get_id_attribute()[assigned_job_index], 
                                              index=assigned_worker_index)
        agent_set.compute_variables([self.location_id_name], dataset_pool=self.dataset_pool)
        self.job_set.modify_attribute(name=VariableName(self.location_id_name).get_alias(), 
                                      data=agent_set.get_attribute_by_index(self.location_id_name, assigned_worker_index),
                                      index=assigned_job_index)

    def _assign_job_to_worker(self, worker_index, job_index):
        logger.log_status("Atempt to assign %s jobs to %s workers" % (worker_index.size, job_index.size))
        if worker_index.size >= job_index.size: 
           #number of at home workers is greater than the available choice (home_based jobs by default)
            assigned_worker_index = sample_noreplace(worker_index, job_index.size)
            assigned_job_index = job_index
        else:
            assigned_worker_index = worker_index
            assigned_job_index=sample_noreplace(job_index,worker_index.size)
        logger.log_status("Assigned %s jobs to %s workers" % (assigned_worker_index.size, assigned_job_index.size))
        
        return (assigned_worker_index, assigned_job_index)
 
    def prepare_for_run(self, 
                        specification_storage=None, 
                        specification_table=None,
                        coefficients_storage=None,
                        coefficients_table=None,
                        agent_set=None,
                        agents_filter=None,
                        data_objects=None,
                        **kwargs):
        
        spec, coeff = prepare_specification_and_coefficients(specification_storage=specification_storage,
                                               specification_table=specification_table, 
                                               coefficients_storage=coefficients_storage,
                                               coefficients_table=coefficients_table, **kwargs)
        
        if agents_filter is not None:
            agent_set.compute_variables(agents_filter, resources=Resources(data_objects))
            index = where(agent_set.get_attribute(VariableName(agents_filter).get_alias()) > 0)[0]
        
        return (spec, coeff, index)
    
    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)

    
def prepare_for_estimate(specification_dict = None, 
                         specification_storage=None, 
                         specification_table=None,
                         agent_set=None, 
                         household_set=None,
                         agents_for_estimation_storage=None,
                         agents_for_estimation_table=None,
                         households_for_estimation_table=None,
                         join_datasets=False,
                         filter=None,
                         data_objects=None):
    specification = get_specification_for_estimation(specification_dict, 
                                                     specification_storage, 
                                                     specification_table)
    if agents_for_estimation_storage is not None:                 
        estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), 
                                 dataset_name=agent_set.get_dataset_name())
        hh_estimation_set = None
        if households_for_estimation_table is not None:
            hh_estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                     in_table_name=households_for_estimation_table,
                                     id_name=household_set.get_id_name(), 
                                     dataset_name=household_set.get_dataset_name())
        
        filter_index = arange(estimation_set.size())
        if filter:
            estimation_set.compute_variables(filter, resources=Resources(data_objects))
            filter_index = where(estimation_set.get_attribute(filter) > 0)[0]
            #estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)
        
        if join_datasets:
            if hh_estimation_set is not None:
                household_set.join_by_rows(hh_estimation_set, require_all_attributes=False,
                                           change_ids_if_not_unique=True)
                
            agent_set.join_by_rows(estimation_set, require_all_attributes=False,
                                   change_ids_if_not_unique=True)
            index = arange(agent_set.size() - estimation_set.size(), agent_set.size())[filter_index]
        else:
            index = agent_set.get_id_index(estimation_set.get_id_attribute()[filter_index])
    else:
        if agent_set is not None:
            index = arange(agent_set.size())
        else:
            index = None
            
    return (specification, index)
