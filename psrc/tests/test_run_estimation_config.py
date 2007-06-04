#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from psrc.configs.baseline import Baseline

class TestRunEstimationConfig(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'configuration for a test run'
        self['input_configuration'].database_name = 'PSRC_2000_baseyear'
        self['creating_baseyear_cache_configuration'].cache_directory_root = 'c:/urbansim_cache'
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('workers_for_estimation')
        self['years'] = (2001, 2002)

        del self['travel_model_configuration']
