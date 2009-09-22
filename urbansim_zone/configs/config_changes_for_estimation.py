# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configuration import Configuration

class ConfigChangesForEstimation(Configuration):

    def __init__(self):
        Configuration.__init__(self)
        estimation_changes = self._get_estimation_changes()
        self.merge(estimation_changes)
        
    def _get_estimation_changes(self):
        config = {
            'household_location_choice_model': {
                        'models': [                                
                                   {"household_relocation_model": ["run"]},
                                   {"household_location_choice_model": ["estimate"]}
                                   ],
                        'datasets_to_preload': {
                                    'building':{},
                                    'household':{}
                                    }                     
                    },
            'employment_location_choice_model': {
                        'home_based': {'models': [
                                            "employment_relocation_model",
                                            {'employment_location_choice_model': {
                                                   "group_members": [{'home_based': ["estimate"]}]
                                                   }}
                                                ],
                                       "datasets_to_preload": {
                                                'building':{},
                                                'job':{},
                                                'home_based_status':{}                                   
                                                },
                                     },
                        'non_home_based': {'models': [
                                        "employment_relocation_model",
                                        {'employment_location_choice_model': {
                                                   "group_members": [{'non_home_based': ["estimate"]}]}}
                                                ],
                                       "datasets_to_preload": {
                                                'building':{},
                                                'job':{},
                                                'home_based_status':{}                                   
                                                },
                                     },
                        },
            "non_residential_development_project_location_choice_model": {
                            'models': [
                                {"non_residential_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'building':{},
                                'zone':{},
                                'urbansim_constant': {}
                                },   
                                   },
            'residential_development_project_location_choice_model': {
                            'models': [
                                {"residential_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'building':{},
                                'zone':{},
                                'urbansim_constant': {}
                                },   
                                    }
                                             
                  }
        return config