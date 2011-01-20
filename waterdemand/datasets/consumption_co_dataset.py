# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where

from urbansim.datasets.dataset import Dataset as UrbansimDataset


class ConsumptionCoDataset(UrbansimDataset):
    """Set of Bellevue data."""

    id_name_default = ['grid_id', 'month', 'year']
    ### TODO: non-integer id_names cannot be used. This is bad because this
    ###       dataset depends on account_type as a primary id. Thus, in order
    ###       to work around this severe limitation, this dataset should be
    ###       used in conjunction with get_data_subset_by_account_type() below
    ###       to filter by account type.
    
    dataset_name = 'consumption_co'
    in_table_name_default = "consumption_co"
    out_table_name_default = "consumption_co"
    entity_name_default = "consumption_co"

        
from opus_core.tests import opus_unittest


class TestConsumptionCoDataset(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        

if __name__ == '__main__':
    opus_unittest.main()