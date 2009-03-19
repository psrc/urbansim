# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

#DISCLAIMER: THIS FILE IS OUT OF DATE AND NEEDS SIGNIFICANT MODIFICATIONS 
#            TO MAKE IT WORK

print "Create MySQL connection"
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.datasets.dataset import DatasetSubset
from numpy import where
import os

#step 1. unroll gridcell from 2000 to 1990
from urbansim.model_coordinators.cache_scenario_database import CacheScenarioDatabase
from opus_core.configuration import Configuration

def rm_rf(path):
    #TODO: replace uses with use of shutil.rmtree
    """Recursively deletes a directory and all its children (directories or files).
    Can use a relative or absolute path"""
    if not os.path.exists(path):
        return
    if os.path.isdir(path):
        contents = os.listdir(path)
        for file in contents:
            absolute_path = os.path.join(path, file)
            rm_rf(absolute_path)
        os.rmdir(path)
    else:
        os.remove(path)

if __name__ == '__main__':
    cache_directory = "C:/tab/waterdemand4"
    
    gridcell_config = Configuration({
        'in_storage_type':'mysql',
        'db_host_name':'artemis.ce.washington.edu',
        'db_user_name':'urbansim', 
        'db_password':'cee530',    
        'db_input_database':'psrc',
        'db_output_database':None,
        'cache_directory':cache_directory,
        'base_year':2000,
        'tables_to_cache':[
            'gridcells', 
    #        'households',
    #        'jobs', 
        ]})
    
    #CacheScenarioDatabase().run(gridcell_config)
    
    # step 2 cache water demand data by 
    dbcon = ScenarioDatabase(database_name = "water_demand_seattle2") 
    
    print "Create Storage object."
    from opus_core.storage_factory import StorageFactory
    storage = StorageFactory().get_storage(type="mysql_storage", storage_location=dbcon)
    
    from waterdemand.datasets.consumption_dataset import ConsumptionDataset
    consumption_types = ['wrmr', 'wcsr', 'wrsr'] #'wcmr'
    for consumption_type in consumption_types:
        
        consumption = ConsumptionDataset(in_storage = storage, in_table_name=consumption_type+'_grid')
        
        for year in range(1990, 2001):
            print "%s %s" % (consumption_type, year)
            year_index = where(consumption.get_attribute("billyear") == year)
            out_storage = StorageFactory().get_storage(type="flt_storage", storage_location=os.path.join(cache_directory, str(year)))
            consumption_subset = DatasetSubset(consumption, year_index)
            consumption_subset.write_dataset(out_storage=out_storage, out_table_name=consumption_type.lower())