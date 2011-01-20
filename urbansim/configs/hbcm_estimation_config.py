# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config

run_configuration = config.copy()
run_configuration['models'] = [
    {'home_based_choice_model': ['estimate']}
]

run_configuration['datasets_to_preload'] = {
        'gridcell':{},
        'household':{},
        'zone':{},
        'person':{'package_name':'psrc'}
       }

run_configuration['creating_baseyear_cache_configuration'].tables_to_cache += [
        'persons',
        'persons_for_estimation',
        'home_based_choice_model_specification',
        'home_based_choice_model_coefficients'
       ]