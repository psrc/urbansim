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

from dplcm_estimation_config import dplcm_configuration as dplcm_gridcell_config
from estimation_zone_config import run_configuration as config

class dplcm_configuration(dplcm_gridcell_config):
    def get_configuration(self):
        run_configuration = config.copy()
        dplcm_local_configuration = self.get_dplcm_configuration()
        run_configuration.merge(dplcm_local_configuration)
        return run_configuration
    
    def get_dplcm_configuration(self):
        run_configuration = dplcm_gridcell_config.get_dplcm_configuration(self)
        run_configuration.merge(self.get_local_dplcm_configuration())
        return run_configuration
        
    def get_local_dplcm_configuration(self):
        run_configuration = {}
        run_configuration["models"] = [
            {"%s_development_project_location_choice_model" % self.type: ["estimate"]}
         ]
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'job':{},
            'gridcell': {}
            }
        return run_configuration