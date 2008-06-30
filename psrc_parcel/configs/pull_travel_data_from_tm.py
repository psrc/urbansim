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


from baseline import Baseline

class PullTravelDataFromTm(Baseline):
    def __init__(self):
        config = Baseline()

        config_changes = {
            'description':'extract travel data from travel model',
            'models':[],
            'models_in_year': {2000:[],},
            'years': (2005,2005),
        }
        
        from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_2008_lmwang', 
                                                                       emme2_batch_file='MODEL1-0.BAT',
                                                                       mode='skims', years_to_run={2000: '2000_v1.0aTG',
                                                                                                  2005: '2006_v1.0aTG',
                                                                                                  2010: '2010_v1.0aTG', 
                                                                                                  2015: '2010_v1.0aTG_2015', 
                                                                                                  2020: '2020_v1.0aTG'})
        config['travel_model_configuration'] = travel_model_configuration
        config.replace(config_changes)
        
        self.merge(config)

