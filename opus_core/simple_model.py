# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.variables.variable_name import VariableName

class SimpleModel(Model):
    """
    The model computes a given expression on a dataset and assigns the result to the outcome_attribute. 
    The outcome_attribute is set as primary. If it is missing, the alias of the expression is taken.
    """
    def run(self, dataset, expression, outcome_attribute=None, dataset_pool=None):
        values = dataset.compute_variables([expression], dataset_pool=dataset_pool)
        if outcome_attribute is None:
            outcome_attribute = VariableName(expression).get_alias()
        #if outcome_attribute in dataset.get_known_attribute_names():
        #    dataset.delete_one_attribute(outcome_attribute)
        dataset.add_primary_attribute(data=values, name=outcome_attribute)
        print "Min: %s" % dataset[outcome_attribute].min()
        return values
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, sqrt, log

class SimpleModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.data = {
            'id': arange(10)+1,
            'attribute':  array([3000,2800,1000,550,600,1000,2000,500,100,1000])
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'dataset', table_data = self.data)
        self.dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name=['id'])

    def test_simple_model(self):
        m = SimpleModel()
        m.run(self.dataset, 'sqrt(dataset.attribute)', outcome_attribute='sqrtattr')
        self.assertEqual(ma.allclose(self.dataset.get_attribute('sqrtattr'), sqrt(self.data['attribute'])), True)
        self.assertEqual('sqrtattr' in self.dataset.get_primary_attribute_names(), True)
        
    def test_simple_model_without_outcome_attribute(self):
        m = SimpleModel()
        m.run(self.dataset, 'lattr = ln(dataset.attribute)')
        self.assertEqual(ma.allclose(self.dataset.get_attribute('lattr'), log(self.data['attribute'])), True)
        self.assertEqual('lattr' in self.dataset.get_primary_attribute_names(), True)
                                     
if __name__=="__main__":
    opus_unittest.main()