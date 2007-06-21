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
from numpy import array, where, logical_and, arange, ones, cumsum, zeros, alltrue, absolute, resize, any, floor
from numpy.random import seed
from scipy.ndimage import sum as ndimage_sum
from opus_core.logger import logger
from opus_core.store.opus_database import OpusDatabase
from opus_core.storage_factory import StorageFactory
from opus_core.sampling_toolbox import sample_noreplace, sample_replace, probsample_noreplace
from opus_core.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from opus_core.misc import unique_values, create_combination_indices
from opus_core.variables.attribute_type import AttributeType
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
    def run(self, in_storage, out_storage, dataset_pool_storage, jobs_table="jobs", 
            zone_averages_table="building_sqft_per_job"):
        """
        'in_storage' should contain the jobs table and the zone_averages_table. The 'dataset_pool_storage'
        shoudl contain all other tables needed (buildings, households, building_types). 
        The script runs for all jobs that have parcel assigned but no building_id, separately 
        for home_based and non_home_based_jobs.
        For home_based jobs the capacity of a single-family building is determined from sizes of the households living there 
        (for each household the minimum of numper of members and 2 is taken). For multi-family buildings the capacity is 50.
        """
        seed(1)
        job_dataset = JobDataset(in_storage=in_storage, in_table_name = jobs_table)
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=dataset_pool_storage)
        dataset_pool._add_dataset("job", job_dataset)
        parcel_ids = job_dataset.get_attribute("parcel_id")
        building_ids = job_dataset.get_attribute("building_id")
        building_types = job_dataset.get_attribute("building_type")
        is_considered = logical_and(parcel_ids > 0, building_ids <= 0) # jobs that have assigned parcel but not a building
        job_index_home_based = where(logical_and(is_considered, building_types == 1))[0]
        job_index_non_home_based = where(logical_and(is_considered, building_types == 2))[0]
        
        building_dataset = dataset_pool.get_dataset('building')
        parcel_ids_in_bldgs = building_dataset.get_attribute("parcel_id")
        bldg_ids_in_bldgs = building_dataset.get_id_attribute()
        bldg_types_in_bldgs = building_dataset.get_attribute("building_type_id")
        
        non_res_sqft = building_dataset.get_attribute("non_residential_sqft")
        occupied = building_dataset.compute_variables(["urbansim_parcel.building.occupied_building_sqft_by_jobs"],
                                                                     dataset_pool=dataset_pool)
        
        # re-classify non-home based jobs to home-based if parcels contain only residential buildings
        bldgs_unit_names = building_dataset.compute_variables([
                               "building.disaggregate(generic_building_type.unit_name, [building_type])"], 
                                                           dataset_pool=dataset_pool)
        unique_parcels = unique_values(parcel_ids[job_index_non_home_based])
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_non_home_based] == parcel)[0]
            capacity = non_res_sqft[idx_in_bldgs] - occupied[idx_in_bldgs]
            if capacity.sum() <= 0:
                where_residential = where(bldgs_unit_names[idx_in_bldgs] == "residential_units")[0]
                if where_residential.size > 0:
                    building_types[job_index_non_home_based[idx_in_jobs]] = 1 # set to home-based jobs
        job_dataset.modify_attribute(name="building_type", data = building_types)        
        
        old_nhb_size = job_index_non_home_based.size
        job_index_home_based = where(logical_and(is_considered, building_types == 1))[0]
        job_index_non_home_based = where(logical_and(is_considered, building_types == 2))[0]
        logger.log_status("%s non-home based jobs reclassified as home-based." % (old_nhb_size-job_index_non_home_based.size))

        # home_based jobs
        unique_parcels = unique_values(parcel_ids[job_index_home_based])
        capacity_in_buildings = building_dataset.compute_variables([
                          "building.aggregate(psrc_parcel.household.minimum_persons_and_2)"],
                             dataset_pool=dataset_pool)
        capacity_in_buildings[bldg_types_in_bldgs==12] = 50 # in multi-family houses is higher capacity
        occupied = building_dataset.compute_variables(["urbansim_parcel.building.number_of_jobs"],
                                                                     dataset_pool=dataset_pool)
        parcels_with_exceeded_capacity = []
        # iterate over parcels
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_home_based] == parcel)[0]
            capacity = capacity_in_buildings[idx_in_bldgs] - occupied[idx_in_bldgs]
            if capacity.sum() <= 0:
                continue
            probcomb = ones((idx_in_bldgs.size, idx_in_jobs.size))
            taken = zeros(capacity.shape, dtype="int32")
            while True:
                zero_cap = where((capacity - taken) <= 0)[0]
                probcomb[zero_cap,:] = 0
                if probcomb.sum() <= 0:
                    break
                req =  probcomb.sum(axis=0)
                wmaxi = where(req==req.max())[0]
                drawjob = sample_noreplace(arange(wmaxi.size), 1) # draw job from available jobs
                imax_req = wmaxi[drawjob]
                weights = probcomb[:,imax_req]
                # sample building
                draw = probsample_noreplace(arange(probcomb.shape[0]), 1, resize(weights/weights.sum(), (probcomb.shape[0],)))
                taken[draw] = taken[draw] + 1
                building_ids[job_index_home_based[idx_in_jobs[imax_req]]] = bldg_ids_in_bldgs[idx_in_bldgs[draw]]
                probcomb[:,imax_req] = 0
            if -1 in building_ids[job_index_home_based[idx_in_jobs]]:
                parcels_with_exceeded_capacity.append(parcel)
        parcels_with_exceeded_capacity = array(parcels_with_exceeded_capacity)    
        
        logger.log_status("%s home based jobs (out of %s hb jobs) were placed." % ((building_ids[job_index_home_based]>0).sum(),
                                                                         job_index_home_based.size))
        
        
        # non_home_based jobs
        unique_parcels = unique_values(parcel_ids[job_index_non_home_based])
        job_building_types = job_dataset.compute_variables(["job.disaggregate(building.building_type_id)"], 
                                                           dataset_pool=dataset_pool)
        where_valid_jbt = where(logical_and(job_building_types>0, building_types == 2))[0]                     
        building_type_dataset = dataset_pool.get_dataset("building_type")
        available_building_types= building_type_dataset.get_id_attribute()
        idx_available_bt = building_type_dataset.get_id_index(available_building_types)
        sectors = job_dataset.get_attribute("sector_id")
        unique_sectors = unique_values(sectors)
        sector_bt_distribution = zeros((unique_sectors.size, building_type_dataset.size()), dtype="float32")
        
        jobs_sqft = job_dataset.get_attribute_by_index("sqft", job_index_non_home_based).astype("float32")
        jobs_zones = job_dataset.get_attribute_by_index("zone_id", job_index_non_home_based)
        
        # find sector -> building_type distribution
        sector_index_mapping = {}
        for isector in range(unique_sectors.size):
            idx = where(sectors[where_valid_jbt]==unique_sectors[isector])[0]
            o = ones(idx.size, dtype="int32")
            sector_bt_distribution[isector,:] = ndimage_sum(o, labels=job_building_types[where_valid_jbt[idx]], 
                                                            index=available_building_types)
            sector_bt_distribution[isector,:] = sector_bt_distribution[isector,:]/sector_bt_distribution[isector,:].sum()
            sector_index_mapping[unique_sectors[isector]] = isector
               
        # create a lookup table for zonal average per building type of sqft per employee 
        zone_average_dataset = Dataset(in_storage=in_storage, id_name=[], dataset_name="building_sqft_per_job", 
                                       in_table_name=zone_averages_table)
        zone_ids_in_zad = zone_average_dataset.get_attribute("zone_id").astype("int32")
        bt_in_zad = zone_average_dataset.get_attribute("building_type_id")
        sqft_in_zad = zone_average_dataset.get_attribute("building_sqft_per_job")
        zone_bt_lookup = zeros((zone_ids_in_zad.max()+1, bt_in_zad.max()+1)) 
        for i in range(zone_average_dataset.size()):
            zone_bt_lookup[zone_ids_in_zad[i], bt_in_zad[i]] = sqft_in_zad[i]
        counter_zero_capacity = 0
        counter_zero_distr = 0
        # iterate over parcels
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_non_home_based] == parcel)[0]
            capacity = non_res_sqft[idx_in_bldgs] - occupied[idx_in_bldgs]
            if capacity.sum() <= 0:
                counter_zero_capacity += idx_in_jobs.size
                continue
            this_jobs_sectors = sectors[job_index_non_home_based][idx_in_jobs]
            this_jobs_sqft_table = resize(jobs_sqft[idx_in_jobs], (idx_in_bldgs.size, idx_in_jobs.size))
            wn = jobs_sqft[idx_in_jobs] <= 0
            for i in range(idx_in_bldgs.size):
                this_jobs_sqft_table[i, where(wn)[0]] = zone_bt_lookup[jobs_zones[idx_in_jobs[wn]], bldg_types_in_bldgs[idx_in_bldgs[i]]]
            supply_demand_ratio = (resize(capacity, (capacity.size, 1))/this_jobs_sqft_table.astype("float32").sum(axis=0))/float(idx_in_jobs.size)*0.9
            if any(supply_demand_ratio < 1): # correct only if supply is smaller than demand 
                this_jobs_sqft_table = this_jobs_sqft_table * supply_demand_ratio
            probcomb = zeros(this_jobs_sqft_table.shape)
            bt = bldg_types_in_bldgs[idx_in_bldgs]
            ibt = building_type_dataset.get_id_index(bt)
            for i in range(probcomb.shape[0]):
                for j in range(probcomb.shape[1]):
                    probcomb[i,j] = sector_bt_distribution[sector_index_mapping[this_jobs_sectors[j]],ibt[i]]
            pcs = probcomb.sum(axis=0)
            probcomb = probcomb/pcs
            wz = where(pcs<=0)[0]
            counter_zero_distr += wz.size
            probcomb[:, wz] = 0 # to avoid nan values
            taken = zeros(capacity.shape)
            has_sqft = this_jobs_sqft_table > 0
            while True:
                if (has_sqft * probcomb).sum() <= 0:
                    break
                req =  (this_jobs_sqft_table * probcomb).sum(axis=0)
                maxi = req.max()
                wmaxi = where(req==maxi)[0]
                drawjob = sample_noreplace(arange(wmaxi.size), 1) # draw job from jobs with the maximum size
                imax_req = wmaxi[drawjob]
                weights = has_sqft[:,imax_req] * probcomb[:,imax_req]
                draw = probsample_noreplace(arange(probcomb.shape[0]), 1, resize(weights/weights.sum(), (probcomb.shape[0],)))
                if (taken[draw] + this_jobs_sqft_table[draw,imax_req]) > capacity[draw]:
                    probcomb[draw,imax_req]=0
                    continue
                taken[draw] = taken[draw] + this_jobs_sqft_table[draw,imax_req]
                building_ids[job_index_non_home_based[idx_in_jobs[imax_req]]] = bldg_ids_in_bldgs[idx_in_bldgs[draw]]
                probcomb[:,imax_req] = 0
            
        logger.log_status("%s non home based jobs (out of %s nhb jobs) were placed." % (
                                                                (building_ids[job_index_non_home_based]>0).sum(),
                                                                 job_index_non_home_based.size))
        logger.log_status("Unplaced due to zero capacity: %s" % counter_zero_capacity)
        logger.log_status("Unplaced due to zero distribution: %s" % counter_zero_distr)
        
        job_dataset.modify_attribute(name="building_id", data = building_ids)
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage, attributes=AttributeType.PRIMARY)
        logger.log_status("Done.")
#        idx = where(building_ids[job_index_non_home_based]<=0)[0]
#        unique_parcels = unique_values(parcel_ids[job_index_non_home_based[idx]])
#        rescapacity=[]
#        for parcel in unique_parcels:
#            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
#            rescapacity.append(non_res_sqft[idx_in_bldgs] - occupied[idx_in_bldgs])
#        print array(rescapacity).max()            
        
        
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

            