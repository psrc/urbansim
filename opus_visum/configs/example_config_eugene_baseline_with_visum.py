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

from baseline import Baseline

class BaselineVisumTravelModel(Baseline):
    
    def __init__(self):
        config = Baseline()
        
        config_changes = {
            'description':'baseline with full Visum travel model run',
            'years':(1981, 1981),
        }
        config.replace(config_changes)
        
        from opus_visum.configs.visum_configuration import VisumConfiguration
        travel_model_configuration = VisumConfiguration(r'C:/visum/eugene', mode='full')
        config['travel_model_configuration'] = travel_model_configuration
        
        self.merge(config)

