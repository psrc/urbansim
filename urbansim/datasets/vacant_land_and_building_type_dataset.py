# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array

class VacantLandAndBuildingTypeDataset(BuildingTypeDataset):
    """building_types table with an additional row for vacant land (used by RealEstatePriceModel."""
    dataset_name = "vacant_land_and_building_type"
    
    def __init__ (self, *args, **kwargs):
        BuildingTypeDataset.__init__(self, *args, **kwargs)
        self.add_elements(data={self.get_id_name()[0]:array([self.get_id_attribute().max()+1]),
                                "name": array(["vacant_land"])}, require_all_attributes=False)
        
    
