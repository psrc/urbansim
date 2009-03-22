# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline import Baseline

class BaselineVisumTravelModel(Baseline):
    
    def __init__(self):
        config = Baseline()
        
        config_changes = {
            'description':'baseline with full Visum travel model run',
            'years':(1981, 1981),
        }
        config.replace(config_changes)
        
        from opus_visum.configs.visum_configuration import VisumConfiguration
        travel_model_configuration = VisumConfiguration(r'C:/visum/eugene', mode='full')
        config['travel_model_configuration'] = travel_model_configuration
        
        self.merge(config)

