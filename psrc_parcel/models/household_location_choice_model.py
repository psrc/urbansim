# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel as UrbansimHouseholdLocationChoiceModel

class HouseholdLocationChoiceModel(UrbansimHouseholdLocationChoiceModel):
    
    def __init__(self, location_set, **kwargs): 
        UrbansimHouseholdLocationChoiceModel.__init__(self, location_set, **kwargs)
        location_set.compute_variables(["urbansim_parcel.building.zone_id"], dataset_pool = self.dataset_pool)   
