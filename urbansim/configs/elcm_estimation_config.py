# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
