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

from estimation_config_for_model_members import model_member_configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration

class elcm_configuration(model_member_configuration):
    def __init__(self, type, add_member_prefix=False, base_configuration=AbstractUrbansimConfiguration):
        model_member_configuration.__init__(self, "employment_location_choice_model", type, add_member_prefix,
                                            base_configuration=base_configuration)
        
    def get_local_configuration(self):
        run_configuration = model_member_configuration.get_local_configuration(self)
        run_configuration["models"].insert(0, "employment_relocation_model")
        run_configuration["datasets_to_preload"] = {
                'gridcell':{},
                'job':{},
                'job_building_type':{}                                   
                }
        return run_configuration
