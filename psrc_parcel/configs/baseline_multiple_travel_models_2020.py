# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline_hana import BaselineHana

class BaselineMultipleTravelModels2020(BaselineHana):
    
    tm_scenario = 'baseline_v1.0bb_C1'
    multiple_runs=True
    
    def __init__(self):
        config = BaselineHana()
        config['number_of_runs'] = 5
        config['seed'] = 1
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration(self.tm_scenario, 
                                                                       emme2_batch_file='./model1-0.sh',
                                                                       mode='full', years_to_run={2020: '2020'})
        config['travel_model_configuration'] = travel_model_configuration
        
        config['travel_model_configuration']['travel_model_input_file_writer'] = 'inprocess.hana.uncertainty.travel_model_input_file_writer'
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
                
        config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
                                                                                      "tveham.rpt": {"@tveh": "vehicle_volume"}
                                                                            }}
        
        config['travel_model_configuration']['bm_distribution_file'] = \
                '/Users/hana/bm/psrc_parcel/simulation_results/0818/2005/bm_parameters'
                
        config['travel_model_configuration']['scale_to_control_totals'] = True
        config['travel_model_configuration']['control_totals'] = { # for 2020
                                    'households': 1706945,
                                    'jobs': {'manu':   186131, # sectors 3, 4, 5
                                             'wtcu':   216184, # sectors 6, 8, 9, 10
                                             'retail': 402241, # sectors 7, 14
                                             'fires': 1046052, # sectors 11, 12, 13, 16, 17
                                             'edu':    146626, # sectors 15, 19
                                             'gov':    207079,  # sector 18
                                             'constr': 189047,  # sector 2
                                             'mining':   8882  # sector 1
                                             }
                                            }
        self.merge(config)

if __name__ == "__main__":
    config = BaselineMultipleTravelModels2020()
