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

import os
from numpy import array, arange, cumsum, resize
from opus_core.logger import logger
from opus_core.store.opus_database import OpusDatabase
from opus_core.storage_factory import StorageFactory
from urbansim_parcel.datasets.business_dataset import BusinessDataset
from urbansim.datasets.job_dataset import JobDataset

class DB_settings(object):
    db_host_name='trondheim.cs.washington.edu'
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']

class MysqlStorage:
    def get(self, database):
        con = OpusDatabase(hostname = DB_settings.db_host_name,
                               username = DB_settings.db_user_name,
                               password = DB_settings.db_password,
                               database_name = database)
        storage = StorageFactory().get_storage('mysql_storage', storage_location=con)
        return storage

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
class UnrollJobsFromEstablishments:
    def run(self, in_storage, out_storage, business_table="business", jobs_table="jobs"):
        
        # get attributes from the establisments table
        business_dataset = BusinessDataset(in_storage=in_storage, in_table_name=business_table, id_name=[])
        business_sizes = business_dataset.get_attribute("jobs00").astype("int32")
        sectors = business_dataset.get_attribute("psef_sector")
        tazes = business_dataset.get_attribute("taz").astype("int32")
        building_ids = business_dataset.get_attribute("building_id")
        parcel_ids = business_dataset.get_attribute("parcel_id")
        home_based = business_dataset.get_attribute("home_based")
        building_sqft = business_dataset.get_attribute("building_sqft_10vac")
        join_flags = business_dataset.get_attribute("join_flag")
        taz_est = business_dataset.get_attribute("taz_est")
        
        # inititalize jobs attributes
        total_size = business_sizes.sum()
        jobs_data = {}
        jobs_data["sector_id"] = resize(array([-1], dtype=sectors.dtype), total_size)
        jobs_data["building_id"] = resize(array([-1], dtype=building_ids.dtype), total_size)
        jobs_data["parcel_id"] = resize(array([-1], dtype=parcel_ids.dtype), total_size)
        jobs_data["zone_id"] = resize(array([-1], dtype=tazes.dtype), total_size)
        jobs_data["building_type"] = resize(array([-1], dtype=home_based.dtype), total_size)
        jobs_data["sqft"] = resize(array([], dtype=building_sqft.dtype), total_size)
        jobs_data["join_flag"] = resize(array([], dtype=join_flags.dtype), total_size)
        jobs_data["taz_est"] = resize(array([], dtype=taz_est.dtype), total_size)
        
        indices = cumsum(business_sizes)
        # iterate over establishments. For each business create the corresponding number of jobs by filling the corresponding part 
        # of the arrays
        start_index=0
        for i in range(business_dataset.size()):
            end_index = indices[i]
            jobs_data["sector_id"][start_index:end_index] = sectors[i]
            jobs_data["building_id"][start_index:end_index] = building_ids[i]
            jobs_data["parcel_id"][start_index:end_index] = parcel_ids[i]
            jobs_data["zone_id"][start_index:end_index] = tazes[i]
            jobs_data["building_type"][start_index:end_index] = home_based[i]
            jobs_data["sqft"][start_index:end_index] = building_sqft[i]/float(business_sizes[i]) # sqft per employee
            jobs_data["join_flag"][start_index:end_index] = join_flags[i]
            jobs_data["taz_est"][start_index:end_index] = taz_est[i]
            start_index = end_index
            
        jobs_data["job_id"] = arange(total_size)+1
        
        # create jobs table and write it out
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name="jobs",
                table_data=jobs_data
                )
        job_dataset = JobDataset(in_storage=storage)
        logger.log_status("Write jobs table.")
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage)
        logger.log_status("Created %s jobs." % job_dataset.size())
        


if __name__ == '__main__':
    business_table = "est00_match_bldg2005_flag123457_flag12bldg"
    input_database_name = "psrc_2005_parcel_baseyear_change_hyungtai"
    output_database_name = "psrc_2005_data_workspace_hana"
    input_cache = "/Users/hana/urbansim_cache/psrc/cache_source/2000"
    output_cache = "/Users/hana/urbansim_cache/psrc/cache_source_parcel/2005"
    instorage = MysqlStorage().get(input_database_name)
    #outstorage = MysqlStorage().get(output_database_name)
    #instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    UnrollJobsFromEstablishments().run(instorage, outstorage, business_table=business_table)
