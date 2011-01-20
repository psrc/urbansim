# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class has_eg_DDD_households_with_DDD_nonhome_based_workers(Variable):
    """has equal to or more than DDD surveyed households with DDD nonhome-based workers? """
    
    def __init__(self, number1, number2):
        Variable.__init__(self)
        self.tnumber = number1
        self.household_condition = "has_%s_nonhome_based_workers" % number2
        
    def dependencies(self):
        return ["psrc.household." + self.household_condition,
                "psrc.household.zone_id",
                ]
        
    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        has_right_num_workers = households.get_attribute(self.household_condition)
        zone_ids = households.get_attribute("zone_id")
        return self.get_dataset().sum_over_ids(zone_ids, has_right_num_workers) >= self.tnumber

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.has_eg_1_households_with_1_nonhome_based_workers"
    def test(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':   array([1,  2,  3,  4,  5,  6, 7]),
                    'household_id':array([1, 1, 3, 3, 3, 2, 2]),
                    'member_id':array([1, 2, 1, 2, 3, 1, 2]),
                    'work_nonhome_based':array([1, 0, 1, 0, 1, 1, 0]),
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"person":persons, \
             "zone":{
                     "zone_id":array([1, 2, 3])
                     },
             "household":{ \
                 "household_id":array([1, 2, 3]),
                 "zone_id":array([1, 3, 1]),
                 }}, \
            dataset = "zone")
        should_be = array([1,0,1])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()