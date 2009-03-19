# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from baseline import Baseline

class TravelModelOnly(Baseline):
    """
    """
    def __init__(self):
        Baseline.__init__(self)
        self['description']='Washtenaw + travel model'
        self['models']= []
        self['years'] = (2001, 2002)
        #self['creating_baseyear_cache_configuration']['cache_from_database'] = False
        #self['creating_baseyear_cache_configuration']['cache_directory_root']=r'C:\urbansim_cache\washtenaw'
        #self['creating_baseyear_cache_configuration']['baseyear_cache']['directory_to_cache'] = r'C:\urbansim_cache\washtenaw\cache_source20070129'

        from washtenaw.transcad.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('C:\\SEMCOG_baseline\\', mode='full')
        self['travel_model_configuration'] = travel_model_configuration