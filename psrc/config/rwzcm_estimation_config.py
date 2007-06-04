#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import copy
from psrc.config.workplace_zone_choice_model_config import run_configuration
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class rwzcm_configuration:
    def __init__(self, dummy=None):
        self.model_name = "workplace_location_choice_model_for_resident"
    
    def get_configuration(self, specification_module="psrc.estimation.estimation_RWZCM_variables"):
        config = copy.deepcopy(run_configuration)
        config["models"] = [
            #"land_price_model",
            {"workplace_location_choice_model_for_resident": ["estimate"]}
         ]
        
        config["datasets_to_preload"] = {
            'gridcell':{},
            'person':{'package_name':'psrc'},
            'zone':{}                
        } 

        config = update_controller_by_specification_from_module(config, self.model_name, specification_module)

        return config