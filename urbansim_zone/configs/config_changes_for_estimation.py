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
                                   {"household_relocation_model": ["run"]},
                                   {"household_location_choice_model": ["estimate"]}
                                   ],
                        'datasets_to_preload': {
                                    'pseudo_building':{},
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
                                                'pseudo_building':{},
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
                                                'pseudo_building':{},
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
                                                'pseudo_building':{},
                                                'job':{},
                                                'job_building_type':{}                                   
                                                },
                                     },
                        },
            "industrial_development_project_location_choice_model": {
                            'models': [
                                {"industrial_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'pseudo_building':{},
                                'zone':{},
                                'urbansim_constant': {}
                                },   
                                   },
            'commercial_development_project_location_choice_model': {
                            'models': [
                                {"commercial_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'pseudo_building':{},
                                'zone':{},
                                'urbansim_constant': {}
                                },   },
            'residential_development_project_location_choice_model': {
                            'models': [
                                {"residential_development_project_location_choice_model": ["estimate"]}
                                    ],
                            "datasets_to_preload": {
                                'pseudo_building':{},
                                'zone':{},
                                'urbansim_constant': {}
                                },   
                                    }
                                             
                  }
        return config