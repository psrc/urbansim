# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import newaxis
from opus_core.logger import logger

class workerDDD_SSS_if_worker_SSS(Variable):
    """SSS (the first SSS) variable for worker1 if household condition SSS (the second SSS) is true, 0 otherwise"""    

    default_value = 180.0
    def __init__(self, number, var_name, condition):
        self.var_name = "worker" + str(number) + "_" + var_name
        self.condition = "worker" + str(number) + "_" + condition
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.household." + self.condition,
                "transit_accessibility.household_x_parcel." + self.var_name]

    def compute(self, dataset_pool):
        household_x_parcels = self.get_dataset()
        return household_x_parcels.get_attribute_of_dataset(self.condition)[:, newaxis] * \
               household_x_parcels.get_attribute(self.var_name)
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

 
class TestsHouseholdParcelWorkerDddSssIfWorkerSss(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit"
    
    def setUp(self):
        logger.enable_hidden_error_and_warning_words()

    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='persons',
            table_data={
                'person_id':array([1,  2,  3,  4,  5,  6]),                                
                'household_id':array([1,  1,  2,  3,  3,  3]),
                'member_id':array([1,  2,  1,  1,  2,  3]),
                'worker1':array([1,  0,  1,  0,  0,  1]),
                'uses_transit':array([1,  1,  1,  1,  0,  0]),
                'work_place_zone_id':array([1,  3,  3,  2,  1,  3])
            }
        )
        storage.write_table(
            table_name='parcels',
            table_data={
                'parcel_id':array([1,2,3,4]),
                'zone_id':array([1, 1, 3, 2]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'zone_id':array([3, 1, 1, 1, 2]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_total_transit_time_walk':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['transit_accessibility', 'psrc', 'urbansim', 'opus_core'],
                                   storage=storage)
        
        gridcell = dataset_pool.get_dataset('household_x_parcel')
        
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([[3.3, 3.3, 1.1, 0.7], 
                           [4.4, 4.4, 2.2, 8.7], 
                           [0, 0, 0, 0], 
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]])
        
        self.assert_(ma.allclose( values, should_be, rtol=1e-7), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()