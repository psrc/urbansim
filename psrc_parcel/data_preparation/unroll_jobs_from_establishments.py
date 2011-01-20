# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from numpy import array, arange, cumsum, resize, clip, logical_and, where, concatenate, ones
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.sampling_toolbox import sample_noreplace
from urbansim_parcel.datasets.business_dataset import BusinessDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.building_dataset import BuildingDataset
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from urbansim_parcel.datasets.building_sqft_per_job_dataset import create_building_sqft_per_job_dataset

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
    
class UnrollJobsFromEstablishments:
    
    minimum_sqft = 1
    maximum_sqft = 4000
    number_of_jobs_attr = "jobs00"
    sqft_attr = "building_sqft_10vac"
    geography_id_attr = "zone_id"
    compute_sqft_per_job = True
    unplace_jobs_with_non_existing_buildings = True
    
    def run(self, in_storage, out_storage, business_table="business", jobs_table="jobs", control_totals_table=None):
        logger.log_status("Unrolling %s table." % business_table)
        # get attributes from the establisments table
        business_dataset = BusinessDataset(in_storage=in_storage, in_table_name=business_table)
        business_sizes = business_dataset.get_attribute(self.number_of_jobs_attr).astype("int32")
        sectors = business_dataset.get_attribute("sector_id")
        tazes = business_dataset.get_attribute(self.geography_id_attr).astype("int32")
        building_ids = array([], dtype='int32')
        if "building_id" in business_dataset.get_primary_attribute_names():
            building_ids = business_dataset.get_attribute("building_id")
        parcel_ids = array([], dtype='int32')
        if "parcel_id" in business_dataset.get_primary_attribute_names():
            parcel_ids = business_dataset.get_attribute("parcel_id")
        home_based = array([], dtype='int16')
        if "home_based" in business_dataset.get_primary_attribute_names():
            home_based = business_dataset.get_attribute("home_based")
        building_sqft = business_dataset.get_attribute(self.sqft_attr)
        building_sqft[building_sqft <= 0] = 0
        join_flags = None
        if "join_flag" in business_dataset.get_primary_attribute_names():
            join_flags = business_dataset.get_attribute("join_flag")
        impute_sqft_flag = None
        if "impute_building_sqft_flag" in business_dataset.get_primary_attribute_names():
            impute_sqft_flag = business_dataset.get_attribute("impute_building_sqft_flag")
        
        # inititalize jobs attributes
        total_size = business_sizes.sum()
        jobs_data = {}
        jobs_data["sector_id"] = resize(array([-1], dtype=sectors.dtype), total_size)
        jobs_data["building_id"] = resize(array([-1], dtype=building_ids.dtype), total_size)
        jobs_data["parcel_id"] = resize(array([-1], dtype=parcel_ids.dtype), total_size)
        jobs_data[self.geography_id_attr] = resize(array([-1], dtype=tazes.dtype), total_size)
        jobs_data["building_type"] = resize(array([-1], dtype=home_based.dtype), total_size)
        jobs_data["sqft"] = resize(array([], dtype=building_sqft.dtype), total_size)
        if join_flags is not None:
            jobs_data["join_flag"] = resize(array([], dtype=join_flags.dtype), total_size)
        if impute_sqft_flag is not None:
            jobs_data["impute_building_sqft_flag"] = resize(array([], dtype=impute_sqft_flag.dtype), total_size)
        
        indices = cumsum(business_sizes)
        # iterate over establishments. For each business create the corresponding number of jobs by filling the corresponding part 
        # of the arrays
        start_index=0
        for i in range(business_dataset.size()):
            end_index = indices[i]
            jobs_data["sector_id"][start_index:end_index] = sectors[i]
            if building_ids.size > 0:
                jobs_data["building_id"][start_index:end_index] = building_ids[i]
            if parcel_ids.size > 0:
                jobs_data["parcel_id"][start_index:end_index] = parcel_ids[i]
            jobs_data[self.geography_id_attr][start_index:end_index] = tazes[i]
            if home_based.size > 0:
                jobs_data["building_type"][start_index:end_index] = home_based[i]
            if self.compute_sqft_per_job:
                jobs_data["sqft"][start_index:end_index] = round((building_sqft[i]-building_sqft[i]/10.0)/float(business_sizes[i])) # sqft per employee
            else:
                jobs_data["sqft"][start_index:end_index] = building_sqft[i]
            if join_flags is not None:
                jobs_data["join_flag"][start_index:end_index] = join_flags[i]
            if impute_sqft_flag is not None:
                jobs_data["impute_building_sqft_flag"][start_index:end_index]  = impute_sqft_flag[i]
            start_index = end_index
            
        jobs_data["job_id"] = arange(total_size)+1
        if self.compute_sqft_per_job:
            jobs_data["sqft"] = clip(jobs_data["sqft"], 0, self.maximum_sqft)
            jobs_data["sqft"][logical_and(jobs_data["sqft"]>0, jobs_data["sqft"]<self.minimum_sqft)] = self.minimum_sqft
        
        # correct missing job_building_types
        wmissing_bt = where(jobs_data["building_type"]<=0)[0]
        if wmissing_bt.size > 0:
            jobs_data["building_type"][wmissing_bt] = 2 # assign non-homebased type for now. It can be re-classified in the assign_bldgs_to_jobs... script
        
        # create jobs table and write it out
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name="jobs",
                table_data=jobs_data
                )
        job_dataset = JobDataset(in_storage=storage)
        if self.unplace_jobs_with_non_existing_buildings:
            self.do_unplace_jobs_with_non_existing_buildings(job_dataset, out_storage)
        
        # Match to control totals (only eliminate jobs if control totals are smaller than the actual number of jobs). 
        if control_totals_table is not None:
            logger.log_status("Matching to control totals.")
            control_totals = ControlTotalDataset(what='employment', id_name=['zone_id', 'sector_id'], 
                                                 in_table_name=control_totals_table, in_storage=in_storage)
            control_totals.load_dataset(attributes=['zone_id', 'sector_id', 'jobs'])
            zones_sectors = control_totals.get_id_attribute()
            njobs = control_totals.get_attribute('jobs')
            remove = array([], dtype='int32')
            for i in range(zones_sectors.shape[0]):
                zone, sector = zones_sectors[i,:]
                in_sector = job_dataset.get_attribute("sector_id") == sector
                in_zone_in_sector = logical_and(in_sector, job_dataset.get_attribute("zone_id") == zone)
                if in_zone_in_sector.sum() <= njobs[i]:
                    continue
                to_be_removed = in_zone_in_sector.sum() - njobs[i]
                this_removal = 0
                not_considered = ones(job_dataset.size(), dtype='bool8')
                for unit in ['parcel_id', 'building_id', None]: # first consider jobs without parcel id, then without building_id, then all
                    if unit is not None:
                        wnunit = job_dataset.get_attribute(unit) <= 0
                        eligible = logical_and(not_considered, logical_and(in_zone_in_sector, wnunit))
                        not_considered[where(wnunit)] = False
                    else:
                        eligible = logical_and(not_considered, in_zone_in_sector)
                    eligible_sum = eligible.sum()
                    if eligible_sum > 0:
                        where_eligible = where(eligible)[0]
                        if eligible_sum <= to_be_removed-this_removal:
                            draw = arange(eligible_sum)
                        else:
                            draw = sample_noreplace(where_eligible, to_be_removed-this_removal, eligible_sum)
                        remove = concatenate((remove, where_eligible[draw]))
                        this_removal += draw.size
                        if this_removal >= to_be_removed:
                            break
                
            job_dataset.remove_elements(remove)
            logger.log_status("%s jobs removed." % remove.size)
            
        
        logger.log_status("Write jobs table.")
        job_dataset.write_dataset(out_table_name=jobs_table, out_storage=out_storage)
        logger.log_status("Created %s jobs." % job_dataset.size())
    
    def do_unplace_jobs_with_non_existing_buildings(self, jobs, in_storage):
        buildings = BuildingDataset(in_storage=in_storage)
        building_ids = jobs.get_attribute(buildings.get_id_name()[0])
        valid_building_ids_idx = where(building_ids > 0)[0]
        index = buildings.try_get_id_index(building_ids[valid_building_ids_idx])
        logger.log_status("%s jobs have non-existing locations and are unplaced from buildings (parcel_id and zone_id are not affected)." % where(index < 0)[0].size)
        jobs.modify_attribute(name="building_id", data=-1, index=valid_building_ids_idx[index < 0])

