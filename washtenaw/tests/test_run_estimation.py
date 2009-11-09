# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# test_scanner: IGNORE_THIS_FILE
### This file takes a long time to run, thus it is only run by NightlyFullTests.

import os, sys

from shutil import rmtree
from tempfile import mkdtemp

from opus_core.tests import opus_unittest

from opus_core.logger import logger
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.tools.create_baseyear_cache import __file__ as create_baseyear_cache_script_path

from washtenaw.estimation.run_estimation import EstimationRunner


class TestRunEstimation(opus_unittest.TestCase):
    def setUp(self):
        self.estimation_runner = EstimationRunner()
        
    def tearDown(self):
        pass
        
    def test_run_estimation(self):
        cache_dir = mkdtemp(prefix='test_washtenaw_run_estimation_tmp')
        try:
            # Cache to a temporary folder.
            ev = ('%s "%s" --cache-directory="%s" washtenaw.tests.test_run_estimation_config'
                % (sys.executable, create_baseyear_cache_script_path, cache_dir))
            logger.log_status("Invoking '%s'" % ev)
            return_code = os.system(ev)
            
            if return_code > 0:
                raise EnvironmentError('Failed while creating the baseyear cache '
                    'needed to run Washtenaw estimation tests.')
            
            estimation_config = {
                'cache_directory' : cache_dir,
                'dataset_pool_configuration': DatasetPoolConfiguration(
                    package_order=['washtenaw', 'urbansim', 'opus_core'],
                    ),
                'datasets_to_cache_after_each_model':[],
                'low_memory_mode':False,
                'base_year': 2000,
                'years': (2000,2000),                    
                }
        
            failed = []
            succeeded = []
            
            for model_name in [
                    'lpm',
                    'hlcm', 
                    'elcm-industrial',
                    'elcm-commercial',
#                    'elcm-home_based', # fails
                    'dplcm-industrial',
                    'dplcm-commercial',
                    'dplcm-residential',
                    'rlsm',
                    ]:
                    
                try:
                    self.estimation_runner.run_estimation(estimation_config, model_name, save_estimation_results=False)
                    succeeded.append(model_name)
                except:
                    logger.log_stack_trace()
                    failed.append(model_name)

            if len(succeeded) > 0:
                print 'Succeeded in estimating the following models: %s.' % ', '.join(succeeded)
                
            if len(failed) > 0:
                self.fail('Failed to estimate the following models: %s.' % ', '.join(failed))
            
        finally:
            if os.path.exists(cache_dir):
                rmtree(cache_dir)
                
                
if __name__ == '__main__':
    opus_unittest.main()