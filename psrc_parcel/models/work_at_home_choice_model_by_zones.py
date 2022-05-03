# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.choice_model import ChoiceModel
from numpy import array, arange, where, ones, logical_and, zeros, concatenate, setdiff1d
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.logger import logger
from urbansim_parcel.models.work_at_home_choice_model import WorkAtHomeChoiceModel

class WorkAtHomeChoiceModelByZones(WorkAtHomeChoiceModel):
    """
    For each zone, this model first predicts the probability of workers working at home, 
    then assigns them to one of the home-based jobs by sampling from this probability.
    """
        
    def __init__(self, match_number_of_jobs=True, *args, **kwargs):
        WorkAtHomeChoiceModel.__init__(self, match_number_of_jobs=match_number_of_jobs, *args, **kwargs)
        #self.upc_sequence.choice_class = None # no choices are made, since we only want the probabilities 
        
    def run(self, zones, run_choice_model=True, choose_job_only_in_residence_zone=True, 
            residence_id=None, match_choice_attribute_to_jobs=True, 
            modify_home_based_status = False, *args, **kwargs):
        agent_set = kwargs['agent_set']
        agents_index = kwargs.get('agents_index', None)
        if agents_index is None:
            agents_index = arange(agent_set.size())
        #cond_array = zeros(agent_set.size(), dtype="bool8")
        #cond_array[agents_index] = True
        zone_ids = zones.get_id_attribute()
        geo_id_name = zones.get_id_name()[0]
        agent_set.compute_one_variable_with_unknown_package(geo_id_name, dataset_pool=self.dataset_pool)
        self.job_set.compute_one_variable_with_unknown_package(geo_id_name, dataset_pool=self.dataset_pool)        

        if self.filter is not None:
            jobs_set_index = where( self.job_set.compute_variables(self.filter) )[0]
        else:
            jobs_set_index = arange( self.job_set.size() )  
        #self.job_set.compute_variables("urbansim_parcel.job.zone_id")
        #agent_set.compute_variables("urbansim_parcel.person.zone_id")
        
        # remove job links from all workers include in this model
        agent_set.set_values_of_one_attribute(self.choice_attribute_name, -1*ones(agents_index.size, dtype='int32'), 
                                              index=agents_index)
        assigned_worker_index = array([], dtype="int32")
        assigned_job_index = array([], dtype="int32") 
        agent_zone_ids = agent_set.get_attribute_by_index(geo_id_name, agents_index)
        job_zone_ids = self.job_set.get_attribute_by_index(geo_id_name, jobs_set_index)
        
        for zone_id in zone_ids:
            if zone_id <= 0: continue
            at_home_worker_in_this_zone = setdiff1d(where(agent_zone_ids == zone_id)[0], assigned_worker_index)
            job_set_in_this_zone = setdiff1d(where(job_zone_ids == zone_id)[0], assigned_job_index)
            assigned_job_set_in_this_zone = job_set_in_this_zone
            #new_index = where(logical_and(cond_array, agents_zones == zone_id))[0]
            logger.log_status("%s for %s %s" % (self.model_short_name, zones.get_dataset_name(), zone_id))
            if run_choice_model:
                kwargs['agents_index'] = agents_index[at_home_worker_in_this_zone]
                choices = ChoiceModel.run(self, *args, **kwargs)
                if self.match_number_of_jobs:
                    prob_work_at_home = self.upc_sequence.get_probabilities()[:, 1]
                    #job_set_in_this_zone = jobs_set_index[self.job_set[geo_id_name][jobs_set_index] == zone_id]
                    number_of_hb_jobs = job_set_in_this_zone.size
                    # sample workers for the number of jobs
                    if kwargs['agents_index'].size > number_of_hb_jobs:
                        #draw = probsample_noreplace(kwargs['agents_index'].size, min(agents_index.size, jobs_set_index.size), 
                        #                            prob_work_at_home)                    
                        draw = probsample_noreplace(arange(kwargs['agents_index'].size), min(kwargs['agents_index'].size, number_of_hb_jobs), 
                                            prob_work_at_home)
                    else:
                        draw = arange(kwargs['agents_index'].size)
                        assigned_job_set_in_this_zone = sample_noreplace(job_set_in_this_zone, draw.size)
                    assigned_worker_in_this_zone = at_home_worker_in_this_zone[draw]
                else:
                    assigned_worker_in_this_zone = at_home_worker_in_this_zone[choices == 1]
            else:
                at_home_worker_in_this_zone = at_home_worker_in_this_zone[where(agent_set[self.choice_attribute_name][kwargs['agents_index']] == 1)[0]]
                assigned_worker_in_this_zone, assigned_job_set_in_this_zone = self._assign_job_to_worker(at_home_worker_in_this_zone, 
                                                                                                             job_set_in_this_zone)
            
            assigned_worker_index = concatenate((assigned_worker_index, agents_index[assigned_worker_in_this_zone]))
            assigned_job_index = concatenate((assigned_job_index, jobs_set_index[assigned_job_set_in_this_zone]))
                
            logger.log_status("%s workers choose to work at home, %s workers chose to work out of home. %s HB jobs available." % 
                              (assigned_worker_in_this_zone.size, kwargs['agents_index'].size - assigned_worker_in_this_zone.size,
                               assigned_job_set_in_this_zone.size)
                               #where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 1)[0].size,
                               #where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 0)[0].size)
                               )
                
        if match_choice_attribute_to_jobs:
            all_choices = zeros(agent_set.size(), dtype='int32')
            all_choices[assigned_worker_index] = 1
            agent_set.set_values_of_one_attribute(self.choice_attribute_name, all_choices[agents_index],
                                                      index = agents_index)
            
        agent_set.set_values_of_one_attribute(self.job_set.get_id_name()[0], 
                                              self.job_set.get_id_attribute()[assigned_job_index], 
                                              index=assigned_worker_index)
        agent_set.compute_variables([self.location_id_name], dataset_pool=self.dataset_pool)
        self.job_set.modify_attribute(name=VariableName(self.location_id_name).get_alias(), 
                                      data=agent_set.get_attribute_by_index(self.location_id_name, assigned_worker_index),
                                      index=assigned_job_index)
        #agent_set.flush_dataset()
        #self.job_set.flush_dataset()
            
            
        logger.log_status("Total: %s workers work at home, %s workers work out of home." % 
                          (where(agent_set.get_attribute(self.choice_attribute_name) == 1)[0].size,
                           where(agent_set.get_attribute(self.choice_attribute_name) == 0)[0].size
                          ))
