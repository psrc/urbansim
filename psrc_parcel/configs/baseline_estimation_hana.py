# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from .baseline_hana import BaselineHana
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimationHana(BaselineHana):

    def __init__(self):
        BaselineHana.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self['cache_directory'] = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        self['estimation_database_configuration'] = EstimationDatabaseConfiguration(
                                                             database_name = 'psrc_activity2006_ver2_hana_est',
                                                             )
        self['dataset_pool_configuration'] = DatasetPoolConfiguration(
                                                                      package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
                                                                      )
        self['datasets_to_cache_after_each_model'] = []
        self['years'] = (2000,2000)
        if 'models_in_year' in list(self.keys()):
            del self['models_in_year']          


