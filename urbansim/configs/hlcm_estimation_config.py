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

from urbansim.configs.estimation_base_config import run_configuration as config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configs.estimation_base_config import EstimationBaseConfig

class HLCMEstimationConfig(EstimationBaseConfig):
    def __init__(self, base_configuration=AbstractUrbansimConfiguration):
        EstimationBaseConfig.__init__(self, base_configuration)
        self.update_config()
        
    def update_config(self):
        self.merge(get_changes_for_hlcm_estimation(self))
        
def get_changes_for_hlcm_estimation(config=None):
    estimation_configuration = {}
    estimation_configuration["models"] = [                                
                  {"household_relocation_model": ["run"]},
                  {"household_location_choice_model": ["estimate"]}
              ]

    estimation_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'household':{}
        }
    return estimation_configuration

run_configuration = config.copy()

estimation_configuration = get_changes_for_hlcm_estimation()
run_configuration.merge(estimation_configuration)
