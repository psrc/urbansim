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

from numpy import unique, where
from opus_core.misc import do_id_mapping_array_from_array
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class PseudoBuildingDataset(UrbansimDataset):
    """A dataset of pseudo-buildings: There is one building in each zone for each building type (such as commercial, industrial, 
        governmental, residential)
    """
    id_name_default = "pseudo_building_id"
    in_table_name_default = "pseudo_buildings"
    out_table_name_default = "pseudo_buildings"
    dataset_name = "pseudo_building"
    
    location_id_name = 'zone_id'
    type_id_name = 'building_type_id'
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        self.create_location_type_mappings()
        
    def create_location_type_mappings(self):
        ids = self.get_id_attribute()
        locs = self.get_attribute(self.location_id_name)
        types = self.get_attribute(self.type_id_name)
        unique_types = unique(types)
        maxid = locs.max()
        minid = locs.min()
        self.location_type_dict = {}
        self.location_type_dict_shift = minid
        for bt in unique_types:
            locs_of_this_type = where(types == bt, locs, maxid+1)
            self.location_type_dict[bt] = do_id_mapping_array_from_array(locs_of_this_type, minid=minid, maxid=maxid+1)
            
    def get_ids_of_locations_and_type(self, locations, type_id):
        idx = self.location_type_dict[type_id][locations - self.location_type_dict_shift]
        return self.get_id_attribute()[idx]