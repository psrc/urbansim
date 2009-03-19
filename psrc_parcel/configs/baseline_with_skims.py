# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from baseline import Baseline

class BaselineWithSkims(Baseline):
    def __init__(self):
        config = Baseline()
        
        config_changes = {
            'description':'baseline with skims',
        }
        config.replace(config_changes)
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc', mode='skims')
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        self.merge(config)
