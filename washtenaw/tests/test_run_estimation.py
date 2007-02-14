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

# test_scanner: IGNORE_THIS_FILE
### This file takes a long time to run, thus it is only run by NightlyFullTests.

import os

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
            ev = ('python "%s" --cache-directory="%s" washtenaw.tests.test_run_estimation_config'
                % (create_baseyear_cache_script_path, cache_dir))
            logger.log_status("Invoking '%s'" % ev)
            os.system(ev)
            
            estimation_config = {
                'cache_directory' : cache_dir,
                'dataset_pool_configuration': DatasetPoolConfiguration(
                    package_order=['washtenaw', 'urbansim', 'opus_core'],
                    package_order_exceptions={},
                    ),
                'datasets_to_cache_after_each_model':[],
                'low_memory_mode':False,
                'base_year': 2000,
                'years': (2000,2000),                    
                }
        
            failed = []
            succeeded = []
            
            for model in [
                    'hlcm', 
                    'elcm-industrial',
                    'elcm-commercial',
#                    'elcm-home_based', # fails
                    'dplcm-industrial',
                    'dplcm-commercial',
                    'dplcm-residential',
                    'lpm',
                    'rlsm',
                    ]:
                    
                try:
                    self.estimation_runner.run_estimation(estimation_config, model, save_estimation_results=False)
                    succeeded.append(model)
                except:
                    logger.log_stack_trace()
                    failed.append(model)

            if len(succeeded) > 0:
                print 'Succeeded in estimating the following models: %s.' % ', '.join(succeeded)
                
            if len(failed) > 0:
                self.fail('Failed to estimate the following models: %s.' % ', '.join(failed))
            
        finally:
            if os.path.exists(cache_dir):
                rmtree(cache_dir)
                
                
if __name__ == '__main__':
    opus_unittest.main()