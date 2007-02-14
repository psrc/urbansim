#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from baseline import Baseline

class TravelModelOnly(Baseline):
    """
    """
    def __init__(self):
        Baseline.__init__(self)
        self['description']='Washtenaw + travel model'
        self['models']= []
        self['years'] = (2001, 2002)
        #self['creating_baseyear_cache_configuration']['cache_from_mysql'] = False
        #self['creating_baseyear_cache_configuration']['cache_directory_root']=r'C:\urbansim_cache\washtenaw'
        #self['creating_baseyear_cache_configuration']['baseyear_cache']['directory_to_cache'] = r'C:\urbansim_cache\washtenaw\cache_source20070129'

        from washtenaw.transcad.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('C:\\SEMCOG_baseline\\', mode='full')
        self['travel_model_configuration'] = travel_model_configuration