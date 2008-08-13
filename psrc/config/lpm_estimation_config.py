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
