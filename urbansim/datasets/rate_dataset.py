# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.session_configuration import SessionConfiguration
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import array, where, int32, float32, ones, zeros, setdiff1d
from numpy import logical_and, reshape, apply_along_axis, maximum
from numpy.random import normal, seed
from opus_core.logger import logger

class RateDataset(UrbansimDataset):

    id_name_default = ['rate_id']
    in_table_name_default = "annual_relocation_rates"
    out_table_name_default = "annual_relocation_rates"
    dataset_name = "rate"
    probability_attribute = "probability_of_relocating"
    attribute_aliases = {}  
    ## to keep backward compatibility, allow using aliases for attributes, 
    ## e.g. 'age' for 'age_of_head'
    
    def __init__(self, what='', resources=None, **kwargs):
        # what is a legacy argument that is not used any more
        UrbansimDataset.__init__(self, resources, **kwargs)
        self.independent_variables = []
        
    def get_rate(self, dataset):
        probability_attribute = self.get_probability_attribute_name()
        column_names = set( self.get_known_attribute_names() ) - set( [ probability_attribute, 'rate_id', '_hidden_id_'] )
        self.independent_variables = list(set([col.rstrip('_min').rstrip('_max') for col in column_names]))
        self._compute_variables_for_dataset_if_needed(dataset, self.independent_variables)
        known_attributes = dataset.get_known_attribute_names()
        prob = -1 + zeros( dataset.size(), dtype='float64')
        for index in range(self.size()):
            indicator = ones( dataset.size(), dtype='bool' )
            for attribute in self.independent_variables:
                alias = self.attribute_aliases.get(attribute)
                if attribute in known_attributes:
                    dataset_attribute = dataset.get_attribute(attribute)
                elif alias in known_attributes:
                    dataset_attribute = dataset.get_attribute(alias)
                else:
                    raise ValueError, "attribute %s used in rate dataset can not be found in dataset" % (attribute, dataset.get_dataset_name())
                if attribute + '_min' in column_names and self.get_attribute(attribute+'_min')[index] != -1:
                    indicator *= dataset_attribute >= self.get_attribute(attribute+'_min')[index]
                if attribute + '_max' in column_names and self.get_attribute(attribute+'_max')[index] != -1:
                    indicator *= dataset_attribute <= self.get_attribute(attribute+'_max')[index]
                if attribute in column_names and self.get_attribute(attribute)[index] != -1:
                    rate_attribute = self.get_attribute(attribute)
                    if rate_attribute[index] != -2:
                        indicator *= dataset_attribute == rate_attribute[index]
                    else: ##all other values not appeared in this column, i.e. the complement set
                        complement_values = setdiff1d( dataset_attribute, rate_attribute )
                        has_one_of_the_complement_value = zeros(dataset_attribute.size, dtype='bool')
                        for value in complement_values:
                            has_one_of_the_complement_value += dataset_attribute == value
                        indicator *= has_one_of_the_complement_value
                    
            prob[logical_and(indicator, prob < 0)] = self.get_attribute(probability_attribute)[index]
            
        if any(prob < 0):
            logger.log_warning('There are %i %ss whose relocation probability is ' % ((prob<0).sum(), dataset.get_dataset_name()) + 
                               'un-specified by the relocation rate dataset. ' +
                               'Their relocation probability is set to 0.' )
            prob[prob < 0] = 0.0
                               
        return prob

    def _compute_variables_for_dataset_if_needed(self, dataset, variable_names):
        #dataset.compute_variables(variable_names)
        for variable in variable_names:
            ## to enable rate_dataset to include computed variables in dataset (e.g. household)
            ## see test_get_rate2 in unittest
            alias = self.attribute_aliases.get(variable)
            known_attributes = dataset.get_known_attribute_names()
            if variable not in known_attributes and alias not in known_attributes:
                dataset_pool = SessionConfiguration().get_dataset_pool()
                dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)
    
    def get_probability_attribute_name(self):
        return self.probability_attribute

    def sample_rates(self, n=100, cache_storage=None, multiplicator=1):
        """ Draw a samples from non-zero rates. """
        minimum_sd = 1e-20
        probs = self.get_attribute(self.get_probability_attribute_name())
        non_zero_probs_idx = where(probs > 0)[0]
        non_zero_probs = probs[non_zero_probs_idx]
        sd = non_zero_probs * (1-non_zero_probs)/float(n)
        def draw_rn (mean_var, l):
            return normal(mean_var[0], mean_var[1], size=l)
        sampled_values = reshape(apply_along_axis(draw_rn, 0, (non_zero_probs, maximum(multiplicator*sd, minimum_sd)), 1),
                                 (non_zero_probs.size,))
        probs[non_zero_probs_idx] = sampled_values.astype(probs.dtype)
        self.add_primary_attribute(name=self.get_probability_attribute_name(), data=probs)
        if cache_storage is not None:
            self.write_dataset(out_storage=cache_storage)
            
