# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc_parcel.configs.baseline import Baseline
from household_location_choice_model_with_price_adj_configuration_creator import \
     HouseholdLocationChoiceModelWithPriceAdjConfigurationCreator

class HlcmWithPriceAdj(Baseline):
    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'Run REPM and HLCM with bidding choice only',
            'models':[
                "real_estate_price_model",
                "household_relocation_model",
                "household_location_choice_model_with_price_adj",
                ],
#            'models_in_year': {2000:
#                               [   "household_relocation_model_for_2000",
#                                   "household_location_choice_model_for_2000",]
#                           },
            'years':(2001, 2001),

        }
        config.replace(config_changes)
        config["models_configuration"]["household_location_choice_model_with_price_adj"] = {}
        config["models_configuration"]["household_location_choice_model_with_price_adj"]["controller"] = \
              HouseholdLocationChoiceModelWithPriceAdjConfigurationCreator(
                  location_set = "building",
                  sampler = "opus_core.samplers.weighted_sampler",
                  sample_size_locations = 50,
                  input_index = 'hrm_index',
#                  filter = 'building.unit_price',
                  demand_string="demand",
                  capacity_string = "urbansim_parcel.building.vacant_residential_units",
                  nchunks=1,
                  lottery_max_iterations=20
                  ).execute()
#        config['models_configuration']['household_location_choice_model_with_price_adj']['controller']['run']['arguments']['chunk_specification'] = "{'nchunks':1}"        
        self.merge(config)
