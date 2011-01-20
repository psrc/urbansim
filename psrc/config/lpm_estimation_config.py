# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.lpm_estimation_config import run_configuration

config_changes = {
    'models_configuration':{
        'land_price_model':{
            'controller':{
                'import':{
                    'estimation_LPM_variables':"specification as spec",
                    },
                'prepare_for_estimate':{
                    'arguments':{
                        "specification_dict": "spec",
                        "dataset": "gridcell", 
                        "threshold": 1000,
                        },
                    },
                },
            },
        },
    }
run_configuration.merge(config_changes)
