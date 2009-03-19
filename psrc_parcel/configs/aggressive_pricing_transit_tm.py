# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from baseline import Baseline

class AggressivePricingTransitTm(Baseline):
    tm_scenario = '/urbansim_cache/travel_model/pricing_transit_v1.0bb'
    multiple_runs=False
    def __init__(self):
        config = Baseline()
        config_changes = {
                        'description':'Aggressive land use + pricing & transit travel model',
        }
        config.replace(config_changes)

        config['number_of_runs'] = 1
        config['seed'] = 1
        config['creating_baseyear_cache_configuration'].cache_directory_root = r'/urbansim_cache/psrc_parcel/runs'

        #config['creating_baseyear_cache_configuration'].cache_from_database = True
        config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = r'/urbansim_cache/psrc_parcel/base_year_data/aggressive'

        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration(self.tm_scenario, 
                                                                       emme2_batch_file='model1-0.sh',
                                                                       mode='full', 
                                                                       years_to_run={
                                                                                     2005: '2006_v1.0bb', 
                                                                                     2010: '2010_v1.0bb', 
                                                                                    #2015: '2010_v1.0bb', 
                                                                                     2020: '2020_v1.0bb', 
                                                                                    #2025: '2020_v1.0bb', 
                                                                                     2030: '2030_v1.0bb'})
        config['travel_model_configuration'] = travel_model_configuration
        
        #config['travel_model_configuration']['travel_model_input_file_writer'] = 'psrc_parcel.travel_model_input_file_writer'
        config['travel_model_configuration']['system_command'] = ''
        config['travel_model_configuration']['emme_command'] = 'emme-run -ng --set-iks 127.0.0.1'
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        
        #config['travel_model_configuration']['export_macros']['get_link_attributes.mac'] = {'bank':'bank1', 'scenario':-1, 'path':'export_macros'}
        #config['travel_model_configuration']['node_matrix_variable_map'] = {"bank1": {"attr_on_links.rpt": {"timau": "am_pk_travel_time", "len": "distance"},
        #                                                                              "tveham.rpt": {"@tveh": "vehicle_volume"}
        #                                                                    }}                
        self.merge(config)

if __name__ == "__main__":
    config = BaselineBaselineTm()
