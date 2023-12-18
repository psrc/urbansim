# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .abstract_sum_from_gridcells import abstract_sum_from_gridcells

class developable_SSS_capacity(abstract_sum_from_gridcells):
    """ Aggregation over the corresponding gridcell variable """ 

    def __init__(self, type):
        self.gc_variable = "developable_%s_capacity" % type
        abstract_sum_from_gridcells.__init__(self)
 
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.developable_commercial_capacity"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
            table_name = building_types_table_name,
            table_data = {
                'building_type_id':array([1,2]), 
                'name': array(['residential', 'commercial']),
                'units': array(['residential_units', 'commercial_sqft'])
                }
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'zone':{
                    'zone_id': array([1,2])
                    },
                'gridcell':{
                    'developable_maximum_commercial_sqft':array([1200, 16, 3900, 15]), 
                    'zone_id':array([1,1,2,2])
                    },
                'building_type': building_types
                }, 
            dataset = 'zone'
            )
            
        should_be = array([1216, 3915])
        
        self.assertTrue(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()