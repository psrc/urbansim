# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
            config['creating_baseyear_cache_configuration'].cache_scenario_database,
            'CacheScenarioDatabase'))
        
        CacheScenarioDatabase().run(config)
        logger.log_status("Database %s cached to %s" % (config['scenario_database_configuration'].database_name,
                           config['cache_directory']))
                           
        return config['cache_directory']

if __name__ == "__main__":
    from opus_core.store.attribute_cache import AttributeCache
    
    from opus_core.session_configuration import SessionConfiguration
    from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
    
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
            
        if options.database_name is not None:
            config['services_database_configuration'] = ServicesDatabaseConfiguration(database_name = options.database_name)
        elif options.database_configuration is not None:            
            config['services_database_configuration'] = ServicesDatabaseConfiguration(database_configuration = options.database_configuration)
            
        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,                            
                             in_storage=AttributeCache())
        cacher = CreateBaseyearCache()
        cache_dir = cacher.run(config)