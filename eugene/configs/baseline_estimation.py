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
