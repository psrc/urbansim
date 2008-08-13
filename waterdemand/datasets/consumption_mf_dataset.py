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


class ConsumptionMfDataset(UrbansimDataset):
    """Set of Bellevue data."""

    id_name_default = ['grid_id', 'month', 'year']
    ### TODO: non-integer id_names cannot be used. This is bad because this
    ###       dataset depends on account_type as a primary id. Thus, in order
    ###       to work around this severe limitation, this dataset should be
    ###       used in conjunction with get_data_subset_by_account_type() below
    ###       to filter by account type.
    
    dataset_name = 'consumption_mf'
    in_table_name_default = "consumption_mf"
    out_table_name_default = "consumption_mf"
    entity_name_default = "consumption_mf"

        
from opus_core.tests import opus_unittest


class TestConsumptionReDataset(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        

if __name__ == '__main__':
    opus_unittest.main()