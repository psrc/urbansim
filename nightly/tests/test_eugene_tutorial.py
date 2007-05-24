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
import sys

from shutil import rmtree
from tempfile import mkdtemp

from opus_core.fork_process import ForkProcess
from opus_core.misc import create_import_for_camel_case_class

from eugene.configs.baseline import Baseline


eugene_tutorial_cache_path = sys.argv[1]

temp_output_dir = mkdtemp(prefix='nightly_release_test_eugene_tutorial')
try:
    config = Baseline()
    
    base_year = config['base_year']
        
    config['creating_baseyear_cache_configuration'].cache_from_mysql = False
    config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = eugene_tutorial_cache_path
    config['cache_directory'] = temp_output_dir
    config['years'] = (base_year + 1, base_year + 2)
    
    if not len(range(config['years'][0], config['years'][1]+1)) > 0:
        raise Exception('Nothing to simulate!')
    
    try:
        ForkProcess().fork_new_process('opus_core.tools.start_run', resources=config)
        
    except StandardError:
        raise Exception('Simulation on Eugene cache failed!')

finally:
    if os.path.exists(temp_output_dir):
        rmtree(temp_output_dir)