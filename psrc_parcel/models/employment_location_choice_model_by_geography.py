# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from psrc_parcel.models.employment_location_choice_model import EmploymentLocationChoiceModel

class EmploymentLocationChoiceModelByGeography(EmploymentLocationChoiceModel):
    
    def __init__(self, group_member, location_set, geography_dataset, *args, **kwargs):
        self.geography_dataset = geography_dataset
        self.geography_id_name = geography_dataset.get_id_name()[0]
        EmploymentLocationChoiceModel.__init__(self, group_member, location_set, *args, **kwargs)
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        geography_ids = self.geography_dataset.get_id_attribute()
        geographies_of_agents = agent_set.get_attribute(self.geography_id_name)
        orig_filter = self.filter
        for geography_id in geography_ids:
            new_index = where(logical_and(cond_array, geographies_of_agents == geography_id))[0]
            if orig_filter is not None:
                self.filter = "(building.%s == %s) * %s" % (self.geography_id_name, geography_id, orig_filter)
            else:
                self.filter = "building.%s == %s" % (self.geography_id_name, geography_id)
            logger.log_status("ELCM for %s %s" % (self.geography_dataset.get_dataset_name(), geography_id))
            EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                              agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            # self.choice_set.flush_dataset()
        # set the right parcels
        parcels = agent_set.compute_variables(["job.disaggregate(building.parcel_id)"],
                                              dataset_pool = self.dataset_pool)
        agent_set.modify_attribute(name="parcel_id", data = parcels)
