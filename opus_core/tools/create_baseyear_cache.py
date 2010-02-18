# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
from optparse import OptionParser
from opus_core.logger import logger
from opus_core.misc import create_import_for_class
from opus_core.misc import get_config_from_opus_path
from opus_core.cache.cache_scenario_database import CacheScenarioDatabase
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

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
    
    parser = OptionParser(usage="python %prog [options] configuration", 
                          description="Create baseyear cache. Argument 'configuration' is a "
                          "python module containing dictionary called 'run_configuration'"
                          " or a class with the CamelCase version of the module name.")

    parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                            help="Opus path to Python module defining run_configuration.")        
    parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                            help="file name of xml configuration (must also provide a scenario name using -s)")
    parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                            help="name of the scenario to create cache (required for xml-configuration)") 
    parser.add_option("--cache-directory", dest="cache_directory", default=None, 
                            help="Cache directory.")
    parser.add_option('-d', '--database-name', dest='database_name', default = None,
                            help='Name of scenario database to cache from (required if no scenario_database_configuration is specified in configuration).')        
    parser.add_option("--database-configuration", dest="database_configuration", default = None,
                       action="store", help="Name of the scenario database server configuration in database_server_configurations.xml.")
    
    (options, args) = parser.parse_args()
    
    if options.configuration_path is not None:
        opus_path = options.configuration_path
        try:
            config = get_config_from_opus_path(opus_path)
        except ImportError:
            import_stmt = 'from %s import run_configuration as config' % opus_path
            exec(import_stmt)
    elif options.xml_configuration is not None:
        if options.scenario_name is None:
            parser.print_help()
            sys.exit(1)
        config = XMLConfiguration(options.xml_configuration).get_run_configuration(options.scenario_name)
    else:
        parser.print_help()
        sys.exit(1)
    
    if options.cache_directory is not None:
        config['cache_directory'] = options.cache_directory
        
    if options.database_name is not None or options.database_configuration is not None:
        if not config.has_key('scenario_database_configuration'):
            config['scenario_database_configuration'] = ScenarioDatabaseConfiguration(database_name = options.database_name,
                                                                                      database_configuration = options.database_configuration
                                                                                      )
        else:
            if options.database_configuration is not None:
                    config['scenario_database_configuration'] = ScenarioDatabaseConfiguration(database_configuration = options.database_configuration)
            if options.database_name is not None:
                config['scenario_database_configuration'].database = options.database_name
        
    SessionConfiguration(new_instance=True,
                         package_order=config['dataset_pool_configuration'].package_order,                            
                         in_storage=AttributeCache())
    cacher = CreateBaseyearCache()
    cache_dir = cacher.run(config)