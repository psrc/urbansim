# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


from psrc.configs.baseline import Baseline

class SubsetConfiguration(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'subset baseline without travel model'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_baseyear_fircrest'
        self['creating_baseyear_cache_configuration'].cache_directory_root = 'c:/urbansim_cache'
        self['years'] = (2001, 2002)

        del self['travel_model_configuration']
