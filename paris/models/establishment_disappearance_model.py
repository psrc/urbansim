# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.choice_model import ChoiceModel
from urbansim_parcel.models.work_at_home_choice_model import prepare_for_estimate

class EstablishmentDisappearanceModel(ChoiceModel):
    """
    """
    model_name = "Establishment Disappearance Model"
    model_short_name = "EDM"

    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)

