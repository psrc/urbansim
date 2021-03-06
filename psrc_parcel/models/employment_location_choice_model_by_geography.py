# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, ceil, maximum
from opus_core.logger import logger
from psrc_parcel.models.employment_location_choice_model import EmploymentLocationChoiceModel

class EmploymentLocationChoiceModelByGeography(EmploymentLocationChoiceModel):
    
    def __init__(self, group_member, location_set, geography_dataset, *args, **kwargs):
        self.geography_dataset = geography_dataset
        self.geography_id_name = geography_dataset.get_id_name()[0]
        EmploymentLocationChoiceModel.__init__(self, group_member, location_set, *args, **kwargs)
        
    def run(self, specification, coefficients, agent_set, agents_index=None, increase_job_capacity_if_needed=True, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        geography_ids = self.geography_dataset.get_id_attribute()
        geographies_of_agents = agent_set.get_attribute(self.geography_id_name)
        orig_filter = self.filter
        for geography_id in geography_ids:
        #for geography_id in [197]:
            new_index = where(logical_and(cond_array, geographies_of_agents == geography_id))[0]
            if orig_filter is not None:
                self.filter = "(building.%s == %s) * %s" % (self.geography_id_name, geography_id, orig_filter)
            else:
                self.filter = "building.%s == %s" % (self.geography_id_name, geography_id)
            logger.log_status("ELCM for %s %s" % (self.geography_dataset.get_dataset_name(), geography_id))
            for irun in [1,2]:
                EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                              agents_index=new_index, **kwargs)
                if not increase_job_capacity_if_needed or irun > 1:
                    break
                # increase buildings job_capacity to fit all jobs
                unplaced_size = (agent_set['building_id'][agent_set[self.geography_id_name]==geography_id] <= 0).sum()
                if unplaced_size <= 0 or not 'job_capacity' in self.choice_set.get_known_attribute_names():
                    break
                filt = where(self.choice_set.compute_variables(self.filter, dataset_pool=self.dataset_pool)>0)[0]
                if filt.size <= 0:
                    break
                noa = self.choice_set.compute_variables('noj = building.number_of_agents(job)', 
                                                                    dataset_pool=self.dataset_pool)
                cap = maximum(self.choice_set['job_capacity'][filt], self.choice_set['noj'][filt])
                if unplaced_size <= cap.sum():
                    break
# TODO: make these two lines optional
#                self.choice_set.modify_attribute('job_capacity', data=ceil(cap + cap*(unplaced_size/float(cap.sum()))).astype(cap.dtype), index=filt)
#                logger.log_warning('Capacity increased by %s jobs.' % round(cap*unplaced_size/float(cap.sum())))
            agent_set.flush_dataset()
            # self.choice_set.flush_dataset()
        # set the right parcels
        #parcels = agent_set.compute_variables(["job.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
