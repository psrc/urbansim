# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_buildings(Variable):
    """Number of buildings in zones"""
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("building", "zone_id")]

    def compute(self, dataset_pool):
        agents = dataset_pool.get_dataset("building")
        return self.get_dataset().sum_dataset_over_ids(agents, constant=1)

    def post_check(self,  values, arguments=None):
        size = arguments["building"].size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_buildings"
    def test(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name = 'zones',
            table_data = {
                'zone_id': array([1,2,3,4,5]),
            }
        )
        storage.write_table(
            table_name = 'buildings',
            table_data = {
                'building_id': array([1, 2, 3, 4, 5, 6]),
                'zone_id': array([1, 2, 3, 4, 2, 2]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('zone')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([1, 3, 1, 1, 0])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()