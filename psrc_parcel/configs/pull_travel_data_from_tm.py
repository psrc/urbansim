# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


from baseline import Baseline

class PullTravelDataFromTm(Baseline):
    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'extract travel data from travel model',
            'models':[],
            'models_in_year': {2000:[],},
            'years': (2005,2005),
        }
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_2008_lmwang', 
                                                                       emme2_batch_file='MODEL1-0.BAT',
                                                                       mode='skims', years_to_run={2000: '2000_v1.0aTG',
                                                                                                  2005: '2006_v1.0aTG',
                                                                                                  2010: '2010_v1.0aTG', 
                                                                                                  2015: '2010_v1.0aTG_2015', 
                                                                                                  2020: '2020_v1.0aTG'})
        config['travel_model_configuration'] = travel_model_configuration
        config.replace(config_changes)
        
        self.merge(config)

