# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from urbansim_parcel.models.work_at_home_choice_model import prepare_for_estimate

class WorkplaceChoiceModel(AgentLocationChoiceModel):
    """
    """
    model_name = "Workplace Choice Model"
    model_short_name = "WCM"
    
    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)
