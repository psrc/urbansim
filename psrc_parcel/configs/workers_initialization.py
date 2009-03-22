# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from psrc_parcel.configs.baseline import Baseline

class WorkersInitialization(Baseline):
    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'assigning jobs to workers',
            'models_in_year':{2001:[ "work_at_home_choice_model",],
                              2002:[ "workplace_choice_model_for_resident" ] },
            'years': (2001,2002),
            'datasets_to_cache_after_each_model':['person'],
        }
        config.replace(config_changes)
        
        self.merge(config)
        self['models_configuration']['work_at_home_choice_model']['controller']['run']['arguments']['run_choice_model'] = False
        self['models_configuration']['work_at_home_choice_model']['controller']['run']['arguments']['choose_job_only_in_residence_zone'] = False
        

