# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class workerDDD_SSS(Variable):
    """return SSS variable for worker DDD in a household"""
    
    _return_type="float32"

    def __init__(self, number, name):
        self.worker = "worker" + str(number)
        self.var_name = name
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.person.household_id",
                "psrc.person." + self.var_name,
                "psrc.person." + self.worker,
                attribute_label("household","household_id")]

    def compute(self, dataset_pool):
        persons = dataset_pool.get_dataset('person')
        var_names = persons.get_attribute(self.var_name)
        workers = persons.get_attribute(self.worker)
        data = var_names * workers
        household_ids = persons.get_attribute("household_id")
        return self.get_dataset().sum_over_ids(household_ids, data)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.worker1_var_name_hbw_am_drive_alone_from_home_to_work"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5, 6]),
                    'household_id':array([1, 1, 2, 3, 3, 3]),
                    'member_id':array([1, 2, 1, 1, 2, 3]),
                    'worker1':array([1, 0, 1, 0, 0, 1]),
                    'var_name_hbw_am_drive_alone_from_home_to_work':array([5.3,2, 999,0, 1.1,7])
                    },
            )
        
        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = { 
                'person':persons, 
                'household':{ 
                    'household_id':array([1, 2, 3])
                    }
                },
            dataset = 'household' 
            )
            
        should_be = array([5.3, 999, 7])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()