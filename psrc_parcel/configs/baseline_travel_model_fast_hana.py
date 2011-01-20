# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline import Baseline

class BaselineTravelModelFastHana(Baseline):
    
    multiple_runs = True
    
    def __init__(self):
        config = Baseline()
        if self.multiple_runs:
            config.sample_inputs()
        config['number_of_runs'] = 99
        config['seed'] = 1
        config_changes = {
            'description':'baseline travel model fast',
        }
        config.replace(config_changes)
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_fast_hana', 
                                                                       emme2_batch_file='MODELUSim.BAT ..\\triptabs',
                                                                       mode='skims', 
                                                                       years_to_run={2005: '2005_06', 2010: '2010_06', 2015: '2010_06'})
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        
        ##fast model doesn't have bank2 and bank3; disable macros using them
        del config['travel_model_configuration']['export_macros']['tazvmt2.mac']
        del config['travel_model_configuration']['export_macros']['tazvmt3.mac']

        del config['travel_model_configuration']['matrix_variable_map']['bank2']
        del config['travel_model_configuration']['matrix_variable_map']['bank3']
        
        config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
                                                                            "tveham.rpt": {"@tveh": "vehicle_volume"}
                                                                            }}
        #config['travel_model_configuration'][2015]['models'] = list(config['travel_model_configuration'][2015].get('models'))
        #config['travel_model_configuration'][2015]['models'].append('opus_emme2.models.restore_trip_tables')
             
        self.merge(config)

    
if __name__ == "__main__":
    config = BaselineTravelModelFastHana()
