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

from baseline_hana import BaselineHana
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimationHana(BaselineHana):

    def __init__(self):
        BaselineHana.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self['cache_directory'] = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        self['estimation_database_configuration'] = EstimationDatabaseConfiguration(
                                                             database_name = 'psrc_activity2006_ver2_hana',
                                                             )
        self['dataset_pool_configuration'] = DatasetPoolConfiguration(
                                                                      package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
                                                                      )
        self['datasets_to_cache_after_each_model'] = []
        self['years'] = (2000,2000)
        if 'models_in_year' in self.keys():
            del self['models_in_year']          


