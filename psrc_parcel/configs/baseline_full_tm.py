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

from baseline import Baseline

class BaselineFullTm(Baseline):
    multiple_runs=False
    def __init__(self):
        config = Baseline()
        config['number_of_runs'] = 1
        config['seed'] = 1
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_tm_no_hbw_v1.0a', 
                                                                       emme2_batch_file='./model1-0.sh',
                                                                       mode='full', years_to_run={2005: '2006', 2010: '2010', 2015: '2010_2015', 2020: '2020'})
        config['travel_model_configuration'] = travel_model_configuration
        
        config['travel_model_configuration']['travel_model_input_file_writer'] = 'psrc_parcel.travel_model_input_file_writer'
        config['travel_model_configuration']['system_command'] = ''
        config['travel_model_configuration']['emme_command'] = 'emme-run -ng --set-iks 192.168.1.236'
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        
        config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
                                                                                      "tveham.rpt": {"@tveh": "vehicle_volume"}
                                                                            }}                
        self.merge(config)

if __name__ == "__main__":
    config = BaselineFullTm()
