# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.tests import opus_unittest
from opus_core.opus_package_info import package
import os
import tempfile
from shutil import rmtree
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.iterative_meta_model import IterativeMetaModel
from opus_core.store.utils.cache_flt_data import CacheFltData
from urbansim.model_coordinators.model_system import ModelSystem

class IterativeMetaModelTests(opus_unittest.OpusTestCase):
    def setUp(self):
        opus_core_path = package().get_opus_core_path()
        cache_dir = os.path.join(opus_core_path, 'data', 'test_cache')
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        run_dir = os.path.join(self.temp_dir, 'tests', 'runs')
        os.makedirs(run_dir)
        self.config = {
            'models': ['my_regression_model', 'my_meta_model'],
            'years': (1981, 1982),
            'base_year': 1980,
            'cache_directory': run_dir,
            'models_configuration': {
                'aging_model': {
                    'controller': {
                         'import': {'opus_core.simple_model': 'SimpleModel'},
                         'init': {'name': 'SimpleModel'},
                         'run': {
                            'arguments': {
                                'dataset': 'household',
                                'expression': "'household.age_of_head + 10'",
                                'outcome_attribute': "'age_of_head'",
                                'dataset_pool': 'dataset_pool'
                            }
                        }
                    }         
                },
                'my_meta_model': {
                    'controller': {
                         'import': {'opus_core.iterative_meta_model': 'IterativeMetaModel'},
                         'init': {'arguments': {'models': ['aging_model'],
                                                'configuration': 'resources',
                                                'datasets_to_preload': ['household']},
                                  'name': 'IterativeMetaModel'},
                         'run': {'arguments': {
                                    'year': 'year',
                                    'condition': "'alldata.aggregate_all(numpy.logical_not(household.age_of_head > 70)) == 0'",
                                }
                         }
                    }
                },
                'my_regression_model': {
                      'controller': {                          
                              'import': {'opus_core.regression_model': 'RegressionModel'},
                              'init': {'arguments': {'dataset_pool': 'dataset_pool'},
                                       'name': 'RegressionModel'},
                              'prepare_for_run': {
                                        'arguments': {
                                             'coefficients_storage': 'base_cache_storage',
                                             'coefficients_table': "'land_price_model_coefficients'", 
                                             'specification_storage': 'base_cache_storage',
                                             'specification_table': "'land_price_model_specification'",
                                                    },
                                        'name': 'prepare_for_run',
                                        'output': '(_specification, _coefficients, dummy)'
                                                },
                                'run': {
                                    'arguments': {
                                        'coefficients': '_coefficients',
                                        'specification': '_specification',
                                        'dataset': 'gridcell'
                                                 }
                                        }
                        }
                    },
            },
            'datasets_to_preload': {'gridcell': {}},
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                    cache_directory_root = run_dir,
                    cache_from_database = False,
                    baseyear_cache = BaseyearCacheConfiguration(years_to_cache = [1980],
                                                                existing_cache_to_copy = cache_dir)
                    ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['urbansim', 'opus_core'],
                ),
            'model_system':'urbansim.model_coordinators.model_system',
        }
        CacheFltData().run(self.config)
     
    def tearDown(self):
        rmtree(self.temp_dir)
        pass
                     
    def test_run_models(self):
        model_system = ModelSystem()
        model_system.run_in_same_process(self.config)
        
if __name__ == "__main__":
    opus_unittest.main()                  
                  
