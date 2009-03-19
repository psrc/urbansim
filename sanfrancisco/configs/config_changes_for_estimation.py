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
                                   {"real_estate_price_model": ["run"]},
                                   {"household_location_choice_model": ["estimate"]}
                                   ],                  
                    },
            'business_location_choice_model': 
                        {'models': [
                                {'business_location_choice_model': ["estimate"]}
                                                ],
                        },
            'real_estate_price_model': {'models': [
                                {"real_estate_price_model": ["estimate"]}
                                ]},
            "building_location_choice_model": {
                    'nonresidential': {
                            'models': [
                                {"building_location_choice_model": {
                                     "group_members": [{'nonresidential': ["estimate"]}]
                                         }
                                }
                                    ]},
                    'residential': {
                            'models': [
                                {"building_location_choice_model": {
                                     "group_members": [{'residential': ["estimate"]}]
                                         }
                                }
                                    ]}
                    }}
                    
        return config