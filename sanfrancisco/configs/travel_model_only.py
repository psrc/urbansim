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
from baseline import Baseline

class TravelModelOnly(Baseline):
    """
    """
    def __init__(self):
        Baseline.__init__(self)
        self['description']='SF travel model only'
        self['models']= []
        self['years'] = (2001, 2002)
#        self['creating_baseyear_cache_configuration']['cache_from_database'] = True
#        self['creating_baseyear_cache_configuration']['cache_directory_root']=r'/workspace/urbansim_cache\sanfrancisco'
#        self['creating_baseyear_cache_configuration']['baseyear_cache']['directory_to_cache'] = r'C:\urbansim_cache\washtenaw\cache_source20070129'

        from sanfrancisco.travel_model.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('/test/sf_tm/', mode='full')
        self['travel_model_configuration'] = travel_model_configuration