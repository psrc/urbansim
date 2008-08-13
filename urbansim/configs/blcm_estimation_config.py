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

from estimation_config_for_model_members import model_member_configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration

class blcm_configuration(model_member_configuration):
    def __init__(self, type, add_member_prefix=False, base_configuration=AbstractUrbansimConfiguration):
        model_member_configuration.__init__(self, "building_location_choice_model", type, add_member_prefix,
                                            base_configuration=base_configuration)
        
    def get_configuration(self):
        run_configuration = model_member_configuration.get_configuration(self)
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["filter"] = \
            "'urbansim.gridcell.is_developable_for_UNITS_lag%s' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_maximum_unit_variable"] = \
            "'urbansim.gridcell.developable_maximum_UNITS_lag%s' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_minimum_unit_variable"] = \
            "'urbansim.gridcell.developable_minimum_UNITS_lag%s' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["capacity_string"] = \
            "'urbansim.gridcell.is_developable_for_UNITS_lag%s' % (urbansim_constant['recent_years']+1)"
        return run_configuration
        
    def get_local_configuration(self):
        run_configuration = model_member_configuration.get_local_configuration(self)
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'gridcell': {},
            'household':{},
            'building':{},
            'building_type':{},
            'job': {},
                }
        return run_configuration
        