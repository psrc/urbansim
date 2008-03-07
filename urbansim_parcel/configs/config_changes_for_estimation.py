#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from urbansim.configs.config_changes_for_estimation import ConfigChangesForEstimation as USConfigChangesForEstimation

class ConfigChangesForEstimation(USConfigChangesForEstimation):

    def __init__(self):
        USConfigChangesForEstimation.__init__(self)
        self['household_location_choice_model'] = {'models': [
                                   {"real_estate_price_model": ["run"]},                          
                                   #{"household_relocation_model": ["run"]},
                                   {"household_location_choice_model": ["estimate"]}
                                   ]}
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
                                
        self["home_based_job_choice_model"] = {'models': [
                                {"home_based_job_choice_model": ["estimate"]}
                                                    ]
                                                }
                                     