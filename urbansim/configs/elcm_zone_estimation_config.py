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

from elcm_estimation_config import elcm_configuration as elcm_gridcell_config
from estimation_zone_config import run_configuration as config

class elcm_configuration(elcm_gridcell_config):
    def get_configuration(self):
        run_configuration = config.copy()
        elcm_local_configuration = self.get_local_configuration()
        run_configuration.merge(elcm_local_configuration)
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = elcm_gridcell_config.get_local_configuration(self)
        run_configuration.merge(self.get_local_elcm_configuration())
        #residential_price_model = {"real_estate_price_model": {"group_members": ["residential"]}}
        #if self.type == "home_based":
        #    run_configuration["models"] = [residential_price_model] + \
        #        run_configuration["models"]
        #else:
        #    run_configuration["models"] = [{"real_estate_price_model": {"group_members": [self.type]}}] + \
        #                                  run_configuration["models"] 
        return run_configuration
    
    def get_local_elcm_configuration(self):
        run_configuration = {}
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'job':{},
            'gridcell': {},
            'household':{},
            'job_building_type':{},
            'building':{},
            'faz': {},
            }
        return run_configuration