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
from numpy import array, concatenate
from opus_core.resources import Resources
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
    
        # inititalize jobs attributes
        jobs_data = {}
        jobs_data["sector_id"] = array([], dtype="int32")
        jobs_data["building_id"] = array([], dtype="int32")
        jobs_data["parcel_id"] = array([], dtype="int32")
        jobs_data["zone_id"] = array([], dtype="int32")
        jobs_data["building_type"] = array([], dtype="int32")
        jobs_data["sqft"] = array([], dtype="int32")
        jobs_data["join_flag"] = array([], dtype="int32")
        
        # get attributes from the establisments table
        business_dataset = BusinessDataset(in_storage=in_storage, in_table_name=business_table, id_name=[])
        business_sizes = business_dataset.get_attribute("jobs00")
        sectors = business_dataset.get_attribute("psef_sector_rev")
        tazes = business_dataset.get_attribute("taz")
        building_ids = business_dataset.get_attribute("building_id")
        parcel_ids = business_dataset.get_attribute("parcel_id")
        home_based = business_dataset.get_attribute("home_based")
        building_sqft = business_dataset.get_attribute("imputed_sqft_10vac")
        join_flags = business_dataset.get_attribute("join_flag")
        
        # iterate over establishments. For each business create the corresponding number of jobs
        for i in range(business_dataset.size()):
            n = business_sizes[i]
            logger.log_status("Business %s: %s employees." % (i+1, n))
            jobs_data["sector_id"] = concatenate((jobs_data["sector_id"], array(n*[sectors[i]])))
            jobs_data["building_id"] = concatenate((jobs_data["building_id"], array(n*[building_ids[i]])))
            jobs_data["parcel_id"] = concatenate((jobs_data["parcel_id"], array(n*[parcel_ids[i]])))
            jobs_data["zone_id"] = concatenate((jobs_data["zone_id"], array(n*[tazes[i]])))
            jobs_data["building_type"] = concatenate((jobs_data["building_type"], array(n*[home_based[i]])))
            jobs_data["sqft"] = concatenate((jobs_data["sqft"], array(n*[building_sqft[i]/float(n)]))) # sqft per employee
            jobs_data["join_flag"] = concatenate((jobs_data["join_flag"], array(n*[join_flag[i]])))
            
        jobs_data["job_id"] = arange(jobs_data["sector_id"].size)+1
        
        # create jobs table and write it out
        job_dataset = JobDataset(resources=Resources({"data": jobs_data}))
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage)
        logger.log_status("Created %s jobs." % job_dataset.size())
        


if __name__ == '__main__':
    business_table = "est_match_bldg_flag123457_flag12bldg"
    input_database_name = "psrc_2005_parcel_baseyear_change_hyungtai"
    output_database_name = "psrc_2005_data_workspace_hana"
    input_cache = "/Users/hana/urbansim_cache/psrc/cache_source/2000"
    output_cache = "/Users/hana/urbansim_cache/psrc/test"
    instorage = MysqlStorage().get(input_database_name)
    outstorage = MysqlStorage().get(output_database_name)
    #instorage = FltStorage().get(input_cache)
    #outstorage = FltStorage().get(output_cache)
    UnrollJobsFromEstablishments().run(instorage, outstorage, business_table=business_table)
