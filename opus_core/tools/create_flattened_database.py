#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from opus_core.misc import get_config_from_opus_path
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration


class CreateFlattenedDatabaseOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] configuration",
            description="Create flattened database from a scenario database chain. "
                "Argument 'configuration' is a python module containing dictionary called 'run_configuration'"
                " or a class with the CamelCase version of the module name.")
        #self.parser.remove_option('--database')
        self.parser.add_option("--database", dest="database_name", default=None, 
                               action="store", help="Name of flattened database")
        


if __name__ == "__main__":
    option_group = CreateFlattenedDatabaseOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
    else:
        opus_path = args[0]
        config = get_config_from_opus_path(opus_path)

        from_database_configuration = config['scenario_database_configuration']
    
        to_database_name = options.database_name
        if to_database_name is None:
            to_database_name = from_database_configuration.database_name + '_flattened'
        
        to_database_configuration = ScenarioDatabaseConfiguration(
                                        protocol = from_database_configuration.protocol,
                                        host_name = from_database_configuration.host_name,
                                        user_name = from_database_configuration.user_name,
                                        password = from_database_configuration.password,
                                        database_name = to_database_name)
        tables_to_copy = config['creating_baseyear_cache_configuration'].tables_to_cache
        
        copier = FlattenScenarioDatabaseChain()
        copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                                      to_database_configuration = to_database_configuration,
                                      tables_to_copy = tables_to_copy)
    