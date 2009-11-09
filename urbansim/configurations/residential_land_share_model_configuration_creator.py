# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class ResidentialLandShareModelConfigurationCreator(object):
    
    _model_name = 'residential_land_share_model'

    def __init__(self,
                dataset = 'gridcell',
                debuglevel = 'debuglevel',
                coefficients_table = 'residential_land_share_model_coefficients',
                specification_table = 'residential_land_share_model_specification',
                estimation_procedure = "opus_core.estimate_linear_regression",
                input_changed_indices = 'changed_indices'
                ):
        self.dataset = dataset
        self.debuglevel = debuglevel
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        self.estimation_procedure = estimation_procedure
        self.input_changed_indices = input_changed_indices
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'index'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': self.dataset,
                    'debuglevel': self.debuglevel,
                    'index': _index,
                    'specification': _specification,
                    'procedure': "'%s'" % self.estimation_procedure
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.%s' % self._model_name: 'ResidentialLandShareModel'
                },
            'init': {'name': 'ResidentialLandShareModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': self.dataset,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _index)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table, 
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients)
                },
            'run': {
                'arguments': {
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'dataset': self.dataset,
                    'debuglevel': self.debuglevel,
                    'index': self.input_changed_indices,
                    'specification': _specification
                    }
                }
            })


from opus_core.tests import opus_unittest 


class TestResidentialLandShareModelConfiguration(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = ResidentialLandShareModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': 'gridcell',
                    'debuglevel': 'debuglevel',
                    'index': 'index',
                    'specification': 'specification',
                    'procedure': "'opus_core.estimate_linear_regression'"
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.residential_land_share_model': 'ResidentialLandShareModel'
                },
            'init': {'name': 'ResidentialLandShareModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'gridcell',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'residential_land_share_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'residential_land_share_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'residential_land_share_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'dataset': 'gridcell',
                    'debuglevel': 'debuglevel',
                    'index': 'changed_indices',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = ResidentialLandShareModelConfigurationCreator(
            dataset = 'dataset',
            debuglevel = -5,
            input_changed_indices = 'input_changed_indices',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': 'dataset',
                    'debuglevel': -5,
                    'index': 'index',
                    'specification': 'specification',
                    'procedure': "'opus_core.estimate_linear_regression'"
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.residential_land_share_model': 'ResidentialLandShareModel'
                },
            'init': {'name': 'ResidentialLandShareModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'dataset',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
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
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'dataset': 'dataset',
                    'debuglevel': -5,
                    'index': 'input_changed_indices',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()