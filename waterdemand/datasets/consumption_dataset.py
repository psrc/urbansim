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
from numpy import sort, where, array

class ConsumptionDataset(UrbansimDataset):
    """Set of consumption data."""

    id_name_default = ["grid_id","billyear","billmonth"]
    in_table_name_default = "WCSR_grid"
    out_table_name_default = "WCSR_grid"
    entity_name_default = "consumption"
    
