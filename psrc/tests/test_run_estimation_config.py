# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.configs.baseline import Baseline

class TestRunEstimationConfig(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'configuration for a test run'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_baseyear'
        self['creating_baseyear_cache_configuration'].cache_directory_root = 'c:/urbansim_cache'
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('workers_for_estimation')
        self['years'] = (2001, 2002)

        del self['travel_model_configuration']
