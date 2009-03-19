# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
                                    'gridcell':{},
                                    'household':{}
                                    }                     
                    },
            'employment_location_choice_model': {
                        'industrial': {'models': [
                                            "employment_relocation_model",
                                            {'employment_location_choice_model': {
                                                   "group_members": [{'industrial': ["estimate"]}]
                                                   }}
                                                ],
                                       "datasets_to_preload": {
                                                'gridcell':{},
                                                'job':{},
                                                'job_building_type':{}                                   
                                                },
                                     },
                        'commercial': {'models': [
                                        "employment_relocation_model",
                                        {'employment_location_choice_model': {
                                                   "group_members": [{'commercial': ["estimate"]}]}}
                                                ],
                                       "datasets_to_preload": {
                                                'gridcell':{},
                                                'job':{},
                                                'job_building_type':{}                                   
                                                },
                                     },
                        'home_based': {'models': [
                                        "employment_relocation_model",
                                        {'employment_location_choice_model': {
                                                   "group_members": [{'home_based': ["estimate"]}]}}
                                                ],
                                       "datasets_to_preload": {
                                                'gridcell':{},
                                                'job':{},
                                                'job_building_type':{}                                   
                                                },
                                     },
                        },
            'land_price_model': {
                    'models': [{
                            "land_price_model": ["estimate"]
                                }]
                    },
            "development_project_location_choice_model": {
                    'industrial': {
                            'models': [
                                "land_price_model",
                                {"industrial_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'gridcell':{}
                                },   
                                   },
                    'commercial': {
                            'models': [
                                "land_price_model",
                                {"commercial_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'gridcell':{}
                                },   },
                    'residential': {
                            'models': [
                                "land_price_model",
                                {"residential_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'gridcell':{}
                                },   
                                    }
                        
                            },
            "residential_land_share_model": {
                        'models': [{
                            "residential_land_share_model": ["estimate"]
                                }]
                    },
                                             
                  }
        return config