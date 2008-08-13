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

import os

from opus_core.database_management.database_configuration import DatabaseConfiguration

from psrc.config.wlcm_config import run_configuration

    
run_configuration["models"] = [
    "household_person_consistency_keeper",
    "home_based_choice_model",
    "home_based_workplace_choice_model",
    "workplace_location_choice_model_for_resident"
    ]

#run_configuration["models_configuration"]['household_location_choice_model']['controller']['run']['arguments']['agents_index']=None
config_changes = {                   
    'creating_baseyear_cache_configuration':{
        'cache_from_mysql': False,
        'cache_directory_root':r'/projects/urbansim7/urbansim_cache/psrc', #'/projects/urbansim7/urbansim_cache/psrc',
        'baseyear_cache':{
            'existing_cache_to_copy':r'/projects/urbansim7/urbansim_cache/psrc/wlcm_initialization_source',
            'years':range(2000,2001)
            },
     "tables_to_cache":[
                     "persons",
                     "home_based_choice_model_coefficients",
                     "home_based_choice_model_specification",
                     "home_based_workplace_choice_model_coefficients",
                     "home_based_workplace_choice_model_specification",
                     "workplace_location_choice_model_for_resident_specification",
                     "workplace_location_choice_model_for_resident_coefficients",
                     "workplace_location_choice_model_for_immigrant_specification",
                     "workplace_location_choice_model_for_immigrant_coefficients",                     
                     ],                                          
        'unroll_gridcells':False,
        'tables_to_cache_nchunks': {
                    'gridcells':4,
                    },
        },

    'input_configuration':DatabaseConfiguration(
        database_name = 'GSPSRC_2000_baseyear_change_20060924_wlcm_init',
        ),
#    'output_configuration':DatabaseConfiguration(
#        host_name = "trondheim.cs.washington.edu", #os.environ['MYSQLHOSTNAME'],
#        user_name = os.environ.get('MYSQLUSERNAME',''),
#        password = os.environ.get('MYSQLPASSWORD',''),
#        database_name = 'GSPSRC_2000_baseyear_change_20060924_wlcm_init',
#        ),
    'datasets_to_cache_after_each_model':['person'],
    'low_memory_mode':True,
    'base_year': 2000,
    'years': (2001,2001),
    "datasets_to_preload": {
        'gridcell': {},
        'job': {},                                            
        'person': {'package_name':'psrc'},
        'zone': {},
        'household': {},
        }
    }

from urbansim.simulation.run_simulation import RunSimulation
from urbansim.model_coordinators.model_system import ModelSystem

if __name__ == "__main__":
    simulation = RunSimulation()
    run_configuration.merge(config_changes)
    simulation.prepare_and_run(run_configuration, 
                               simulation_instance=ModelSystem(),
                               remove_cache=False)