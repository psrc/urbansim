#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

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