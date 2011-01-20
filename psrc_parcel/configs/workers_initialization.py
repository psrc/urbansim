# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
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
        self['models_configuration']['work_at_home_choice_model']['controller']['run']['arguments']['run_choice_model'] = True
        self['models_configuration']['work_at_home_choice_model']['controller']['run']['arguments']['choose_job_only_in_residence_zone'] = True
        self['models_configuration']['work_at_home_choice_model']['controller']['init']['arguments']['filter'] = "'job.building_type==2'"
        self['models_configuration']['work_at_home_choice_model']['controller']['prepare_for_run']['arguments']['agents_filter'] = "'urbansim_parcel.person.is_worker'"
        self['models_configuration']['workplace_choice_model_for_resident']['controller']['init']['arguments']["run_config"].merge({"capacity_string":"job.building_type==1"})
        self['models_configuration']['workplace_choice_model_for_resident']['controller']['init']['arguments']["filter"] = "'job.building_type==1'"
        self['models_configuration']['workplace_choice_model_for_resident']['controller']['run']['arguments']["agents_filter"] = "'urbansim_parcel.person.is_non_home_based_worker'"
        self['models_configuration']['workplace_choice_model_for_resident']['controller']['run']['arguments']["chunk_specification"] = "{'records_per_chunk':20000}"