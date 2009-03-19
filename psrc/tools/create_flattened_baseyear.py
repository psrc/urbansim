# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.configs.baseline import Baseline
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

"""
This utility creates a new flattened database containing the
necessary files from the scenario database chain pointed to by
PSRC_2000_baseyear.
"""

run_configuration = Baseline()

from_database_configuration = ScenarioDatabaseConfiguration(database_name = 'PSRC_2000_baseyear')
to_database_configuration = ScenarioDatabaseConfiguration(database_name = 'PSRC_2000_baseyear_flattened')
tables_to_copy = run_configuration['creating_baseyear_cache_configuration'].tables_to_cache

copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                              to_database_configuration = to_database_configuration,
                              tables_to_copy = tables_to_copy)