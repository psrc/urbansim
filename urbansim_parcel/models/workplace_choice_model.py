# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from urbansim_parcel.models.work_at_home_choice_model import prepare_for_estimate
from opus_core.model import get_specification_for_estimation
from numpy import arange, where
from opus_core.variables.variable_name import VariableName

class WorkplaceChoiceModel(AgentLocationChoiceModel):
    """
    """
    model_name = "Workplace Choice Model"
    model_short_name = "WCM"
    
    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)
