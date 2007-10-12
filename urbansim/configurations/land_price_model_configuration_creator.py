#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait

from opus_core.configuration import Configuration


class LandPriceModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    dataset = Str('gridcell')
    nchunks = Int(1)
    threshold = Int(1000)
    estimation_procedure = Str("opus_core.estimate_linear_regression")
    
    coefficients_table = Str('land_price_model_coefficients')
    specification_table = Str('land_price_model_specification')
    
    _model_name = 'land_price_model'
    
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
            'init': {'name': 'CorrectedLandPriceModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': self.dataset,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
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
            'init': {'name': 'CorrectedLandPriceModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'gridcell',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'land_price_model_specification'",
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
            'init': {'name': 'CorrectedLandPriceModel'},
            'prepare_for_estimate': {
                'arguments': {
                    'dataset': 'dataset',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
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