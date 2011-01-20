# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel as UrbansimEmploymentLocationChoiceModel

class EmploymentLocationChoiceModel(UrbansimEmploymentLocationChoiceModel):
    
    geography_id_name = 'zone_id'
    def __init__(self, group_member, location_set, **kwargs): 
        UrbansimEmploymentLocationChoiceModel.__init__(self, group_member, location_set, **kwargs)
        location_set.compute_variables(["urbansim_parcel.building.%s" % self.geography_id_name], dataset_pool = self.dataset_pool)   
