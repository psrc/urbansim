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

import os
import re
import pickle
import shutil
from opus_core.tests import opus_unittest
import tempfile

from opus_core.opus_package import OpusPackage
from opus_core.fork_process import ForkProcess
from psrc.configs.subset_configuration import SubsetConfiguration
from opus_core.misc import does_database_server_exist_for_this_hostname


if does_database_server_exist_for_this_hostname(
        module_name = __name__, 
        hostname = SubsetConfiguration()['input_configuration'].host_name):
    
    class Test(opus_unittest.OpusTestCase):   
        def setUp(self):
            self.config = SubsetConfiguration()
            self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            self.config['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
            self.config['creating_baseyear_cache_configuration'].cache_from_mysql = True
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