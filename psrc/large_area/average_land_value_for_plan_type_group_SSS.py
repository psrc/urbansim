# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class average_land_value_for_plan_type_group_SSS(Variable):
    """average land value for gridcell in residential plan types"""
    _return_type="float32"

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)

    def dependencies(self):
        
        return [attribute_label("gridcell", 'is_in_plan_type_group_%s' % self.group),
                attribute_label("gridcell", 'is_in_plan_type_group_%s' % self.group),
                attribute_label("gridcell", 'total_land_value_if_in_plan_type_group_%s' % self.group),
                "total_%s_land_value = large_area.aggregate(gridcell.total_land_value_if_in_plan_type_group_%s, intermediates=[zone, faz])" % (self.group,self.group),
                "number_of_%s_gridcells = large_area.aggregate(gridcell.is_in_plan_type_group_%s, intermediates=[zone, faz])" % (self.group, self.group), 
                my_attribute_label("large_area_id")]

    def compute(self, dataset_pool):
        num = self.get_dataset().get_attribute("number_of_%s_gridcells" % self.group)
        acres = num * dataset_pool.get_dataset('urbansim_constant')["acres"]
        return ma.filled(self.get_dataset().get_attribute("total_%s_land_value" % self.group) / \
                      ma.masked_where(acres==0.0, acres.astype(float32)), 0.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    

from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.large_area.average_land_value_for_plan_type_group_residential"
 
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
                "zone_id":array([1,2,3,4,5]),
                "faz_id":array([1,2,2,3,4]),
                },
        )
        storage.write_table(
            table_name='gridcells',
            table_data={
                "grid_id":array([1,2,3,4,5,6,7,8,9]),
                "zone_id":array([1,1,1,2,2,3,3,4,5]),
                "total_land_value":array([10, 11, 12, 13, 14, 15, 16, 17, 18]),
                "is_in_plan_type_group_residential":array([1, 1, 1, 1, 0, 0, 1, 0, 1])    
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                'acres': array([1.5]),
                }
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        large_area = dataset_pool.get_dataset('large_area')
        large_area.compute_variables(self.variable_name,
                                     dataset_pool=dataset_pool)
        values = large_area.get_attribute(self.variable_name)
            
        should_be = array([7.333, 9.667, 12.0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()