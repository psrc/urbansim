# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class LandPriceModelConfigurationCreator(object):    
    _model_name = 'land_price_model'

    def __init__(self,
                debuglevel = 'debuglevel',
                nchunks = 1,
                dataset = 'gridcell',
                submodel_string = "development_type_id",
                filter = "urbansim.gridcell.is_in_development_type_group_developable",
                coefficients_table = 'land_price_model_coefficients',
                specification_table = 'land_price_model_specification',
                filter_for_estimation = "urbansim.gridcell.total_land_value",
                threshold = 1000,
                estimation_procedure = "opus_core.estimate_linear_regression",
                run_config = None, # additional arguments passed to simulation modules
                estimate_config = None, # additional arguments passed to estimation modules
                ):
        self.debuglevel = debuglevel
        self.nchunks = nchunks
        self.dataset = dataset
        self.threshold = threshold
        self.estimation_procedure = estimation_procedure
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        self.submodel_string = submodel_string
        self.filter = filter
        self.filter_for_estimation = filter_for_estimation
        self.run_config = run_config
        self.estimate_config = estimate_config
        
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
                'urbansim.models.corrected_%s' % self._model_name: 'CorrectedLandPriceModel'
                },
            'init': {'name': 'CorrectedLandPriceModel',
                     'arguments': {
                        'filter': "'%s'" % self.filter,
                        'submodel_string': "'%s'" % self.submodel_string,
                        'run_config': self.run_config,
                        'estimate_config': self.estimate_config,
                                   }
                     },
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': self.dataset,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    'filter_variable': "'%s'" % self.filter_for_estimation,
                    'threshold': self.threshold,
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
                    'n_simulated_years': "year-base_year",
                    'specification': _specification,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestLandPriceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = LandPriceModelConfigurationCreator()
        
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
                'urbansim.models.corrected_land_price_model': 'CorrectedLandPriceModel'
                },
            'init': {'name': 'CorrectedLandPriceModel',
                     'arguments':{
                           'filter': "'urbansim.gridcell.is_in_development_type_group_developable'",
                           'submodel_string': "'development_type_id'",
                           'run_config': None,
                           'estimate_config': None,
                                  }
                     },
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'gridcell',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'land_price_model_specification'",
                    'filter_variable': "'urbansim.gridcell.total_land_value'",
                    'threshold': 1000
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'land_price_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'land_price_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'chunk_specification': "{'nchunks':1}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'dataset': 'gridcell',
                    'debuglevel': 'debuglevel',
                    'n_simulated_years': "year-base_year",
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = LandPriceModelConfigurationCreator(
            debuglevel = 9999,
            dataset = 'dataset',
            nchunks = 8888,
            threshold = 7777,
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            run_config={"aaa": "bbb"},
            estimate_config = {}
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'data_objects': 'datasets',
                    'dataset': 'dataset',
                    'debuglevel': 9999,
                    'index': 'index',
                    'specification': 'specification',
                    'procedure': "'opus_core.estimate_linear_regression'"
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.corrected_land_price_model': 'CorrectedLandPriceModel'
                },
            'init': {'name': 'CorrectedLandPriceModel',
                     'arguments':{
                           'filter': "'urbansim.gridcell.is_in_development_type_group_developable'",
                           'submodel_string': "'development_type_id'",
                           'run_config': {"aaa": "bbb"},
                           'estimate_config': {},
                                  }},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'dataset',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
                    'filter_variable': "'urbansim.gridcell.total_land_value'",
                    'threshold': 7777,
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'coefficients_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
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
                    'n_simulated_years': 'year-base_year',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()