from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose
from urbansim.datasets.household_dataset import HouseholdDataset
from opus_core.session_configuration import SessionConfiguration
from urbansim.household.aliases import aliases

aliases += ["per_capita_income = (household.income).astype('float') / household.persons"]

class Tests(StochasticTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        hh_data={
             'household_id': array([  1,  2,  3,  4,  5,  6,  7]),
                    'age':   array([ 20, 20, 30, 60, 79, 45, 20]),
                    'income':array([  0, 20, 26, 15, 15, 55, 20]),
                   'persons':array([  1,  1,  2,  2,  3,  5,  1]),
            'building_type': array([  4, 12, 19, 12, -1, 19,  4])
                    }                                   
        self.hhs = self.init_dataset('households', hh_data, HouseholdDataset)
        
    def init_dataset(self, table_name, table_data, DatasetClass):
        self.storage.write_table(
                table_name=table_name,
                table_data=table_data
            )
        return DatasetClass(in_storage=self.storage, 
                            in_table_name=table_name)
    
    #def tearDown(self):
        #del self.storage
        #del self.hhs

    def test_get_rate1(self):        
        rates_data={
            'rate_id':             array([   1,   2,   3,    4]),
            'persons':             array([   1,   2,   3,   -2]),
        'probability_of_relocating':array([0.4, 0.3, 0.2, 0.05]),
            }
        
        rates = self.init_dataset('rates', rates_data, RateDataset)
        rates.probability_attribute = 'probability_of_relocating'
        #rates._id_names = ['persons']
        expected = array([0.4, 0.4, 0.3, 0.3, 0.2, 0.05, 0.4] )
        results = rates.get_rate(self.hhs)
        
        self.assert_(allclose(results, expected))

    def test_get_rate2(self):        
        rates_data={
            'rate_id':               array([   1,   2,   3,    4]),
            'per_capita_income_min': array([   0,  11,  16,   -1]),
            'per_capita_income_max': array([  10,  15,  19,   -1]),            
        'probability_of_relocating':  array([0.4, 0.3, 0.2, 0.05]),
            }
        
        rates = self.init_dataset('rates', rates_data, RateDataset)
        rates.probability_attribute = 'probability_of_relocating'
        
        ## because per_capita_income needs to be computed for households,
        ## package_order needs to be specified in SessionConfiguration
        SessionConfiguration(new_instance=True,
                             package_order=['urbansim'],
                             in_storage=self.storage)
        
        expected = array([0.4, 0.05, 0.3, 0.4, 0.4, 0.3, 0.05] )
        results = rates.get_rate(self.hhs)
        
        self.assert_(allclose(results, expected))
        
    def test_get_rate3(self):        
        rates_data={
                    'rate_id':   array([  2,   3,   4,   5,   1]),
                    'age_min':   array([  0,   0,  31,  31,  -1]),
                    'age_max':   array([ 30,  30,  -1,  -1,  -1]),
                    'income_min':array([  0,  26,   0,  26,  -1]),
                    'income_max':array([ 25,  -1,  25,  -1,  -1]),
                'building_type': array([ -2,  -2,  -2,  -2,   4]),
    'probability_of_relocating':array([ 0.1, 0.4, 0.3,0.05, 0.0]),
            }                                              
        
        rates = self.init_dataset('rates', rates_data, RateDataset)
        rates.probability_attribute = 'probability_of_relocating'

        expected = array([0.0, 0.1, 0.4, 0.3, 0.3, 0.05, 0.0] )
        results = rates.get_rate(self.hhs)
        
        self.assert_(allclose(results, expected))
        
        
if __name__=='__main__':
    opus_unittest.main()
