# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# test_scanner: IGNORE_THIS_FILE
### This file takes a long time to run, thus it is only run by NightlyFullTests.

import os, sys

from shutil import rmtree
from tempfile import mkdtemp

### TODO: There really neeeds to be a better way to do this import.
from opus_core.tests import opus_unittest

from opus_core.logger import logger
from opus_core.tools.create_baseyear_cache import __file__ as create_baseyear_cache_script_path

from psrc.estimation.run_estimation import EstimationRunner
from psrc.configs.baseline import Baseline
from psrc.tests.test_run_estimation_in_new_process import __file__ as test_run_estimation_in_new_process_script_path


class TestRunEstimation(opus_unittest.OpusIntegrationTestCase):
    def setUp(self):
        self.estimation_runner = EstimationRunner()
        
    def tearDown(self):
        pass
    
    def test_run_estimation_on_each_model(self):
        cache_dir = mkdtemp(prefix='test_estimation_runner_tmp')
        try:
            # Cache to a temporary folder.
            ev = ('%s "%s" psrc.tests.test_run_estimation_config --cache-directory="%s"' 
                % (sys.executable, create_baseyear_cache_script_path, cache_dir))
            logger.log_status("Invoking '%s'" % ev)
            return_code = os.system(ev)
            
            if return_code > 0:
                raise EnvironmentError('Failed while creating the baseyear cache '
                    'needed to run PSRC estimation tests.')

            failed = []
            succeeded = []
            
            for model in [
                    ('HBCM','HBCM', 'home_based_choice_model'),
                    #('AOCM','AOCM', 'auto_ownership_choice_model'),
                    ('HLCM','HLCM', 'household_location_choice_model'),
                    #('WHLCM','WHLCM', 'worker_specific_household_location_choice_model'), #HLCM with worker specific accessibility variables 
                    ('Industrial ELCM','ELCM', 'employment_location_choice_model', 'industrial', False), # uses general ELCM and therefore type will not be added to the model name
                    ('Commercial ELCM','ELCM', 'employment_location_choice_model', 'commercial', False), 
                    ('Home-based ELCM','ELCM', 'employment_location_choice_model', 'home_based', True), # we don't know exactly why, but this has to be True to get specification data from file and not the cache.
                    #('RWZCM','RWZCM', 'workplace_choice_model_for_resident', 'dummy'),
                    ('LPM','LPM', 'land_price_model'),
                    ('RLSM','RLSM', 'residential_land_share_model'),
                    ('Industrial DPLCM','DPLCM', 'development_location_choice_model', 'industrial'),
                    ('Commercial DPLCM','DPLCM', 'development_location_choice_model', 'commercial'),
                    ('Residential DPLCM','DPLCM', 'development_location_choice_model', 'residential'),
                    ]:
                
                model_slightly_verbose_name = model[0]  
                model_abbreviation = model[1]
                model_verbose_name = model[2]
                
                try:
                    model_type = model[3]    
                except: 
                    model_type = ''
                
                try:
                    model_unknown_boolean = model[4]    
                except: 
                    model_unknown_boolean = ''
                
                ev = ('%s "%s" "%s" %s %s %s %s'
                    % (sys.executable, 
                       test_run_estimation_in_new_process_script_path,
                       cache_dir,
                       model_abbreviation,
                       model_verbose_name,
                       model_type,
                       model_unknown_boolean
                       )
                   )
                
                logger.log_status("Invoking '%s'" % ev)
                return_value = os.system(ev) 

                if return_value == 0:
                    succeeded.append(model_slightly_verbose_name)
                else:
                    failed.append(model_slightly_verbose_name)
            
            if len(succeeded) > 0:
                print 'Succeeded in estimating the following models: %s.' % ', '.join(succeeded)
                
            if len(failed) > 0:
                self.fail('Failed to estimate the following models: %s.' % ', '.join(failed))
            
        finally:
            if os.path.exists(cache_dir):
                rmtree(cache_dir)

if __name__ == '__main__':
    opus_unittest.main()