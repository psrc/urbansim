# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


from numpy import where
from urbansim_parcel.models.subarea_scaling_jobs_model import SubareaScalingJobsModel

class SubareaDistributeUnplacedJobsModel(SubareaScalingJobsModel):
    """This model is used to place randomly (within sectors) any unplaced jobs.
    """
    model_name = "Subarea Distribute Unplaced Jobs Model"
     
    def run(self, location_set, agent_set, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset. The model selects all unplaced jobs 
            and passes them to ScalingJobsModel.
        """
        agents_index = where(agent_set.get_attribute(location_set.get_id_name()[0]) <= 0)[0]
        
        return SubareaScalingJobsModel.run(self, location_set, agent_set, agents_index, **kwargs)

