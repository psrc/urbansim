# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.variables.variable_name import VariableName
from numpy import ndarray, ones_like, where
from opus_core.logger import logger

class SimpleModel(Model):
    """
    The model computes a given expression on a dataset (or a value array) and assigns the result to the outcome_attribute. 
    The outcome_attribute is set as primary. If it is missing, the alias of the expression is taken.
    """

    def __init__(self, model_name=None, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        if model_name is not None:
            self.model_name = model_name

    def run(self, dataset, expression=None, outcome_attribute=None, outcome_values=None, 
            dataset_filter=None, dataset_pool=None, year = None, year_condition = None):
        """
        dataset_filter - if it is specified and outcome_attribute exists, only update values for dataset records whose dataset_filter is True.
        outcome_values - if expression is None and outcome_values is an numpy array of the same size as dataset, 
                        the outcome_values are assigned to outcome_attribute.
        year, year_condition - if both are given, the model is applied only if eval(year + year_condition) is true.
        """
        if year is not None and year_condition is not None:
            if not eval(str(year) + year_condition):
                return
        if not expression:
            if isinstance(outcome_values, ndarray) and outcome_values.size == dataset.size():
                values = outcome_values
            else:
                raise Exception("If expression is None, outcome values must be an ndarray of the same size as dataset.")
        else:
            values = dataset.compute_variables([expression], dataset_pool=dataset_pool)

        #outcome = values
        ddtype = values.dtype  #default dtype
        if outcome_attribute is None:
            outcome_attribute = VariableName(expression).get_alias()
        elif outcome_attribute in dataset.get_known_attribute_names():
            outcome = dataset[outcome_attribute]
            ddtype = outcome.dtype  #default dtype
        else:
            try:
                outcome = dataset.compute_variables(outcome_attribute, dataset_pool=dataset_pool)
                ddtype = outcome.dtype  #default dtype
            except LookupError:
                outcome=values

        if dataset_filter is not None:
            if type(dataset_filter)==str:
                filter_index = where(dataset.compute_variables([dataset_filter], 
                                                               dataset_pool=dataset_pool))[0]
            elif isinstance(dataset_filter, ndarray):
                filter_index = dataset_filter
            logger.log_status("Values of %s records to be updated." % filter_index.size)
            outcome[filter_index] = (values[filter_index]).astype(ddtype)
        else:
            outcome = values.astype(ddtype)
            
        #if outcome_attribute in dataset.get_known_attribute_names():
        #    dataset.delete_one_attribute(outcome_attribute)
        dataset.add_primary_attribute(data=outcome, name=outcome_attribute)
            
        return outcome
    
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, sqrt, log, zeros

class SimpleModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.data = {
            'id': arange(10)+1,
            'attribute':  array([3000,2800,1000,550,600,1000,2000,500,100,1000]),
            'sqrt_outcome': zeros(10)
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'dataset', table_data = self.data)
        self.dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name=['id'])

    def test_simple_model(self):
        m = SimpleModel()
        m.run(self.dataset, 'sqrt(dataset.attribute)', outcome_attribute='sqrtattr')
        self.assertEqual(ma.allclose(self.dataset.get_attribute('sqrtattr'), sqrt(self.data['attribute'])), True)
        self.assertEqual('sqrtattr' in self.dataset.get_primary_attribute_names(), True)

    def test_simple_model_with_filter(self):
        m = SimpleModel()
        m.run(self.dataset, 'sqrt(dataset.attribute)', outcome_attribute='sqrt_outcome', dataset_filter='dataset.attribute>1000')
        expected = array([1, 1, 0, 0, 0, 0, 1, 0, 0, 0]) * sqrt(self.data['attribute'])
        self.assertEqual(ma.allclose(self.dataset.get_attribute('sqrt_outcome'), 
                                     expected), True)
        self.assertEqual('sqrt_outcome' in self.dataset.get_primary_attribute_names(), True)

    def MASKEDtest_simple_model_with_random_filter(self):
        m = SimpleModel()
        m.run(self.dataset, 'sqrt(dataset.attribute)', 
              outcome_attribute='sqrt_outcome', 
              dataset_filter='(dataset.attribute>=1000) & (random_like(dataset.attribute)<=0.5)',
             )
        con_filter = self.dataset['attribute']>=1000
        results = self.dataset['sqrt_outcome'][con_filter]
        expected = sqrt(self.data['attribute'])[con_filter]
        #test half of the elements passing filter are being sqrt
        self.assertEqual((results==expected).sum(), expected.size/2)
        self.assertEqual((results!=expected).sum(), expected.size/2)
        
    def test_simple_model_without_outcome_attribute(self):
        m = SimpleModel()
        m.run(self.dataset, 'lattr = ln(dataset.attribute)')
        self.assertEqual(ma.allclose(self.dataset.get_attribute('lattr'), log(self.data['attribute'])), True)
        self.assertEqual('lattr' in self.dataset.get_primary_attribute_names(), True)
        
    def test_simple_model_with_outcome_values(self):
        m = SimpleModel()
        m.run(self.dataset,  outcome_attribute='iniattr', outcome_values=zeros(10)-1)
        self.assertEqual(ma.allclose(self.dataset.get_attribute('iniattr'), array(10*[-1])), True)
        self.assertEqual('iniattr' in self.dataset.get_primary_attribute_names(), True)
        # run with filter
        m.run(self.dataset,  outcome_attribute='iniattr', outcome_values=arange(10)+1, dataset_filter='dataset.attribute>1000')
        expected = array([1, 2, -1, -1, -1, -1, 7, -1, -1, -1])
        self.assertEqual(ma.allclose(self.dataset.get_attribute('iniattr'), expected), True)
        
                               
if __name__=="__main__":
    opus_unittest.main()
