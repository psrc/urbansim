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

class BaselineWithSkims(Baseline):
    def __init__(self):
        config = Baseline()
        
        config_changes = {
            'description':'baseline with skims',
        }
        config.replace(config_changes)
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc', mode='skims')
        config['travel_model_configuration'] = travel_model_configuration
        config['travel_model_configuration']['locations_to_disaggregate'] = ['parcel', 'building']
        self.merge(config)