class UnrollJobsFromEstablishmentsWithZipcode(UnrollJobsFromEstablishments):
    
    number_of_jobs_attr = "employees"
    sqft_attr = "sqft_per_job"
    geography_id_attr = "zip_id"
    compute_sqft_per_job = False
    unplace_jobs_with_non_existing_buildings = False
    
class CreateBuildingSqftPerJobDataset:
    minimum_median = 25
    maximum_median = 2000
    def run(self, in_storage, out_storage):
        dataset_pool = DatasetPool(storage=in_storage, package_order=['psrc_parcel', 'urbanism_parcel', 'urbansim'] )
        ds = self._do_run(dataset_pool)
        logger.log_status("Write building_sqft_per_job table.")
        ds.write_dataset(out_storage=out_storage)
        
    def _do_run(self, dataset_pool):
        logger.log_status("Creating building_sqft_per_job table.")
        ds = create_building_sqft_per_job_dataset(dataset_pool, self.minimum_median, self.maximum_median)
        return ds
    
if __name__ == '__main__':
    #business_table = "est00_match_bldg2005_flag123457_flag12bldg"
    business_table = "businesses"
    control_totals_table = "employment_control_total_zone_2000_flattened"
    input_database_name = "psrc_2005_parcel_baseyear_data_prep_business_zip"
    #input_database_name = "psrc_2005_parcel_baseyear_change_20070713"
    #input_database_name = "psrc_2005_data_workspace_hana"
    #output_database_name = "psrc_2005_parcel_baseyear_data_prep_start"
    output_database_name = "psrc_2005_parcel_baseyear_data_prep_business_zip"
    input_cache = "/Users/hana/urbansim_cache/psrc/cache_source/2000"
    output_cache = "/Users/hana/urbansim_cache/psrc/data_preparation/stepI/2000"
    instorage = MysqlStorage().get(input_database_name)
    outstorage = MysqlStorage().get(output_database_name)
    #instorage = FltStorage().get(input_cache)
    #outstorage = FltStorage().get(output_cache)
    
    unrolling_businesses_with_zipcode = True # set this True for unrolling businesses that have zip codes (instead of zone, parcels and buildings) 
    
    if not unrolling_businesses_with_zipcode:
        UnrollJobsFromEstablishments().run(instorage, outstorage, business_table=business_table, control_totals_table=control_totals_table)
        CreateBuildingSqftPerJobDataset().run(in_storage=outstorage, out_storage=outstorage)
    else:
        UnrollJobsFromEstablishmentsWithZipcode().run(instorage, outstorage, business_table=business_table, control_totals_table=None)
