# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from baseline_hana import BaselineHana

class BaselineTravelModel2005WithObservedData(BaselineHana):
    tm_scenario = 'baseline_v1.0bb_C1'
    multiple_runs=False
    def __init__(self):
        config = BaselineHana()
        config['number_of_runs'] = 1
        config['seed'] = 1
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration(self.tm_scenario, 
                                                                       emme2_batch_file='./model1-0.sh',
                                                                       mode='full', 
                                                                       years_to_run={2005: '2006_obs'})
        config['travel_model_configuration'] = travel_model_configuration
        
        config['travel_model_configuration']['travel_model_input_file_writer'] = 'inprocess.hana.uncertainty.travel_model_input_file_writer_with_observed_values'
        config['travel_model_configuration']['system_command'] = ''
        config['travel_model_configuration']['emme_command'] = 'emme-run -ng --set-iks 192.168.1.236'
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        
        config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
                                                                                      "tveham.rpt": {"@tveh": "vehicle_volume"}
                                                                            }}
        self.merge(config)

if __name__ == "__main__":
    config = BaselineTravelModel2005WithObservedData()
