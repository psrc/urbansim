# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from psrc_parcel.configs.baseline import Baseline

class BaselineWcmTravelModelFull(Baseline):
    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'assigning jobs to workers',
            'models':[
                #"process_pipeline_events",
                "real_estate_price_model",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "household_transition_model",
                "employment_transition_model",
                "household_relocation_model",
                "household_location_choice_model",
                "employment_relocation_model",
                {"employment_location_choice_model":{'group_members': '_all_'}},
                "work_at_home_choice_model",                
                "workplace_choice_model_for_resident",
                'distribute_unplaced_jobs_model'
                ],
#                {2001:[ "work_at_home_choice_model",],
#                              2002:[ "workplace_choice_model_for_resident" ] },
            'years': (2001,2006),
#            'datasets_to_cache_after_each_model':['person'],
        }
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_2008_lmwang', 
                                                                       emme2_batch_file='MODEL1-0.BAT',
                                                                       mode='full', years_to_run={2005: '2006_v1.0aTG',
                                                                                                  2010: '2010_v1.0aTG', 
                                                                                                  2015: '2010_v1.0aTG_2015', 
                                                                                                  2020: '2020_v1.0aTG'})
        config['travel_model_configuration'] = travel_model_configuration
        config.replace(config_changes)
        
        self.merge(config)

