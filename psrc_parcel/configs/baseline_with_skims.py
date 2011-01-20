# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

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
