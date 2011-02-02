# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.choice_model import ChoiceModel
from numpy import array, arange, where, ones, logical_and, zeros
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import probsample_noreplace
from opus_core.logger import logger
from urbansim_parcel.models.work_at_home_choice_model import WorkAtHomeChoiceModel

class WorkAtHomeChoiceModelByZones(WorkAtHomeChoiceModel):
    """
    For each zone, this model first predicts the probability of workers working at home, 
    then assigns them to one of the home-based jobs by sampling from this probability.
    """
        
    def __init__(self, *args, **kwargs):
        WorkAtHomeChoiceModel.__init__(self, *args, **kwargs)
        self.upc_sequence.choice_class = None # no choices are made, since we only want the probabilities 
        
    def run(self, zones, run_choice_model=True, choose_job_only_in_residence_zone=True, **kwargs):
        agent_set = kwargs['agent_set']
        agents_index = kwargs.get('agents_index', None)
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        zone_ids = zones.get_id_attribute()
        agents_zones = agent_set.compute_variables(['urbansim_parcel.%s.%s' % (agent_set.get_dataset_name(),
                                                        zones.get_id_name()[0])], dataset_pool=self.dataset_pool)
        if self.filter is not None:
            jobs_set_index = where( self.job_set.compute_variables(self.filter) )[0]
        else:
            jobs_set_index = arange( self.job_set.size() )  
        #self.job_set.compute_variables("urbansim_parcel.job.zone_id")
        agent_set.compute_variables("urbansim_parcel.person.zone_id")
        # remove job links from all workers
        agent_set.set_values_of_one_attribute(self.choice_attribute_name, -1*ones(agents_index.size, dtype='int32'), 
                                              index=agents_index)
        for zone_id in zone_ids:
            new_index = where(logical_and(cond_array, agents_zones == zone_id))[0]
            logger.log_status("%s for zone %s" % (self.model_short_name, zone_id))
            if run_choice_model:
                kwargs['agents_index'] = new_index
                choices = ChoiceModel.run(self, **kwargs)
                prob_work_at_home = self.upc_sequence.get_probabilities()[:, 1]
                job_set_in_this_zone = jobs_set_index[self.job_set['zone_id'][jobs_set_index] == zone_id]
                number_of_hb_jobs = job_set_in_this_zone.size
                # sample workers for the number of jobs
                draw = probsample_noreplace(kwargs['agents_index'], min(kwargs['agents_index'].size, number_of_hb_jobs), 
                                            prob_work_at_home)
                agent_set.set_values_of_one_attribute(self.choice_attribute_name, 
                                                  ones(draw.size, dtype=agent_set[self.choice_attribute_name].dtype), 
                                                  index=draw)
                logger.log_status("%s workers choose to work at home, %s workers chose to work out of home." % 
                              (where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 1)[0].size,
                               where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 0)[0].size))            
            at_home_worker_in_this_zone = kwargs['agents_index'][agent_set[self.choice_attribute_name][kwargs['agents_index']] == 1]
            assigned_worker_in_this_zone, assigned_job_set_in_this_zone = self._assign_job_to_worker(at_home_worker_in_this_zone, 
                                                                                                     job_set_in_this_zone)
            agent_set.set_values_of_one_attribute(self.job_set.get_id_name()[0], 
                                              self.job_set.get_id_attribute()[assigned_job_set_in_this_zone], 
                                              index=assigned_worker_in_this_zone)
            agent_set.compute_variables([self.location_id_name], dataset_pool=self.dataset_pool)
            self.job_set.modify_attribute(name=VariableName(self.location_id_name).get_alias(), 
                                      data=agent_set.get_attribute_by_index(self.location_id_name, assigned_worker_in_this_zone),
                                      index=assigned_job_set_in_this_zone)
            agent_set.flush_dataset()
            self.job_set.flush_dataset()
            
            
        logger.log_status("Total: %s workers work at home, (%s workers work out of home), will try to assign %s workers to %s jobs." % 
                          (where(agent_set.get_attribute(self.choice_attribute_name) == 1)[0].size,
                           where(agent_set.get_attribute(self.choice_attribute_name) == 0)[0].size,
                          at_home_worker_index.size,
                          jobs_set_index.size
                          ))
