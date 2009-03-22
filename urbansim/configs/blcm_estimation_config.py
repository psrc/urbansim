# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
        