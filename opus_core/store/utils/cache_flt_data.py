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

from shutil import copytree, rmtree

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

class CacheFltData(Model):
    """Get data from a flt storage into a cache.
    """
    def run(self, config):
        input_directory = config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy

        logger.log_status("Caching files from '%s' \nto '%s'." 
            % (input_directory, config['cache_directory']))

        if os.path.exists(config['cache_directory']):
            rmtree(config['cache_directory'])
            
        years = config['creating_baseyear_cache_configuration'].baseyear_cache.years_to_cache
        if years == BaseyearCacheConfiguration.ALL_YEARS:
            # copy entire directory
            copytree(input_directory, config['cache_directory'])
            
        else:
            # copy specified years
            os.makedirs(config['cache_directory'])
            for year in years:
                copytree(os.path.join(input_directory, str(year)), 
                          os.path.join(config['cache_directory'], str(year)))