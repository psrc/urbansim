# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide

class avg_val_per_unit_SSS(Variable):
    """average value per unit of the given type"""
    
    _return_type="float32"

    def __init__(self, type):
        self.value = "total_value_%s = large_area.aggregate(urbansim.zone.total_value_%s, intermediates=[faz])" % (type, type)
        self.space = "%s_space = large_area.aggregate(urbansim.zone.buildings_%s_space, intermediates=[faz])" % (type, type)
        self.type = type
        Variable.__init__(self)

    def dependencies(self):
        return [self.value, self.space]

    def compute(self, dataset_pool):
        sp = self.get_dataset().get_attribute("%s_space" % self.type)
        return safe_array_divide(self.get_dataset().get_attribute("total_value_%s" % self.type), sp)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.large_area.avg_val_per_unit_industrial"
 
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='large_areas',
            table_data={
                "large_area_id":array([1, 2, 3])
                },
        )
        storage.write_table(
            table_name='fazes',
            table_data={
                "faz_id":array([1,2,3,4]),
                "large_area_id":array([1,2,3,3]),
                },
        )
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,2,3,4,5]),
                "faz_id":array([1,2,2,3,4]),
                "total_value_industrial":array([10, 11, 12, 13, 14]),
                "buildings_industrial_space":array([10, 1, 2, 1, 0])    
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        large_area = dataset_pool.get_dataset('large_area')
        large_area.compute_variables(self.variable_name,
                                     dataset_pool=dataset_pool)
        values = large_area.get_attribute(self.variable_name)
            
        should_be = array([1, 23/3.0, 27])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()