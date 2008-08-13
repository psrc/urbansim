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

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingUseClassificationDataset(UrbansimDataset):
    id_name_default = "class_id"
    in_table_name_default = "building_use_classification"
    out_table_name_default = "building_use_classification"
    dataset_name = "building_use_classification"
    
#    def get_code(self, use):
#        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]