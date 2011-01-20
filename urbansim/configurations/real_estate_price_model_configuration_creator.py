# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class RealEstatePriceModelConfigurationCreator(object):    
    _model_name = 'real_estate_price_model'

    def __init__(self,
                debuglevel = 'debuglevel',
                nchunks = 1,
                dataset = 'building',
                outcome_attribute = 'ln_unit_price=ln(urbansim.building.avg_val_per_unit)',
                submodel_string = 'building_type_id',
                filter_variable = 'building.avg_val_per_unit',
                coefficients_table = 'real_estate_price_model_coefficients',
                specification_table = 'real_estate_price_model_specification'
                ):
        self.debuglevel = debuglevel
        self.nchunks = nchunks
        self.dataset = dataset
        self.outcome_attribute = outcome_attribute
        self.submodel_string = submodel_string
        self.filter_variable = filter_variable
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'repm_index'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': self.dataset,
                    'outcome_attribute': "'%s'" % self.outcome_attribute,
                    'debuglevel': self.debuglevel,
                    'index': _index,
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.%s' % self._model_name: 'RealEstatePriceModel'
                },
            'init': {
                'arguments': {
                    'dataset_pool': 'dataset_pool',
                    'debuglevel': self.debuglevel,
                    'filter_attribute': None,
                    'outcome_attribute': "'%s'" % self.outcome_attribute,
                    'submodel_string': get_string_or_None(self.submodel_string)
                    },
                'name': 'RealEstatePriceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': self.dataset,
                    'filter_variable': get_string_or_None(self.filter_variable),
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _index)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table, 
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients)
                },
            'run': {
                'arguments': {
                    'chunk_specification': "{'nchunks':%s}" % self.nchunks,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'dataset': self.dataset,
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestRealEstatePriceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RealEstatePriceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': 'building',
                    'outcome_attribute': "'ln_unit_price=ln(urbansim.building.avg_val_per_unit)'",
                    'debuglevel': 'debuglevel',
                    'index': 'repm_index',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.real_estate_price_model': 'RealEstatePriceModel'
                },
            'init': {
                'arguments': {
                    'dataset_pool': 'dataset_pool',
                    'debuglevel': 'debuglevel',
                    'filter_attribute': None,
                    'outcome_attribute': "'ln_unit_price=ln(urbansim.building.avg_val_per_unit)'",
                    'submodel_string': "'building_type_id'"
                    },
                'name': 'RealEstatePriceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'building',
                    'filter_variable': "'building.avg_val_per_unit'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'real_estate_price_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, repm_index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'real_estate_price_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'real_estate_price_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'chunk_specification': "{'nchunks':1}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'dataset': 'building',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = RealEstatePriceModelConfigurationCreator(
            debuglevel = 9999,
            nchunks = 8888,
            dataset = 'dataset',
            outcome_attribute = 'package.dataset.outcome_attribute',
            submodel_string = 'submodel_string',
            filter_variable = 'dataset.filter_variable',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': 'dataset',
                    'outcome_attribute': "'package.dataset.outcome_attribute'",
                    'debuglevel': 9999,
                    'index': 'repm_index',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.real_estate_price_model': 'RealEstatePriceModel'
                },
            'init': {
                'arguments': {
                    'dataset_pool': 'dataset_pool',
                    'debuglevel': 9999,
                    'filter_attribute': None,
                    'outcome_attribute': "'package.dataset.outcome_attribute'",
                    'submodel_string': "'submodel_string'"
                    },
                'name': 'RealEstatePriceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'dataset',
                    'filter_variable': "'dataset.filter_variable'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, repm_index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'coefficients_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'chunk_specification': "{'nchunks':8888}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'dataset': 'dataset',
                    'debuglevel': 9999,
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()