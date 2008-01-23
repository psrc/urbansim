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

from baseline import Baseline

class BaselineTravelModelFastHana(Baseline):
    
    multiple_runs = True
    
    def __init__(self):
        config = Baseline()
        config['number_of_runs'] = 1
        config['seed'] = 1
        config_changes = {
            'description':'baseline travel model fast',
        }
        config.replace(config_changes)
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_fast_hana', 
                                                                       emme2_batch_file='MODELUSim.BAT ..\\triptabs',
                                                                       mode='full', 
                                                                       years_to_run={2005: '2005_06', 2010: '2010_06', 2015: '2010_06'})
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        del config['travel_model_configuration'][2000]
        
        ##fast model doesn't have bank2 and bank3; disable macros using them
        del config['travel_model_configuration']['emmission_emme2_macros']['tazvmt2.mac']
        del config['travel_model_configuration']['emmission_emme2_macros']['tazvmt3.mac']

        del config['travel_model_configuration']['matrix_variable_map']['bank2']
        del config['travel_model_configuration']['matrix_variable_map']['bank3']
             
        self.merge(config)

#if __name__ == "__main__":
#    config = BaselineTravelModelFast()
