# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.estimation_config_for_model_members import model_member_configuration
from urbansim_parcel.configs.controller_config import config
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class bldglcm_configuration(model_member_configuration):
    def __init__(self, type, add_member_prefix=False):
        model_member_configuration.__init__(self, "building_location_choice_model", type, add_member_prefix)
        
    def get_configuration(self):
        run_configuration = config
        local_config = self.get_local_configuration()
        run_configuration.replace(local_config)
        
        #run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["filter"] = \
        #    "'zone:opus_core.func.aggregate(urbansim.gridcell.developable_SSS_capacity_lag%s)' % (constants['recent_years']+1)" 
#        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_maximum_unit_variable"] = \
#            "'zone:opus_core.func.aggregate(urbansim.gridcell.developable_maximum_UNITS_lag%s)' % (constants['recent_years']+1)" 
#        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_minimum_unit_variable"] = \
#            "'zone:opus_core.func.aggregate(urbansim.gridcell.developable_minimum_UNITS_lag%s)' % (constants['recent_years']+1)" 
#        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["capacity_string"] = \
#            "'zone:opus_core.func.aggregate(urbansim.gridcell.is_developable_for_UNITS_lag%s, maximum)' % (constants['recent_years']+1)"
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = model_member_configuration.get_local_configuration(self)
#        vacant_land_model = {"real_estate_price_model": {"group_members": ["vacant_land"]}}
#        if self.type == "residential":
#            run_configuration["models"] = run_configuration["models"]
#        else:
#            run_configuration["models"] = run_configuration["models"] 
#                                          
#        run_configuration["datasets_to_preload"] = {
#            'zone':{},
#            'gridcell': {},
#            'household':{},
#            'building':{},
#            'building_type':{},
#            'job': {},
#                }
 
        return run_configuration

    def get_updated_configuration_from_module(self, run_configuration, specification_module=None):
        run_configuration = update_controller_by_specification_from_module(
                            run_configuration, self.model_name, specification_module)
        run_configuration["models_configuration"][self.model_name]["controller"]["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec['%s']" % self.type
        return run_configuration  