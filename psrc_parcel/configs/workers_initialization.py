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
        

