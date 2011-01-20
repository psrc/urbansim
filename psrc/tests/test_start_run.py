# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import re
import pickle
import shutil
from opus_core.tests import opus_unittest
import tempfile

from opus_core.fork_process import ForkProcess
from psrc.configs.subset_configuration import SubsetConfiguration

class Test(opus_unittest.OpusIntegrationTestCase):   
    def setUp(self):
        self.config = SubsetConfiguration()
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.config['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        self.config['creating_baseyear_cache_configuration'].cache_from_database = True
        self.config['models'] = [
            'land_price_model',
            ]
        self.config['years'] = (2001, 2001)
        self.config['cache_directory'] = os.path.join(self.temp_dir, 'urbansim_cache')
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_start_run_via_pickle(self):
        """A weak test of start_run - does it crash?"""
        ForkProcess().fork_new_process('opus_core.tools.start_run', self.config)       

if __name__=="__main__":
    opus_unittest.main()