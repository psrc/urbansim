# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.choice_model import ChoiceModel
from opus_core.resources import Resources
from urbansim_parcel.models.work_at_home_choice_model import prepare_for_estimate
from numpy import where

class EstablishmentDisappearanceModel(ChoiceModel):
    """
    """
    model_name = "Establishment Disappearance Model"
    model_short_name = "EDM"

    def prepare_for_estimate(self, 
                             agent_set=None, 
                             filter=None,
                             data_objects=None,
                             *args,
                             **kwargs):
        specification, agents_index = prepare_for_estimate(agent_set=agent_set,
                                                           data_objects=data_objects,
                                                           *args,
                                                           **kwargs)

        if filter is not None:
            filter_condition = agent_set.compute_variables(filter, resources=Resources(data_objects))
            agents_index = where(filter_condition)[0]

        return specification, agents_index
