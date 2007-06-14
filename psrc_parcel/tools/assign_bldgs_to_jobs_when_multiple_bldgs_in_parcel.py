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
from numpy import array, where, logical_and, arange, ones, cumsum, zeros, alltrue, absolute
from scipy.ndimage import sum as ndimage_sum
from opus_core.logger import logger
from opus_core.store.opus_database import OpusDatabase
from opus_core.storage_factory import StorageFactory
from opus_core.sampling_toolbox import sample_noreplace, sample_replace
from opus_core.dataset_pool import DatasetPool
from opus_core.misc import unique_values, create_combination_indices
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
    
class AssignBuildingsToJobs:
    def run(self, in_storage, out_storage, dataset_pool_storage, jobs_table="jobs"):
        job_dataset = JobDataset(in_storage=in_storage, in_table_name = jobs_table)
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=dataset_pool_storage)
        parcel_ids = job_dataset.get_attribute("parcel_id")
        building_ids = job_dataset.get_attribute("building_id")
        building_types = job_dataset.get_attribute("building_type")
        is_considered = logical_and(parcel_ids > 0, building_ids <= 0) # jobs taht have assigned parcel but not a building
        job_index_home_based = where(logical_and(is_considered, building_types == 1))[0]
        job_index_non_home_based = where(logical_and(is_considered, building_types == 2))[0]
        
        building_dataset = dataset_pool.get_dataset('building')
        parcel_ids_in_bldgs = building_dataset.get_attribute("parcel_id")
        bldg_ids_in_bldgs = building_dataset.get_id_attribute()
        
        # home_based
        unique_parcels = unique_values(parcel_ids[job_index_home_based])
        population_in_buildings = building_dataset.compute_variables(["urbansim_parcel.building.population"],
                                                                     dataset_pool=dataset_pool)
        occupied = building_dataset.compute_variables(["urbansim_parcel.building.number_of_jobs"],
                                                                     dataset_pool=dataset_pool)
        # iterate ovar parcels
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_home_based] == parcel)[0]
            capacity = population_in_buildings[idx_in_bldgs] - occupied[idx_in_bldgs]
            if capacity.sum() <= 0:
                continue
            keep_bldgs = where(capacity>0)[0]
            capacity = capacity[keep_bldgs]
            idx_in_bldgs = idx_in_bldgs[keep_bldgs]
            cumcap = cumsum(capacity)
            tmp = (capacity.sum()*ones(idx_in_jobs.size)).astype("int32") # the sampling is done proportional to the capacity
            comb = create_combination_indices(tmp)
            tcomb = array(comb)
            for j in range(idx_in_jobs.size):
                for i in range(cumcap.size-1, -1, -1):
                    tcomb[where(comb[:,j] < cumcap[i])[0], j] = i
            s = zeros((tcomb.shape[0], capacity.size))
            o = ones(tcomb.shape[1], dtype="int32")
            idx = arange(capacity.size)+1
            for i in range(tcomb.shape[0]):
                s[i,:] = ndimage_sum(o, labels=tcomb[i,:]+1, index=idx)
            tcomb = tcomb[alltrue(s<=capacity, axis=1)]
            if tcomb.size <= 0: # not enough space for all jobs
                draw = sample_replace(arange(idx_in_jobs.size), capacity.sum()) # sample jobs that will be placed
                building_ids[job_index_home_based[idx_in_jobs[draw]]] = bldg_ids_in_bldgs[idx_in_bldgs]
            else:
                draw = sample_noreplace(arange(tcomb.shape[0]), 1)
                building_ids[job_index_home_based[idx_in_jobs]] = bldg_ids_in_bldgs[idx_in_bldgs][tcomb[draw]][0]
        
        # non_home_based
        unique_parcels = unique_values(parcel_ids[job_index_non_home_based])
        job_building_types = job_dataset.compute_variables(["job.disaggregate(building.building_type_id"], 
                                                           dataset_pool=dataset_pool)[job_index_non_home_based]
        building_type_dataset = datasett_pool.get_dataset("building_type")
        available_building_types= building_type_dataset.get_id_attribute()
        idx_available_bt = building_type_dataset.get_id_index(available_building_types)
        sectors = job_dataset.get_attribute_by_index("sector_id", job_index_non_home_based)
        unique_sectors = unique_values(sectors)
        sector_bt_distribution = zeros((unique_sectors.size, building_type_dataset.size()), dtype="float32")
        jobs_sqft = job_dataset.get_attribute_by_index("sqft", job_index_non_home_based)
        
        # find sector -> building_type distribution
        for isector in range(unique_sectors.size):
            idx = where(sectors==unique_sectors[isector])[0]
            o = ones(idx.size, dtype="int32")
            sector_bt_distribution[isector,:] = ndimage_sum(o, labels=job_building_types[idx], index=avalable_building_types)
        
        non_res_sqft = building_dataset.get_attribute("non_residential_sqft")
        occupied = building_dataset.compute_variables(["urbansim_parcel.building.occupied_building_sqft_by_jobs"],
                                                                     dataset_pool=dataset_pool)
        
        # iterate ovar parcels
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_non_home_based] == parcel)[0]
            capacity = non_res_sqft[idx_in_bldgs] - occupied[idx_in_bldgs]
            if capacity.sum() <= 0:
                continue
            this_jobs_sectors = sectors[idx_in_jobs]
            this_jobs_types = job_building_types[idx_in_jobs]
            tmp = (idx_in_bldgs.size*ones(idx_in_jobs.size)).astype("int32")
            comb = create_combination_indices(tmp)
            s = zeros((comb.shape[0], capacity.size))
            o = jobs_sqft[idx_in_jobs]
            idx = arange(capacity.size)+1
            for i in range(comb.shape[0]): # compute capacity requirements for each building 
                s[i,:] = ndimage_sum(o, labels=comb[i,:]+1, index=idx)
            allowed = alltrue(s<=capacity, axis=1)
            if allowed.sum() <= 0: # no combination fits
                dif = absolute(s - capacity)
                imindif = dif.argmin() # get combination with min. difference
                building_ids[job_index_non_home_based[idx_in_jobs]] = bldg_ids_in_bldgs[idx_in_bldgs][comb[imindif]][0]
                continue
            
            random_job = sample_noreplace(idx_in_jobs, 1)
            
        job_dataset.modify_attribute(name="building_id", data = building_ids)
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage)
        logger.log_status("Done.")
        
if __name__ == '__main__':
    input_database_name = "psrc_2005_parcel_baseyear_change_20070613"
    output_database_name = "psrc_2005_data_workspace_hana"
    input_cache =  "/Users/hana/urbansim_cache/psrc/cache_source_parcel/2005"
    output_cache = "/Users/hana/urbansim_cache/psrc/cache_source_parcel"
    #instorage = MysqlStorage().get(input_database_name)
    #outstorage = MysqlStorage().get(output_database_name)
    instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    AssignBuildingsToJobs().run(instorage, outstorage, dataset_pool_storage=instorage)

            