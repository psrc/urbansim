# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline import Baseline

class BaselineTravelModelFast(Baseline):

    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'baseline travel model fast',
        }
        config.replace(config_changes)
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_fast_new', 
                                                                       emme2_batch_file='MODELUSim.BAT ..\\triptabs',
                                                                       mode='full')
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        del config['travel_model_configuration'][2000]
        
        ##fast model doesn't have bank2 and bank3; disable macros using them
        del config['travel_model_configuration']['export_macros']['tazvmt2.mac']
        del config['travel_model_configuration']['export_macros']['tazvmt3.mac']

        del config['travel_model_configuration']['matrix_variable_map']['bank2']
        del config['travel_model_configuration']['matrix_variable_map']['bank3']
        
        self.merge(config)

#if __name__ == "__main__":
#    config = BaselineTravelModelFast()
