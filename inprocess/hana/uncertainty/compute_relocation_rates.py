# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.multiple_runs import MultipleRuns

rate_dir = '/Users/hana/urbansim/census'
rate_storage = StorageFactory().get_storage('tab_storage',  storage_location = rate_dir)
rates = Dataset(in_storage = rate_storage, 
                in_table_name='household_relocation_rates', id_name=[], dataset_name='household_relocation_rate')

cache_root = '/Users/hana/urbansim_cache/psrc/parcel/bm/relocation/0122'

if os.path.exists(os.path.join(cache_root, 'cache_directories')):
    os.remove(os.path.join(cache_root, 'cache_directories'))
    
mr = MultipleRuns(cache_root, prefix='run_', package_order=['inprocess', 'psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                  additional_datasets = {'household_relocation_rate': rates})

#mr.get_datasets_from_multiple_runs(2001, ['inprocess.household_relocation_rate.annual_relocation_rate'], 'household_relocation_rate')
#mr.export_values_from_mr(cache_root, prefix='rates')

coef = mr.get_datasets_from_multiple_runs(2001, ['household_relocation_choice_model_coefficient.estimate'], 
                                   'household_relocation_choice_model_coefficient', 'coefficient_name', 
                                   dataset_arguments={'household_relocation_choice_model_coefficient': {'id_name':[]}})

print coef['b1_tt'].get_attribute('estimate')