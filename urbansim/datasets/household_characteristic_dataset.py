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

class HouseholdCharacteristicDataset(UrbansimDataset):
    """Set of household characteristics."""

    id_name_default = []
    in_table_name_default = "household_characteristics_for_ht"
    out_table_name_default = "household_characteristics_for_ht"
    dataset_name = "household_characteristic"

        
