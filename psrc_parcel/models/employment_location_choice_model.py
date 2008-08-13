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

from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel as UrbansimEmploymentLocationChoiceModel

class EmploymentLocationChoiceModel(UrbansimEmploymentLocationChoiceModel):
    
    geography_id_name = 'zone_id'
    def __init__(self, group_member, location_set, **kwargs): 
        UrbansimEmploymentLocationChoiceModel.__init__(self, group_member, location_set, **kwargs)
        location_set.compute_variables(["urbansim_parcel.building.%s" % self.geography_id_name], dataset_pool = self.dataset_pool)   
