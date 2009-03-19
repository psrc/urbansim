# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from numpy import where, ones, logical_and, array, median, resize, abs
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.logger import logger

class DB_settings(object):
    db_host_name='trondheim.cs.washington.edu'
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']

class MysqlStorage:
    def get(self, database):
        db_config = DatabaseServerConfiguration(
            protocol = 'mysql',
            host_name = DB_settings.db_host_name,
            user_name = DB_settings.db_user_name,
            password = DB_settings.db_password                                              
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(database)
        
        storage = StorageFactory().get_storage(
            'sql_storage',
            storage_location = db)
        return storage

if __name__ == '__main__':
    input_database_name = 'psrc_2005_data_workspace_hana'
    output_database_name = input_database_name
    instorage = MysqlStorage().get(input_database_name)
    outstorage = MysqlStorage().get(output_database_name)
    dataset_pool = DatasetPool(storage=instorage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'] )
    parcels= dataset_pool.get_dataset('parcel')
    logger.log_status("Loading parcels ...")
    parcels.load_dataset(attributes=['parcel_sqft', 'parcel_sqft_2005', 'land_value', 'improvement_value', 'land_value_2005',
                                     'improvement_value_2005', "zone_id", "land_use_type_id"])
    logger.log_status("Loading finished.")
    sqft_2000 = parcels.get_attribute('parcel_sqft').astype("float32")
    sqft_2005 = parcels.get_attribute('parcel_sqft_2005').astype("float32")
    total_value_2000 = (parcels.get_attribute('land_value')+parcels.get_attribute('improvement_value')).astype("float32")
    total_value_2005 = (parcels.get_attribute('land_value_2005')+parcels.get_attribute('improvement_value_2005')).astype("float32")
    is_valid = logical_and(logical_and(logical_and(logical_and(sqft_2000 > 0, sqft_2005 > 0), 
                           total_value_2005>0), total_value_2000>0), abs(total_value_2005-total_value_2000)>0)
    increases = (total_value_2000[is_valid]/sqft_2000[is_valid])/(total_value_2005[is_valid]/sqft_2005[is_valid])
    #zones = parcels.get_attribute("zone_id")[is_valid]
    zones = parcels.compute_variables(["large_area_id = parcel.disaggregate(faz.large_area_id, intermediates=[zone])"], dataset_pool=dataset_pool)[is_valid]
    lu_types = parcels.get_attribute("land_use_type_id")[is_valid]
    unique_zones = unique_values(zones)
    unique_types = unique_values(lu_types)
    result_zone = []
    result_lut = []
    result_rate = []
    result_n = []
    for zone in unique_zones:
        logger.log_status("LA id: %s" % zone)
        is_zone = zones == zone
        for lut in unique_types:
            is_lut = logical_and(is_zone, lu_types == lut)
            if is_lut.sum() > 0:
                result_zone.append(zone)
                result_lut.append(lut)
                mid = round(median(increases[is_lut]),3)
                result_rate.append(mid)
                result_n.append(is_lut.sum())
                
    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(
            table_name='average_increase_of_total_value',
            table_data={
                        #"zone_id": array(result_zone),
                        "large_area_id": array(result_zone),
                        "land_use_type_id" : array(result_lut),
                        "increase_rate": array(result_rate),
                        'number_of_observations': array(result_n)
                        }
                        )
    ds = Dataset(in_storage=storage, id_name=['large_area_id', 'land_use_type_id'], in_table_name='average_increase_of_total_value')
    ds.write_dataset(out_storage=outstorage, out_table_name='average_increase_of_total_value')