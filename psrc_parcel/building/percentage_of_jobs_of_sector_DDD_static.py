# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array
from opus_core.variables.variable import Variable

class percentage_of_jobs_of_sector_DDD_static(Variable):
    """ Percentage of jobs of sector DDD in buildings taken from the base year."""
    _return_type="float32"
    sector_building_type_distribution = {
        #         0    1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22 
        1: array([0, 3.8,    0, 10.6,    0,    0,    0,    0,  4.9,    0,    0,    0,    0, 12.8,  2.7,    0,    0,    0,    0, 36.4,  2.5, 11.3,  8.9]),                         
        2: array([0,   0,    0, 10.2,    0,    0,    0,    0,  5.1,    0,    0,    0,    0, 18.3,  1.8,    0,    0,    0,  1.1, 33.8,  1.0, 17.8,    0]),                         
        3: array([0,   0,  1.4,  4.4,    0,  2.2,    0,    0, 33.5,    0,    0,    0,    0, 25.2,    0,    0,  1.4,    0,    0,  3.5,  1.4,  9.9, 14.2]),                         
        4: array([0,   0,    0, 10.3,    0,  9.2,    0,    0, 23.6,    0,    0,    0,    0, 17.3,    0,    0,    0,    0,    0,  5.4,  1.0, 28.1,    0]),                         
        5: array([0,   0,    0, 10.8,    0,    0,    0,    0, 27.7,    0,    0,    0,    0, 12.5,    0,    0,    0,    0,  1.1,  4.2,  2.4, 34.5,    0]),                         
        6: array([0,   0,    0, 10.7,    0,  1.1,    0,    0,  8.3,    0,    0,    0,    0, 18.7,    0,    0,    0,    0,    0, 11.0,    0, 42.4,    0]),                         
        7: array([0,   0,    0, 59.3,    0,    0,    0,    0,  1.5,    0,    0,    0,    0, 12.0,    0,    0,    0,    0,    0,    0,    0,  9.5,    0]),                         
        8: array([0,   0,    0, 12.6,    0,  1.3,    0,    0, 10.7,    0,    0,    0,    0, 27.5,    0,    0,    0,    0,  1.5,    0,    0, 32.6,    0]),                         
        9: array([0,   0,  1.9, 21.1,    0,  1.2,    0,    0,  2.3,    0,    0,    0,    0, 40.4,  1.1,    0,    0,    0,  1.4, 10.1,  2.1, 13.8,    0]),                         
       10: array([0,   0,    0, 13.7,    0, 14.8,    0,    0,  2.6,    0,  1.2,    0,    0, 48.5,    0,    0,  1.5,    0,    0,    0,    0,  4.8,    0]),                         
       11: array([0,   0,    0, 12.3,    0,    0,    0,    0,  2.3,    0,    0,    0,    0, 67.2,    0,    0,  3.2,    0,    0,    0,    0,  3.0,    0]),                         
       12: array([0,   0,    0, 13.7,    0,    0,    0,    0,  3.0,    0,  1.0,    0,    0, 56.3,    0,    0,  1.4,    0,    0,    0,    0,  4.0,    0]),                         
       13: array([0,   0,    0, 11.4,    0,  1.3,    0,  1.5,  2.4,    0,  1.2,    0,    0, 47.0,    0,    0,    0,    0,  1.2,    0,    0,  7.8,    0]),                         
       14: array([0,   0,  1.0, 59.3,    0,  1.2,    0,    0,  1.3,    0,  2.3,    0,    0, 11.5,    0,    0,  1.3,    0,  1.2,    0,    0,  4.4,  1.5]),                         
       15: array([0,   0,  1.5,  9.7,    0,  1.5,    0,    0,  4.0,    0,    0,    0,    0, 25.9,  1.0,    0,  1.3,    0, 10.8,    0,    0, 10.9,    0]),                         
       16: array([0,   0,  1.0,  9.5,    0,  1.3,    0, 18.2,  3.3,    0,    0,    0,    0, 34.1,    0,    0,  1.3,    0,  2.2,    0,    0,  5.7,    0]),                         
       17: array([0,   0,  1.4, 33.2,    0,  1.2,    0,    0,  2.9,    0,  2.2,    0,    0, 14.9,  1.1,    0,  1.2,  4.9,  1.0,    0,    0,  6.4,  1.0]),                         
       18: array([0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0]),                         
       19: array([0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0]),
       20: array([0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0])                         
                                        }
    
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["building.building_type_id"]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        distr = self.sector_building_type_distribution[self.sector_id]/100.
        return distr[ds["building_type_id"]]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.building.percentage_of_jobs_of_sector_9_static"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
  
        storage.write_table(
                 table_name='buildings',
                 table_data={
                    'building_id':       array([1, 2, 3, 4, 5, 6, 7]),
                    'building_type_id':  array([3, 22, 3, 5, 13, 13, 8])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        buildings = dataset_pool.get_dataset('building')
        
        values = buildings.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([21.1, 0, 21.1, 1.2, 40.4, 40.4, 2.3 ])/100.0
        self.assert_(ma.allclose(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()