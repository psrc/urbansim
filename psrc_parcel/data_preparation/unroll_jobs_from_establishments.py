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
from numpy import array, arange, cumsum, resize, clip, logical_and, where
from opus_core.logger import logger
from opus_core.store.opus_database import OpusDatabase
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from urbansim_parcel.datasets.business_dataset import BusinessDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.building_dataset import BuildingDataset

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
    
    minimum_sqft = 1
    maximum_sqft = 4000
    
    def run(self, in_storage, out_storage, business_table="business", jobs_table="jobs"):
        logger.log_status("Unrolling %s table." % business_table)
        # get attributes from the establisments table
        business_dataset = BusinessDataset(in_storage=in_storage, in_table_name=business_table)
        business_sizes = business_dataset.get_attribute("jobs00").astype("int32")
        sectors = business_dataset.get_attribute("sector_id")
        tazes = business_dataset.get_attribute("zone_id").astype("int32")
        building_ids = business_dataset.get_attribute("building_id")
        parcel_ids = business_dataset.get_attribute("parcel_id")
        home_based = business_dataset.get_attribute("home_based")
        building_sqft = business_dataset.get_attribute("building_sqft_10vac")
        building_sqft[building_sqft <= 0] = 0
        join_flags = business_dataset.get_attribute("join_flag")
        taz_est = business_dataset.get_attribute("taz_est")
        impute_sqft_flag = business_dataset.get_attribute("impute_building_sqft_flag")
        
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
        jobs_data["impute_building_sqft_flag"] = resize(array([], dtype=impute_sqft_flag.dtype), total_size)
        
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
            jobs_data["sqft"][start_index:end_index] = round((building_sqft[i]-building_sqft[i]/10.0)/float(business_sizes[i])) # sqft per employee
            jobs_data["join_flag"][start_index:end_index] = join_flags[i]
            jobs_data["taz_est"][start_index:end_index] = taz_est[i]
            jobs_data["impute_building_sqft_flag"][start_index:end_index]  = impute_sqft_flag[i]
            start_index = end_index
            
        jobs_data["job_id"] = arange(total_size)+1
        jobs_data["sqft"] = clip(jobs_data["sqft"], 0, self.maximum_sqft)
        jobs_data["sqft"][logical_and(jobs_data["sqft"]>0, jobs_data["sqft"]<self.minimum_sqft)] = self.minimum_sqft
        # create jobs table and write it out
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name="jobs",
                table_data=jobs_data
                )
        job_dataset = JobDataset(in_storage=storage)
        self.delete_jobs_with_non_existing_buildings(job_dataset, out_storage)
        logger.log_status("Write jobs table.")
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage)
        logger.log_status("Created %s jobs." % job_dataset.size())
    
    def delete_jobs_with_non_existing_buildings(self, jobs, in_storage):
        buildings = BuildingDataset(in_storage=in_storage)
        building_ids = jobs.get_attribute(buildings.get_id_name()[0])
        valid_building_ids_idx = where(building_ids > 0)[0]
        index = buildings.try_get_id_index(building_ids[valid_building_ids_idx])
        logger.log_status("%s jobs have non-existing locations and will be deleted." % where(index < 0)[0].size)
        jobs.subset_by_index(valid_building_ids_idx[index >= 0], flush_attributes_if_not_loaded=False)

        
class CreateBuildingSqftPerJobDataset:
    minimum_median = 25
    maximum_median = 2000
    def run(self, in_storage, out_storage):
        logger.log_status("Creating building_sqft_per_job table.")
        from urbansim_parcel.datasets.building_sqft_per_job_dataset import create_building_sqft_per_job_dataset
        dataset_pool = DatasetPool(storage=in_storage, package_order=['psrc_parcel', 'urbanism_parcel', 'urbansim'] )
        ds = create_building_sqft_per_job_dataset(dataset_pool, self.minimum_median, self.maximum_median)
        logger.log_status("Write building_sqft_per_job table.")
        ds.write_dataset(out_storage=out_storage)
    
if __name__ == '__main__':
    #business_table = "est00_match_bldg2005_flag123457_flag12bldg"
    business_table = "businesses"
    #input_database_name = "psrc_2005_parcel_baseyear_change_hyungtai"
    input_database_name = "psrc_2005_parcel_baseyear_change_20070713"
    #input_database_name = "psrc_2005_data_workspace_hana"
    output_database_name = "psrc_2005_data_workspace_hana"
    input_cache = "/Users/hana/urbansim_cache/psrc/cache_source/2000"
    output_cache = "/Users/hana/urbansim_cache/psrc/data_preparation/stepI/2000"
    instorage = MysqlStorage().get(input_database_name)
    #outstorage = MysqlStorage().get(output_database_name)
    #instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    UnrollJobsFromEstablishments().run(instorage, outstorage, business_table=business_table)
    CreateBuildingSqftPerJobDataset().run(in_storage=outstorage, out_storage=outstorage)