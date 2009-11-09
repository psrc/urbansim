# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from urbansim_parcel.models.scaling_jobs_model import ScalingJobsModel

class ScalingJobsModelByGeography(ScalingJobsModel):
        
    def run(self, geography_set, location_set, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        geography_ids = geography_set.get_id_attribute()
        geography_id_name = geography_set.get_id_name()[0]
        geographies_of_agents = agent_set.compute_variables(["urbansim_parcel.job.%s" % geography_id_name], dataset_pool = self.dataset_pool)
        orig_filter = self.filter
        for geography_id in geography_ids:
            new_index = where(logical_and(cond_array, geographies_of_agents == geography_id))[0]
            if orig_filter is not None:
                self.filter = "(urbansim_parcel.building.%s == %s) * %s" % (geography_id_name, geography_id, orig_filter)
            else:
                self.filter = "urbansim_parcel.building.%s == %s" % (geography_id_name, geography_id)
            logger.log_status("SJM for %s %s" % (geography_set.get_dataset_name(), geography_id))
            ScalingJobsModel.run(self, location_set, agent_set, 
                                              agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            # self.choice_set.flush_dataset()
        # set the right parcels
        parcels = agent_set.compute_variables(["job.disaggregate(building.parcel_id)"],
                                              dataset_pool = self.dataset_pool)
        agent_set.modify_attribute(name="parcel_id", data = parcels)
