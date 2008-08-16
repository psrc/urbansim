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
from opus_core.misc import create_import_for_class
from opus_core.misc import get_config_from_opus_path
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.database_server_configuration \
    import DatabaseServerConfiguration

class CreateFlattenedDatabaseOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] configuration",
            description="Create flattened database from a scenario database chain. "
                "Argument 'configuration' is a python module containing dictionary called 'run_configuration'"
                " or a class with the CamelCase version of the module name.")
        self.parser.remove_option('--database')
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
    
        from_database_name = config['input_configuration'].database_name
        to_database_name = options.database_name
        if to_database_name is None:
            to_database_name = from_database_name + '_flattened'
            
        server_config = DatabaseServerConfiguration()
        flatten_config = {
        'tables_to_copy':config['creating_baseyear_cache_configuration'].tables_to_cache,
        'db_server_config_from':server_config,
        'from_database_name':from_database_name,
        'db_server_config_to':server_config,
        'to_database_name':to_database_name,
          }
        copier = FlattenScenarioDatabaseChain()
        copier.copy_scenario_database(**flatten_config)
    