# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel as UrbansimHouseholdLocationChoiceModel

class HouseholdLocationChoiceModel(UrbansimHouseholdLocationChoiceModel):
    
    def __init__(self, location_set, **kwargs): 
        UrbansimHouseholdLocationChoiceModel.__init__(self, location_set, **kwargs)
        location_set.compute_variables(["urbansim_parcel.building.zone_id"], dataset_pool = self.dataset_pool)   
