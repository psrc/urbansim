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

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class PseudoBuildingDataset(UrbansimDataset):
    """A dataset of pseudo-buildings: There is one building in each zone for each building type (such as commercial, industrial, 
        governmental, residential)
    """
    id_name_default = "pseudo_building_id"
    in_table_name_default = "pseudo_buildings"
    out_table_name_default = "pseudo_buildings"
    dataset_name = "pseudo_building"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
