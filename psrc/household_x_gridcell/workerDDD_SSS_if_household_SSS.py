# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import newaxis
from opus_core.logger import logger

class workerDDD_SSS_if_household_SSS(Variable):
    """SSS (the first SSS) variable for worker1 if household condition SSS (the second SSS) is true, 0 otherwise"""    

    default_value = 180.0
    def __init__(self, number, var_name, condition):
        self.var_name = "worker" + str(number) + "_" + var_name
        self.condition = condition
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.household." + self.condition,
                "psrc.household_x_gridcell." + self.var_name]

    def compute(self, dataset_pool):
        household_x_gridcells = self.get_dataset()
        return household_x_gridcells.get_attribute_of_dataset(self.condition)[:, newaxis] * \
               household_x_gridcells.get_attribute(self.var_name)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset   
from opus_core.storage_factory import StorageFactory 
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_gridcell.worker1_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers"
    
    def setUp(self):
        logger.enable_hidden_error_and_warning_words()
        
    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':  array([1, 2, 3, 4, 5, 6]),
                    'household_id':array([1, 1, 2, 3, 3, 3]),
                    'member_id':  array([1, 2, 1, 1, 2, 3]),
                    'worker1':   array([1, 0, 1, 0, 0, 1]),
                    'job_zone_id':array([1, 3, 3, 2, 1, 3])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'gridcell':{
                    'gridcell_id':array([1,2,3,4]),
                    'zone_id':array([1, 1, 3, 2])
                    },
                'household':{
                    'household_id':array([1,2,3,4,5]),
                    'zone_id':array([3, 1, 1, 1, 2]),
                    'cars':   array([0, 2, 2, 0, 1]),
                    'number_of_nonhome_based_workers':array([1, 3, 1, 1, 1])
                    },
                'person':persons,
                'travel_data':{
                    'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                    'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                    'am_total_transit_time_walk':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])}
                    },
            dataset = 'household_x_gridcell',
            )
            
        default_value = workerDDD_SSS_if_household_SSS.default_value
        should_be = array([[3.3, 3.3, 1.1, 0.7], [4.4, 4.4, 2.2, 8.7], 
                           [0, 0, 0, 0], [default_value, default_value, default_value, default_value],
                           [0, 0, 0, 0]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()