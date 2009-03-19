# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from psrc.configs.baseline_without_travel_model import run_configuration as config

run_configuration = config.copy()
run_configuration['scenario_database_configuration'] = ScenarioDatabaseConfiguration(
    database_name = 'PSRC_2000_baseyear_sampled_10_percent',
    ),
run_configuration['datasets_to_cache_after_each_model'] = []