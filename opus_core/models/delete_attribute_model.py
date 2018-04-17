# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.variables.variable_name import VariableName
from numpy import ndarray, ones_like, where
from opus_core.logger import logger

class DeleteAttributeModel(Model):
    """
    The model deletes given attribute of the given dataset.
    """

    def __init__(self, model_name=None, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        if model_name is not None:
            self.model_name = model_name

    def run(self, dataset, attribute, write_to_cache = False):
        """
        If 'attribute' is not a known attribute of 'dataset', the model does nothing.
        Otherwise the attribute is deleted.
        """
        if attribute in dataset.get_known_attribute_names():
            dataset.delete_one_attribute(attribute)
            if write_to_cache:
                # in order not to have the deleted attributes in cache from previous flushings
                table_name = dataset._get_in_table_name_for_cache()
                dataset.attribute_cache.delete_table(table_name)
                dataset.write_dataset(attributes=dataset.get_primary_attribute_names(), 
                                      out_storage = dataset.attribute_cache, 
                                      out_table_name = table_name)        
        return
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, sqrt, log, zeros

class DeleteAttributeModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.data = {
            'id': arange(10)+1,
            'attribute':  array([3000,2800,1000,550,600,1000,2000,500,100,1000]),
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'dataset', table_data = self.data)
        self.dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name=['id'])

    def test_delete_attribute_model(self):
        m = DeleteAttributeModel()
        m.run(self.dataset, 'attr')
        self.assertEqual('attribute' in self.dataset.get_primary_attribute_names(), True)
        m.run(self.dataset, 'attribute')
        self.assertEqual('attribute' in self.dataset.get_primary_attribute_names(), False)

if __name__=="__main__":
    opus_unittest.main()
