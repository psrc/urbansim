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

from repm_estimation_config import repm_configuration as repm_gridcell_config
from estimation_zone_config import run_configuration as config
from opus_core.configuration import Configuration

class repm_configuration(repm_gridcell_config):
    def get_configuration(self):
        run_configuration = Configuration(config)
        local_configuration = self.get_local_configuration()
        run_configuration.merge(local_configuration)
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = repm_gridcell_config.get_local_configuration(self)
        run_configuration.merge(self.get_local_repm_configuration())
        if self.type == "residential":
            pass
            #run_configuration["models"] = ["household_relocation_model", "household_location_choice_model"] + \
             #   run_configuration["models"]
        elif self.type <> "vacant_land":
            pass
            #run_configuration["models"] = ["employment_relocation_model", 
            #                               {"employment_location_choice_model": {"group_members": [self.type]}}] + \
            #                              run_configuration["models"] 
        #if self.type <> "vacant_land":
        #    run_configuration["models"].insert(0, {"real_estate_price_model": {"group_members": ["vacant_land"]}})
        return run_configuration
    
    def get_local_repm_configuration(self):
        run_configuration = {}
        run_configuration["datasets_to_preload"] = {
               'gridcell': {},
               'household':{},
               'job':{},
               'zone':{},
               'building':{},
               'building_type':{},
               'vacant_land_and_building_type':{},                                    
            }
        return run_configuration
