# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

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