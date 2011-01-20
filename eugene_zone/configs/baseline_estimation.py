# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from baseline import Baseline
from urbansim_zone.configs.config_changes_for_estimation import ConfigChangesForEstimation
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

class BaselineEstimation(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self['cache_directory'] = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_zone/base_year_data')
        self['scenario_database_configuration'] = ScenarioDatabaseConfiguration(database_name = 'eugene_1980_baseyear_zone')
        self['estimation_database_configuration'] = EstimationDatabaseConfiguration(database_name = 'eugene_1980_baseyear_zone')
    
        self['datasets_to_cache_after_each_model' ] = []
        self['low_memory_mode'] = False
        self['base_year'] = 1980
        self['years'] = (1980,1980)
        self['seed'] = 1
