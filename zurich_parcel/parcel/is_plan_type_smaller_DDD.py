# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_plan_type_smaller_DDD(Variable):
    """ Is this parcel of a plan type smaller DDD."""
    
    def __init__(self, plan_type):
        self.plan_type = plan_type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("plan_type_id")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("plan_type_id") < self.plan_type

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.parcel.is_plan_type_smaller_7000"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')


        parcels_table_name = 'parcels'        
        storage.write_table(
                 table_name=parcels_table_name,
                 table_data={
                    'parcel_id':      array([1, 2, 3, 4, 5, 6]),
                    'plan_type_id': array([9001, 9001, 1001, 1001, 9001, 9001])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        parcels = dataset_pool.get_dataset('parcel')
        
        values = parcels.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([True, True, False, False, True, True])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()