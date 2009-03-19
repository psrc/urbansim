# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from estimation_config_for_model_members import model_member_configuration
from estimation_zone_config import run_configuration as config

class blcm_configuration(model_member_configuration):
    def __init__(self, type, add_member_prefix=False):
        model_member_configuration.__init__(self, "building_location_choice_model", type, add_member_prefix)
        
    def get_configuration(self):
        run_configuration = config.copy()
        local_config = self.get_local_configuration()
        run_configuration.merge(local_config)
        #run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["filter"] = \
        #    "'zone.aggregate(urbansim.gridcell.developable_SSS_capacity_lag%s)' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_maximum_unit_variable"] = \
            "'zone.aggregate(urbansim.gridcell.developable_maximum_UNITS_lag%s)' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["developable_minimum_unit_variable"] = \
            "'zone.aggregate(urbansim.gridcell.developable_minimum_UNITS_lag%s)' % (urbansim_constant['recent_years']+1)" 
        run_configuration["models_configuration"][self.model_name]["controller"]["init"]["arguments"]["capacity_string"] = \
            "'zone.aggregate(urbansim.gridcell.is_developable_for_UNITS_lag%s, function=aggregate)' % (urbansim_constant['recent_years']+1)"
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = model_member_configuration.get_local_configuration(self)
        #vacant_land_model = {"real_estate_price_model": {"group_members": ["vacant_land"]}}
#        residential_price_model = {"real_estate_price_model": {"group_members": ["residential"]}}
#        commercial_price_model = {"real_estate_price_model": {"group_members": ["commercial"]}}
#        industrial_price_model = {"real_estate_price_model": {"group_members": ["industrial"]}}
#        if self.type == "residential":
#            run_configuration["models"] = [vacant_land_model, residential_price_model] + \
#                run_configuration["models"]
#        else:
#            run_configuration["models"] = [vacant_land_model, commercial_price_model, industrial_price_model] + \
#                                          run_configuration["models"] 
                                          
        #run_configuration["models"] = [vacant_land_model, 
        #                               {"real_estate_price_model": {"group_members": [self.type]}}] + \
        #                                  run_configuration["models"] 
                                          
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'gridcell': {},
            'household':{},
            'building':{},
            'building_type':{},
            'job': {},
                }
 
        return run_configuration
