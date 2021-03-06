# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from numpy import array, where, logical_and, arange, ones, cumsum, zeros, alltrue, absolute, resize, any, floor, maximum, int32, logical_not, logical_or
from numpy.random import seed
from opus_core.ndimage import sum as ndimage_sum
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.sampling_toolbox import sample_noreplace, sample_replace, probsample_noreplace, probsample_replace
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.misc import unique, write_to_text_file
from opus_core.model import Model
from opus_core.variables.attribute_type import AttributeType
from urbansim.datasets.job_dataset import JobDataset
from unroll_jobs_from_establishments import UnrollJobsFromEstablishments
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from unroll_jobs_from_establishments import CreateBuildingSqftPerJobDataset

class MysqlStorage:
    def get(self, database):
        db_config = ScenarioDatabaseConfiguration()
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(database)
        
        storage = StorageFactory().get_storage(
            'sql_storage',
            storage_location = db)
        return storage

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
class AssignBuildingsToJobs:
    
    def run(self, job_dataset, dataset_pool, out_storage=None, jobs_table="jobs"):
        """
        Algorithm:
            1. For all non_home_based jobs that have parcel_id assigned but no building_id, try
                to choose a building from all buildings in that parcel. Draw the building with probabilities
                given by the sector-building_type distribution. The job sizes are
                fitted into the available space (the attribute job.sqft is updated).
            2. For all non_home_based jobs for which no building was found in step 1, check
                if the parcel has residential buildings. In such a case, re-assign the jobs to be
                home-based.
                Otherwise, if sum of non_residential_sqft over the involved buildings is 0,
                for all jobs that have impute_building_sqft_flag=True draw a building using
                the sector-building_type distribution and impute the corresponding sqft to 
                the non_residential_sqft of that building.
            3. For all home_based jobs that have parcel_id assigned but no building_id, try
                to choose a building from all buildings in that parcel. 
                The capacity of a single-family building is determined from sizes of the households living there 
                (for each household the minimum of number of members and 2 is taken). 
                For multi-family buildings the capacity is 50.
            4. Assign a building type to jobs that have missing building type. It is sampled 
                from the regional-wide distribution of home based and non-home based jobs.
            5. Update the table 'building_sqft_per_job' using the updated job.sqft.
        'in_storage' should contain the jobs table and the zone_averages_table. The 'dataset_pool_storage'
        should contain all other tables needed (buildings, households, building_types). 
        """
        parcel_ids = job_dataset.get_attribute("parcel_id")
        building_ids = job_dataset.get_attribute("building_id")
        home_base_status = job_dataset.get_attribute("home_based_status")
        sectors = job_dataset.get_attribute("sector_id")
        
        is_considered = logical_and(parcel_ids > 0, building_ids <= 0) # jobs that have assigned parcel but not building
        job_index_home_based = where(logical_and(is_considered, home_base_status == 0))[0]
        is_governmental_job = sectors == 18
        is_edu_job = sectors == 19
        job_index_governmental = where(logical_and(is_considered, is_governmental_job))[0]
        job_index_edu = where(logical_and(is_considered, is_edu_job))[0]
        
        building_dataset = dataset_pool.get_dataset('building')
        parcel_ids_in_bldgs = building_dataset.get_attribute("parcel_id")
        bldg_ids_in_bldgs = building_dataset.get_id_attribute()
        bldg_types_in_bldgs = building_dataset.get_attribute("building_type_id")
        
        non_res_sqft = building_dataset.get_attribute("non_residential_sqft")

        preferred_nhb_btypes =   (building_dataset['building.building_type_id'] == 3) + \
                                (building_dataset['building.building_type_id'] == 8) + \
                                (building_dataset['building.building_type_id'] == 13) + \
                                (building_dataset['building.building_type_id'] == 20) + \
                                (building_dataset['building.building_type_id'] == 21)
        non_res_sqft_preferred =  non_res_sqft  * preferred_nhb_btypes              
                                          
        is_governmental = building_dataset.compute_variables([
            "numpy.logical_and(building.disaggregate(building_type.generic_building_type_id == 7), building.building_type_id <> 18)"],
                                                                     dataset_pool=dataset_pool)
        idx_gov = where(is_governmental)[0]
        is_edu = building_dataset['building.building_type_id'] == 18
        idx_edu = where(is_edu)[0]
        
        bldgs_is_residential = logical_and(logical_not(logical_or(is_governmental, is_edu)), 
                                           building_dataset.compute_variables(["urbansim_parcel.building.is_residential"], 
                                                           dataset_pool=dataset_pool))
        
        bldgs_isnot_residential = logical_not(bldgs_is_residential)
        
        # assign buildings to educational jobs randomly
        unique_parcels = unique(parcel_ids[job_index_edu])
        logger.log_status("Placing educational jobs ...")
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs[idx_edu] == parcel)[0]
            if idx_in_bldgs.size <= 0:
                continue
            idx_in_jobs = where(parcel_ids[job_index_edu] == parcel)[0]
            draw = sample_replace(idx_in_bldgs, idx_in_jobs.size)
            building_ids[job_index_edu[idx_in_jobs]] = bldg_ids_in_bldgs[idx_edu[draw]]
        logger.log_status("%s educational jobs (out of %s edu. jobs) were placed." % (
                                        (building_ids[job_index_edu]>0).sum(), job_index_edu.size))
        
        # assign buildings to governmental jobs randomly
        unique_parcels = unique(parcel_ids[job_index_governmental])
        logger.log_status("Placing governmental jobs ...")
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs[idx_gov] == parcel)[0]
            if idx_in_bldgs.size <= 0:
                continue
            idx_in_jobs = where(parcel_ids[job_index_governmental] == parcel)[0]
            draw = sample_replace(idx_in_bldgs, idx_in_jobs.size)
            building_ids[job_index_governmental[idx_in_jobs]] = bldg_ids_in_bldgs[idx_gov[draw]]
        logger.log_status("%s governmental jobs (out of %s gov. jobs) were placed." % (
                        (building_ids[job_index_governmental]>0).sum(), job_index_governmental.size))
        logger.log_status("The unplaced governmental jobs will be added to the non-home based jobs.")
        
        #tmp = unique(parcel_ids[job_index_governmental][building_ids[job_index_governmental]<=0])
        #output_dir =  "/Users/hana"
        #write_to_text_file(os.path.join(output_dir, 'parcels_with_no_gov_bldg.txt'), tmp, delimiter='\n')
        
        # consider the unplaced governmental jobs together with other non-home-based jobs
        is_now_considered = logical_and(is_considered, building_ids <= 0)
        job_index_non_home_based = where(logical_and(is_now_considered, logical_or(home_base_status == 0, is_governmental_job)))[0]
                                    
        # assign buildings to non_home_based jobs based on available space
        unique_parcels = unique(parcel_ids[job_index_non_home_based])
        # iterate over parcels
        logger.log_status("Placing non-home-based jobs ...")
        nhb_not_placed = 0
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            if idx_in_bldgs.size <= 0:
                continue
            idx_in_jobs = where(parcel_ids[job_index_non_home_based] == parcel)[0]
            # sample proportionally to the building size
            weights = non_res_sqft_preferred[idx_in_bldgs] # 1.preference: preferred building types with non-res sqft 
            if weights.sum() <= 0:
                weights = preferred_nhb_btypes[idx_in_bldgs] # 2.preference: preferred building types
                if weights.sum() <= 0:
                    weights = non_res_sqft[idx_in_bldgs] # 3.preference: any building with non-res sqft 
                    if weights.sum() <= 0: 
                        weights = bldgs_isnot_residential[idx_in_bldgs] # 4.preference: any non-res building
                        if weights.sum() <= 0: 
                            nhb_not_placed = nhb_not_placed + idx_in_jobs.size
                            continue
            draw = probsample_replace(idx_in_bldgs, idx_in_jobs.size, weights/float(weights.sum()))
            building_ids[job_index_non_home_based[idx_in_jobs]] = bldg_ids_in_bldgs[draw]
            
        logger.log_status("%s non home based jobs (out of %s nhb jobs) were placed. No capacity in buildings for %s jobs." % (
                                                                (building_ids[job_index_non_home_based]>0).sum(),
                                                                 job_index_non_home_based.size, nhb_not_placed))
        
        job_dataset.modify_attribute(name="building_id", data = building_ids)
        
        # re-classify unplaced non-home based jobs to home-based if parcels contain residential buildings

        is_now_considered = logical_and(parcel_ids > 0, building_ids <= 0)
        job_index_non_home_based_unplaced = where(logical_and(is_now_considered, 
                                               logical_and(home_base_status == 0, logical_not(is_governmental_job))))[0]
        unique_parcels = unique(parcel_ids[job_index_non_home_based_unplaced])

        logger.log_status("Try to reclassify non-home-based jobs (excluding governmental jobs) ...")
        nhb_reclass = 0
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            if idx_in_bldgs.size <= 0:
                continue
            idx_in_jobs = where(parcel_ids[job_index_non_home_based_unplaced] == parcel)[0]
            where_residential = where(bldgs_is_residential[idx_in_bldgs])[0]
            if where_residential.size > 0:
                #home_base_status[job_index_non_home_based_unplaced[idx_in_jobs]] = 1 # set to home-based jobs
                nhb_reclass = nhb_reclass + idx_in_jobs.size
            else:
                draw = sample_replace(idx_in_bldgs, idx_in_jobs.size)
                #building_ids[job_index_non_home_based_unplaced[idx_in_jobs]] = bldg_ids_in_bldgs[draw]

        #job_dataset.modify_attribute(name="home_base_status", data = home_base_status)
        #job_dataset.modify_attribute(name="building_id", data = building_ids)
        
        job_index_home_based = where(logical_and(is_considered, home_base_status == 1))[0]
        logger.log_status("%s non-home based jobs reclassified as home-based." % nhb_reclass)

        # home_based jobs
        unique_parcels = unique(parcel_ids[job_index_home_based])
        capacity_in_buildings = building_dataset.compute_variables([
                          "clip_to_zero(urbansim_parcel.building.total_home_based_job_space-building.aggregate(job.home_based_status==1))"],
                             dataset_pool=dataset_pool)
        parcels_with_exceeded_capacity = []
        # iterate over parcels
        logger.log_status("Placing home-based jobs ...")
        for parcel in unique_parcels:
            idx_in_bldgs = where(parcel_ids_in_bldgs == parcel)[0]
            idx_in_jobs = where(parcel_ids[job_index_home_based] == parcel)[0]
            capacity = capacity_in_buildings[idx_in_bldgs]
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
        
        # assign building type where missing
        # determine regional distribution
        idx_home_based = where(home_base_status == 1)[0]
        idx_non_home_based = where(home_base_status == 0)[0]
        idx_bt_missing = where(home_base_status <= 0)[0]
        if idx_bt_missing.size > 0:
            # sample building types
            sample_bt = probsample_replace(array([1,0]), idx_bt_missing.size, 
               array([idx_home_based.size, idx_non_home_based.size])/float(idx_home_based.size + idx_non_home_based.size))
            # coerce to int32 (on a 64 bit machine, sample_bt will be of type int64)
            home_base_status[idx_bt_missing] = sample_bt.astype(int32)
            job_dataset.modify_attribute(name="home_based_status", data = home_base_status) 
        
        if out_storage is not None:
            job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage, attributes=AttributeType.PRIMARY)
        logger.log_status("Assigning building_id to jobs done.")

        
