# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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