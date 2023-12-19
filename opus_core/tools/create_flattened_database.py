# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.configurations.xml_configuration import XMLConfiguration

class CreateFlattenedDatabaseOptionGroup(GenericOptionGroup):
    def __init__(self):
        """ Examples:
            python create_flattened_database.py -c psrc_parcel.configs.baseline --flattened_database=psrc_parcel_baseyear_flattened
            python create_flattened_database.py -x ../project_configs/seattle_parcel.xml -s Seattle_baseline
            python create_flattened_database.py --scenario_database_name=sanfrancisco_baseyear_start --flattened_database=sanfrancisco_baseyear_flattened
        """
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="""
Create flattened database from a scenario database chain.  
The scenario_database_configuration containing database_name of the scenario 
database and tables_to_cache is read either from a Python module configuration 
passed with '-c' option or an xml configuration with '-x' option, or specified
with --database_server and --scenario_database_name options:
""")
        self.parser.remove_option('--services_database')
        self.parser.remove_option('--database_configuration')        
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                                help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                                help="File name of xml configuration (must also provide a scenario name using -s). Only used if only a specific set of tables should be flattened.")
        self.parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                                help="Name of the scenario to run. Only used if only a specific set of tables should be flattened.")
        self.parser.add_option("--scenario_database_configuration", dest="scenario_database_configuration", default = "scenario_database_server",
                               action="store", help="Name of the database server configuration in database_server_configurations.xml that is to be used to connect to the database. Defaults to 'scenario_database_server'.")
        self.parser.add_option("--scenario_database_name", dest="scenario_database_name", default = None,
                               action="store", help="Name of the scenario database on the scenario database server.")
        self.parser.add_option("--flattened_database", dest="flattened_database_name", default=None, 
                               action="store", help="Name of flattened database.")

if __name__ == "__main__":
    option_group = CreateFlattenedDatabaseOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    config = {}
    if options.configuration_path is not None:
        opus_path = options.configuration_path
        try:
            config = get_config_from_opus_path(opus_path)
        except ImportError:
            # TODO: Once all fully-specified configurations are stored as classes,
            #       get rid of this use.
            import_stmt = 'from %s import run_configuration as config' % opus_path
            exec(import_stmt, globals())
    elif options.xml_configuration is not None:
        if options.scenario_name is None:
            parser.print_help()
            sys.exit(1)
        config = XMLConfiguration(options.xml_configuration).get_run_configuration(options.scenario_name)
    
    from_database_configuration = config.get('scenario_database_configuration', ScenarioDatabaseConfiguration(database_name = options.scenario_database_name,
                                                                                                              database_configuration=options.scenario_database_configuration,
                                                                                                              ))
    to_database_name = options.flattened_database_name or (from_database_configuration.database_name + '_flattened')
    to_database_configuration = ScenarioDatabaseConfiguration(
                                    protocol = from_database_configuration.protocol,
                                    host_name = from_database_configuration.host_name,
                                    user_name = from_database_configuration.user_name,
                                    password = from_database_configuration.password,
                                    database_name = to_database_name)

    if config.get('creating_baseyear_cache_configuration', None):
        tables_to_copy = config['creating_baseyear_cache_configuration'].tables_to_cache
    else:
        tables_to_copy = []  # copy all tables in the chain
    
    copier = FlattenScenarioDatabaseChain()
    copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                                  to_database_configuration = to_database_configuration,
                                  tables_to_copy = tables_to_copy)