if __name__ == '__main__':
    # Uncomment the right instorage and outstorage.
    # input/output_database_name is used only if MysqlStorage is uncommented.
    # input/output_cache is used only if FltStorage is uncommented.
    input_database_name = "psrc_2005_parcel_baseyear_change_20070613"
    output_database_name = "psrc_2005_data_workspace_hana"
    input_cache =  "/Users/hana/urbansim_cache/psrc/data_preparation/cache/2000"
    output_cache = "/Users/hana/urbansim_cache/psrc/data_preparation/stepIV"
    input_cache =  "/workspace/work/psrc/unroll_jobs/unroll_jobs_from_establishments_cache"
    output_cache = "/workspace/work/psrc/unroll_jobs/output"
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/jobsdataprep/revised/2000_jobs_from_establishments"
    output_cache = "/Users/hana/workspace/data/psrc_parcel/jobsdataprep/revised/2000_assigned_jobs"
    #instorage = MysqlStorage().get(input_database_name)
    #outstorage = MysqlStorage().get(output_database_name)
    instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)

    pool_storage = instorage
    job_dataset = JobDataset(in_storage=instorage, in_table_name = "jobs")
    dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=pool_storage)
    seed(1)
    
    AssignBuildingsToJobs().run(job_dataset, dataset_pool, out_storage=outstorage)

