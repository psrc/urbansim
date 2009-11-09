# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import ma
from numpy import array

from opus_core.model import Model


class TestModelA(Model):
    """
    The purpose of this model is simply to run it and see that something changed.
    """
    model_name = 'Test Model A'
    
    def run(self, input_storage, table_name):
        results = input_storage.load_table(table_name=table_name)
        
        results['test_attribute'] = results['test_attribute'] + 1
        
        input_storage.write_table(table_name = table_name, table_data = results)


from opus_core.tests import opus_unittest

from opus_core.storage_factory import StorageFactory


class test_model_a_tests(opus_unittest.OpusTestCase):
    def test(self):
        model = TestModelA()
        
        table_name = 'test_db'
            
        input_storage = StorageFactory().get_storage('dict_storage')
        input_storage.write_table(
            table_name = table_name,
            table_data = {
                'test_attribute': array([0,6,1]),
                }
            )

        model.run(input_storage, table_name)
        
        results = input_storage.load_table(table_name=table_name)
        
        self.assert_(ma.allequal(results['test_attribute'], array([1,7,2])))
            
            
if __name__ == '__main__':
    opus_unittest.main()