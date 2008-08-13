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

from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array

class VacantLandAndBuildingTypeDataset(BuildingTypeDataset):
    """building_types table with an additional row for vacant land (used by RealEstatePriceModel."""
    dataset_name = "vacant_land_and_building_type"
    
    def __init__ (self, *args, **kwargs):
        BuildingTypeDataset.__init__(self, *args, **kwargs)
        self.add_elements(data={self.get_id_name()[0]:array([self.get_id_attribute().max()+1]),
                                "name": array(["vacant_land"])}, require_all_attributes=False)
        
    
