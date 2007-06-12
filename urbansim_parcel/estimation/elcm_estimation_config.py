#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from urbansim_parcel.configs.controller_config import base_controller_config
from urbansim.configs.elcm_estimation_config import elcm_configuration as parent_config
from estimation_config_for_model_members import model_member_configuration

class elcm_configuration(config):
    def __init__(self, type, add_member_prefix=False, base_configuration=base_controller_config):
        parent_config.__init__(self, type, add_member_prefix, base_configuration)
        
    def get_local_configuration(self):
        run_configuration = parent_config.get_local_configuration(self)
        run_configuration["datasets_to_preload"] = {
                'building':{},
                'job':{},
                'job_building_type':{}                                   
                }
        return run_configuration