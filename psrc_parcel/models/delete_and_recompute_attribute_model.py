# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.variables.variable_name import VariableName
from numpy import ndarray, ones_like, where
from opus_core.logger import logger

class DeleteAndRecomputeAttributeModel(Model):
    """
    The model deletes given attribute of the given dataset.
    """

    def __init__(self, model_name=None, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        if model_name is not None:
            self.model_name = model_name

    def run(self, dataset, attribute, expression = None, dataset_pool = None):
        """
        If 'attribute' is not a known attribute of 'dataset', the model does nothing.
        Otherwise the attribute is deleted. 
        If expression is give, the attribute is recomputed using the expression. 
        Don't use alias in the expression as the alias is set to the attribute name.
        """
        if attribute in dataset.get_known_attribute_names():
            dataset.delete_one_attribute(attribute)
            if expression is not None:
                dataset.compute_variables(["%s = %s" % (attribute, expression)], dataset_pool = dataset_pool)
                dataset.add_primary_attribute(data=dataset[attribute], name=attribute)
        return
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, sqrt, log, zeros

class DeleteAndRecomputeAttributeModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.data = {
            'id': arange(10)+1,
            'attribute':  array([3000,2800,1000,550,600,1000,2000,500,100,1000]),
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'dataset', table_data = self.data)
        self.dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name=['id'])

    def test_delete_and_recompute_attribute_model(self):
        m = DeleteAndRecomputeAttributeModel()
        m.run(self.dataset, 'attr')
        self.assertEqual('attribute' in self.dataset.get_primary_attribute_names(), True)
        m.run(self.dataset, 'attribute', 'dataset.id + 10')
        self.assertEqual('attribute' in self.dataset.get_primary_attribute_names(), True)
        expected_results = self.data["id"] + 10
        results = self.dataset["attribute"]
        self.assertEqual(ma.allequal(expected_results, results), True, 
                         "Error, should_be: %s, but result: %s" % (expected_results, results))

if __name__=="__main__":
    opus_unittest.main()
