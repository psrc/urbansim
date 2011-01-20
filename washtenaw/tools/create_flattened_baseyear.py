# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from washtenaw.configs.baseline import Baseline
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

"""
This utility creates a new flattened database containing the
necessary files from the scenario database chain pointed to by
the baseline washtenaw configuration.
"""

run_configuration = Baseline()

from_database_configuration = ScenarioDatabaseConfiguration(database_name = 'wastenaw_baseyear')
to_database_configuration = ScenarioDatabaseConfiguration(database_name = 'washtenaw_flattened')
tables_to_copy = run_configuration['creating_baseyear_cache_configuration'].tables_to_cache

copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                              to_database_configuration = to_database_configuration,
                              tables_to_copy = tables_to_copy)
