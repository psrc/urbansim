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

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.logger import logger
from opus_core.misc import create_import_for_class
from opus_core.misc import get_config_from_opus_path

class CreateBaseyearCacheOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] configuration",
            description="Create baseyear cache. Argument 'configuration' is a "
                "python module containing dictionary called 'run_configuration'"
                " or a class with the CamelCase version of the module name.")
        self.parser.add_option("--cache-directory", dest="cache_directory", default=None, 
                                action="store", 
                                help="Cache directory.")
        
class CreateBaseyearCache(object):
    def run(self, config):        
        if config['cache_directory'] is None:
            raise KeyError('The cache directory must be defined at the '
                'command line or in the given configuration. Use '
                '--cache-directory to specify a cache directory to use.')
        
        exec(create_import_for_class(
            config['creating_baseyear_cache_configuration'].cache_mysql_data,
            'CacheMysqlData'))
        
        CacheMysqlData().run(config)
        logger.log_status("Database %s cached to %s" % (config['input_configuration'].database_name,
                           config['cache_directory']))
                           
        return config['cache_directory']

if __name__ == "__main__":
    from opus_core.store.attribute_cache import AttributeCache
    
    from opus_core.session_configuration import SessionConfiguration
    
    option_group = CreateBaseyearCacheOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
    else:
        opus_path = args[0]
        config = get_config_from_opus_path(opus_path)
        
        if options.cache_directory is not None:
            config['cache_directory'] = options.cache_directory
        
        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,
                             package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions,                              
                             in_storage=AttributeCache())
        cacher = CreateBaseyearCache()
        cache_dir = cacher.run(config)