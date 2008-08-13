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

if __name__ == '__main__':
    import os
    import sys
    
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
    
    from psrc.estimation.run_estimation import EstimationRunner

    cache_dir = sys.argv[1]
    model_abbreviation = sys.argv[2]
    model_name = sys.argv[3]   
    
    try:
        model_type = sys.argv[4]   
    except:
        model_type=None
    
    model_unknown_boolean = None
    try:    
        if (sys.argv[5]=='False'):
            model_unknown_boolean = False
        if (sys.argv[5]=='True'):
            model_unknown_boolean = True        
    except:
        pass
       
    estimation_config = {
        'cache_directory' : cache_dir,
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['psrc', 'urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'datasets_to_cache_after_each_model':[],
        'low_memory_mode':False,
        'base_year': 2000,
        'years': (2000,2000),                    
        }

    model = [model_abbreviation, model_name]
    if model_type is not None:
        model.append(model_type)
    if model_unknown_boolean is not None:
        model.append(model_unknown_boolean)
        
    model = tuple(model)    
    EstimationRunner().run_estimation(estimation_config, model, save_estimation_results=False) 