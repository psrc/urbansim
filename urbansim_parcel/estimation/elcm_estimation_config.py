# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration as base_controller_config
from urbansim.configs.elcm_estimation_config import elcm_configuration as parent_config
from urbansim.configs.estimation_config_for_model_members import model_member_configuration

class elcm_configuration(parent_config):
    def __init__(self, type, add_member_prefix=False, base_configuration=base_controller_config):
        parent_config.__init__(self, type, add_member_prefix, base_configuration)
        
    def get_local_configuration(self):
        run_configuration = model_member_configuration.get_local_configuration(self)
        run_configuration["datasets_to_preload"] = {
                'building':{},
                'job':{},
                'job_building_type':{}                                   
                }
        run_configuration["models"].insert(0,
                    {"real_estate_price_model_for_all_parcels": ["run"]})
        return run_configuration