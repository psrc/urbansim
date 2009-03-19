# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from baseline import Baseline
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimation(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self['cache_directory'] = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_gridcell/base_year_data')
        self['scenario_database_configuration'] = ScenarioDatabaseConfiguration(database_name = 'eugene_1980_baseyear')
        self['estimation_database_configuration'] = EstimationDatabaseConfiguration(database_name = 'eugene_1980_baseyear_estimation_xxx')
    
        self['datasets_to_cache_after_each_model' ] = []
        self['low_memory_mode'] = False
        self['base_year'] = 1980
        self['years'] = (1980,1980)
        self['seed'] = 10
        #self['models_configuration']['land_price_model']['controller'] = LandPriceModelConfigurationCreator(
                                                                                    #estimation_procedure='opus_core.bma_for_linear_regression_r',
                                                                                    #estimate_config={'bma_imageplot_filename': 'bma_image.pdf'}
        #                                                                            ).execute()
