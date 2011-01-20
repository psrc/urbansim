# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


###############
# These are examples how to create datasets from different types of storage. 
# Most of the examples use data from opus_core/data
###############

import os
from opus_core.storage_factory import StorageFactory
from opus_core.opus_package import OpusPackage
from opus_core.datasets.dataset import Dataset

def create_dataset_from_tab_storage():
    storage = StorageFactory().get_storage('tab_storage', # type of storage
                                           storage_location = os.path.join(OpusPackage().get_opus_core_path(), "data", "tab") # directory
                                           )
    test_dataset = Dataset(in_storage = storage, 
                           in_table_name='tests', # file name without its ending
                           id_name='id' # which attribute is the unique identifier
                           )
    return test_dataset

def create_dataset_from_tab_storage_shortcut():
    from opus_core.misc import get_dataset_from_tab_storage
    return get_dataset_from_tab_storage('tests', 
                                        directory=os.path.join(OpusPackage().get_opus_core_path(), "data", "tab"),
                                        dataset_args={'in_table_name':'tests', 'id_name':'id'})
    
def create_dataset_from_dbf_storage():
    storage = StorageFactory().get_storage('dbf_storage', # type of storage
                                           storage_location = os.path.join(OpusPackage().get_opus_core_path(), "data", "dbf") # directory
                                           )
    test_dataset = Dataset(in_storage = storage, 
                           in_table_name='test_medium', # file name without its ending
                           id_name='keyid' # which attribute is the unique identifier
                           )
    return test_dataset

def create_dataset_from_flt_storage():
    storage = StorageFactory().get_storage('flt_storage', # type of storage
                                           storage_location = os.path.join(OpusPackage().get_opus_core_path(), "data", "test_cache", "1980") # directory
                                           )
    # in case of flt storage, each dataset is a directory with one file per attribute
    zone_dataset = Dataset(in_storage = storage, 
                           in_table_name='zones', # directory of the dataset 
                           id_name='zone_id' # which attribute is the unique identifier
                           )
    return zone_dataset

def create_dataset_from_dict_storage():
    # This can be used when creating a dataset on the fly (without a physical storage).
    from numpy import arange, array
    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(table_name = 'my_table', # whatever name
                        table_data = {'my_id': arange(1, 6),
                                      'attribute1': array([10, 20, 30, 40, 50]),
                                      'attribute2': array([500, 400, 300, 200, 100])
                                      }
                        )
    test_dataset = Dataset(in_storage = storage, 
                           in_table_name='my_table',
                           id_name='my_id' # which attribute is the unique identifier
                           )
    return test_dataset

def create_dataset_from_sql_storage():
    from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
    from opus_core.database_management.database_server import DatabaseServer
    
    # make sure the environment variables are set, or replace it by approproate values 
    db_config = ServicesDatabaseConfiguration()
    db_server = DatabaseServer(db_config)
    database = db_server.get_database('services') # name of the database
        
    storage = StorageFactory().get_storage('sql_storage',
                                           storage_location = database)
    services_dataset = Dataset(in_storage = storage, 
                           in_table_name='available_runs', # name of the table
                           id_name=[] # the table doees not have an unique identifier
                           )
    return services_dataset

if __name__ == "__main__":
    print "Summary of a test dataset from tab storage"
    ds_from_tab = create_dataset_from_tab_storage()
    ds_from_tab.summary()
    # do the same in different way
    ds2_from_tab = create_dataset_from_tab_storage_shortcut()
    ds2_from_tab.summary()
    
    print "\n\nSummary of a test dataset from dbf storage"
    ds_from_dbf = create_dataset_from_dbf_storage()
    ds_from_dbf.summary()
    
    print "\n\nSummary of a zone dataset from flt storage"
    ds_from_flt = create_dataset_from_flt_storage()
    ds_from_flt.summary()
    
    print "\n\nSummary of a test dataset from dict storage"
    ds_from_dict = create_dataset_from_dict_storage()
    ds_from_dict.summary()
    
    # Uncomment the following three lines, if you have services database available and MYSQL environment variables are set.
    #print "\n\nInfo from available runs dataset from mysql database"
    #ds_from_sql = create_dataset_from_sql_storage()
    #print "Maximum run_id: %s, number_of_entries: %s" % (ds_from_sql.get_attribute('run_id').max(), ds_from_sql.size())

    