# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.configs.subset_configuration import SubsetConfiguration
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

"""
This utility creates, on localhost, a flattened copy of the subset 
test database chain located on trondheim..
"""
server_config_to = ScenarioDatabaseConfiguration()
server_config_from = ScenarioDatabaseConfiguration()

run_configuration = SubsetConfiguration()

from_database_configuration = ScenarioDatabaseConfiguration(database_name = run_configuration['scenario_database_configuration'].database_name)
to_database_configuration = ScenarioDatabaseConfiguration(database_name = run_configuration['scenario_database_configuration'].database_name)
tables_to_copy = run_configuration['creating_baseyear_cache_configuration'].tables_to_cache

copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                              to_database_configuration = to_database_configuration,
                              tables_to_copy = tables_to_copy)