#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel as UrbansimHouseholdLocationChoiceModel

class HouseholdLocationChoiceModel(UrbansimHouseholdLocationChoiceModel):
    
    def __init__(self, location_set, **kwargs): 
        UrbansimHouseholdLocationChoiceModel.__init__(self, location_set, **kwargs)
        location_set.compute_variables(["urbansim_parcel.building.zone_id"], dataset_pool = self.dataset_pool)   
