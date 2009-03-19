# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from baseline import Baseline

class BaselineWithTravelModel(Baseline):
    """
    """
    def __init__(self):
        Baseline.__init__(self)
        self['description']='Washtenaw baseline + travel model'
        
        from washtenaw.transcad.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('C:\\SEMCOG_baseline\\', mode='full')
        self['travel_model_configuration'] = travel_model_configuration