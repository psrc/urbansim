# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from baseline import Baseline

class BaselineTravelModelPointEst(Baseline):
    multiple_runs=True
    def __init__(self):
        config = Baseline()
        config['number_of_runs'] = 1
        config['seed'] = 1
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_2008', 
                                                                       emme2_batch_file='MODEL1-0.BAT',
                                                                       mode='full', years_to_run={2005: '2006_v1.0aTG',
                                                                                                  2020: '2020_06'})
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['travel_model_input_file_writer'] = 'psrc_parcel.travel_model_input_file_writer'
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        
        config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
                                                                                      "tveham.rpt": {"@tveh": "vehicle_volume"}
                                                                            }}
                
        self.merge(config)

