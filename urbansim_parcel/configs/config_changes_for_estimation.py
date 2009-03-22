# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation as USConfigChangesForEstimation

class ConfigChangesForEstimation(USConfigChangesForEstimation):

    def __init__(self):
        USConfigChangesForEstimation.__init__(self)
        self['household_location_choice_model'] = {'models': [
                                   #{"real_estate_price_model": ["run"]},                          
                                   {"household_relocation_model": ["run"]},
                                   #{"tour_schedule_model": ["run"]},
                                   {"household_location_choice_model": ["estimate"]},
                                   ],
                               }
        self['employment_location_choice_model'] = {
                        'non_home_based': {'models': [
                                            {"real_estate_price_model_for_all_parcels": ["run"]},
                                            {'employment_location_choice_model': {
                                                   "group_members": [{'non_home_based': ["estimate"]}]
                                                   }}
                                                ],
                                       "datasets_to_preload": {
                                                'building':{},
                                                'job':{},
                                                'job_building_type':{}                                   
                                                },
                                     },
                        'home_based': {'models': [
                                        {"real_estate_price_model_for_all_parcels": ["run"]},
                                        {'employment_location_choice_model': {
                                                   "group_members": [{'home_based': ["estimate"]}]}}
                                                ],
                                       "datasets_to_preload": {
                                                'gridcell':{},
                                                'job':{},
                                                'job_building_type':{}
                                                },
                                     },
                        }
        self['real_estate_price_model'] = {'models': [
                                {"real_estate_price_model": ["estimate"]}  
                                                     ]
                                           }
        self["workplace_choice_model_for_resident"] = {'models': [
                                {"workplace_choice_model_for_resident": ["estimate"]}
                                                            ]
                                                }
                                
        self["work_at_home_choice_model"] = {'models': [
                                {"work_at_home_choice_model": ["estimate"]}
                                                    ]
                                                }
        self["development_project_proposal_choice_model"] = {'models': [
            #{"expected_sale_price_model":["run"]},
                                {"development_project_proposal_choice_model": ["estimate"]}
                            ]
                            }
                                     
