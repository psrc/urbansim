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

from baseline_travel_model_2020_biaspf_varpf import BaselineTravelModel2020BiaspfVarpf

class BaselineTravelModel2020Nobias(BaselineTravelModel2020BiaspfVarpf):
    
    
    def __init__(self):
        BaselineTravelModel2020BiaspfVarpf.__init__(self)
        self['travel_model_configuration']['bm_module_class_pair'] = ('inprocess.hana.uncertainty.bm_no_bias', 'BmNoBias')

