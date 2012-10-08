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

class AnnualIncomeAdjustmentDataset(UrbansimDataset):
    
    id_name_default = "annual_income_adjustment_id"
    in_table_name_default = "annual_income_adjustment"
    out_table_name_default = "annual_income_adjustment"
    dataset_name = "annual_income_adjustment"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)