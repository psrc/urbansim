from numpy import cumsum, zeros, where, in1d, logical_and, logical_not, logical_or, ones, arange
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import DatasetSubset
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.logger import logger

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
    
class CreateJobsFromQCEW:
    number_of_jobs_attr = "jobs10"
    
    def run(self, in_storage, business_dsname="business"):
        dataset_pool = DatasetPool(storage=in_storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'] )
        allbusinesses = dataset_pool.get_dataset(business_dsname)
        parcels = dataset_pool.get_dataset('parcel')
        buildings = dataset_pool.get_dataset('building')
        parcels.compute_variables(["urbansim_parcel.parcel.residential_units", "number_of_buildings = parcel.number_of_agents(building)", 
                                   "non_residential_sqft = (parcel.aggregate(building.non_residential_sqft)).astype(int32)"], 
                                  dataset_pool=dataset_pool)
        is_valid_business = ones(allbusinesses.size(), dtype='bool8')
        parcels_not_matched = in1d(allbusinesses["parcel_id"], parcels.get_id_attribute(), invert=True)
        if(sum(parcels_not_matched) > 0):
            is_valid_business[where(parcels_not_matched)] = False
            logger.log_warning(message="No parcel exists for %s businesses (%s jobs)" % (sum(parcels_not_matched), 
                                                                                         allbusinesses[self.number_of_jobs_attr][where(parcels_not_matched)].sum()))
        
        zero_size = allbusinesses[self.number_of_jobs_attr].round() == 0
        if(sum(zero_size) > 0):
            is_valid_business[where(zero_size)] = False
            logger.log_warning(message="%s businesses are of size 0." % sum(zero_size))
        
        businesses = DatasetSubset(allbusinesses, index=where(is_valid_business)[0])
            
        parcels.add_attribute(name="number_of_workplaces", data=parcels.sum_dataset_over_ids(businesses, constant=1))
        
        has_single_res_buildings = logical_and(logical_and(parcels["number_of_buildings"] == 1, parcels["residential_units"] > 0), parcels["non_residential_sqft"] == 0)
        parcels.add_attribute(data=has_single_res_buildings.astype("int32"), name="buildings_code")
        has_mult_res_buildings = logical_and(logical_and(parcels["number_of_buildings"] > 1, parcels["residential_units"] > 0), parcels["non_residential_sqft"] == 0)
        parcels.modify_attribute("buildings_code", data=2*ones(sum(has_mult_res_buildings)), index=where(has_mult_res_buildings))
        has_single_nonres_buildings = logical_and(logical_and(parcels["number_of_buildings"] == 1, parcels["non_residential_sqft"] > 0), parcels["residential_units"] == 0)
        parcels.modify_attribute("buildings_code", data=3*ones(sum(has_single_nonres_buildings)), index=where(has_single_nonres_buildings))
        has_mult_nonres_buildings = logical_and(logical_and(parcels["number_of_buildings"] > 1, parcels["non_residential_sqft"] > 0), parcels["residential_units"] == 0)
        parcels.modify_attribute("buildings_code", data=4*ones(sum(has_mult_nonres_buildings)), index=where(has_mult_nonres_buildings))
        has_single_mixed_buildings = logical_and(logical_and(parcels["number_of_buildings"] == 1, parcels["residential_units"] > 0), parcels["non_residential_sqft"] > 0)
        parcels.modify_attribute("buildings_code", data=5*ones(sum(has_single_mixed_buildings)), index=where(has_single_mixed_buildings))
        has_mult_mixed_buildings = logical_and(logical_and(parcels["number_of_buildings"] > 1, parcels["residential_units"] > 0), parcels["non_residential_sqft"] > 0)
        parcels.modify_attribute("buildings_code", data=6*ones(sum(has_mult_mixed_buildings)), index=where(has_mult_mixed_buildings))
        has_no_building = parcels["number_of_buildings"] == 0
        parcels.modify_attribute("buildings_code", data=7*ones(sum(has_no_building)), index=where(has_no_building))
        
        business_sizes = businesses[self.number_of_jobs_attr].round().astype("int32") 
        business_location = {}
        business_location1wrkpl = zeros(businesses.size(), dtype="int32")
        for ibusid in range(businesses.size()):
            bldgids = buildings['building_id'][buildings['parcel_id'] == businesses['parcel_id'][ibusid]]
            business_location[businesses['business_id'][ibusid]] = bldgids
            if bldgids.size == 1:
                business_location1wrkpl[ibusid] = bldgids[0]
            elif bldgids.size > 1:
                business_location1wrkpl[ibusid] = bldgids[sample_noreplace(arange(bldgids.size), 1)] 
        
        home_based = zeros(business_sizes.sum(), dtype="bool8")
        job_building_id = zeros(business_sizes.sum(), dtype="int32")
        job_array_labels = businesses['business_id'].repeat(business_sizes)
        processed_bindicator = zeros(businesses.size(), dtype="bool8")
        logger.log_status("Total number of jobs: %s" % home_based.size)
        
        # single worker in 1 residential building
        idx_single_worker = where(business_sizes == 1)[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])
        idx_sngl_wrk_1bld_fit = where(bcode == 1)[0]
        home_based[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_1bld_fit]])] = True
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_1bld_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_1bld_fit]]
        processed_bindicator[idx_single_worker[idx_sngl_wrk_1bld_fit]] = True
        logger.log_status("1. %s jobs set as home-based due to single worker x 1 residential building fit." % idx_sngl_wrk_1bld_fit.size)
        
        # single worker in multiple residential buildings
        idx_single_worker = where(logical_and(processed_bindicator==0, business_sizes == 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])
        idx_sngl_wrk_multbld_fit = where(bcode == 2)[0]
        home_based[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_multbld_fit]])] = True
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_multbld_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_multbld_fit]]
        processed_bindicator[idx_single_worker[idx_sngl_wrk_multbld_fit]] = True
        logger.log_status("2. %s jobs set as home-based due to single worker x multiple residential buildings fit." % idx_sngl_wrk_multbld_fit.size)
               
        # single worker in single non-res building
        idx_single_worker = where(logical_and(processed_bindicator==0, business_sizes == 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])        
        idx_sngl_wrk_single_nonres_fit = where(bcode == 3)[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_single_nonres_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_single_nonres_fit]]        
        processed_bindicator[idx_single_worker[idx_sngl_wrk_single_nonres_fit]] = True
        logger.log_status("3. %s jobs could be placed due to single worker x single non-res building fit." % idx_sngl_wrk_single_nonres_fit.size)        
        
        # single worker in multiple non-res building 
        idx_single_worker = where(logical_and(processed_bindicator==0, business_sizes == 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])        
        idx_sngl_wrk_mult_nonres_fit = where(bcode == 4)[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_mult_nonres_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_mult_nonres_fit]]        
        processed_bindicator[idx_single_worker[idx_sngl_wrk_mult_nonres_fit]] = True
        logger.log_status("4. %s jobs could be placed due to single worker x multiple non-res building fit." % idx_sngl_wrk_mult_nonres_fit.size)        

                
        # single worker in single mixed-use building
        idx_single_worker = where(logical_and(processed_bindicator==0, business_sizes == 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])        
        idx_sngl_wrk_smu_fit = where(bcode == 5)[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_smu_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_smu_fit]]                
        processed_bindicator[idx_single_worker[idx_sngl_wrk_smu_fit]] = True
        logger.log_status("5. %s jobs in single worker x single mixed-use building." % idx_sngl_wrk_smu_fit.size)          
        
        # single worker in multiple mixed-use building
        idx_single_worker = where(logical_and(processed_bindicator==0, business_sizes == 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_single_worker])        
        idx_sngl_wrk_mmu_fit = where(bcode == 6)[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_single_worker[idx_sngl_wrk_mmu_fit]])] = business_location1wrkpl[idx_single_worker[idx_sngl_wrk_mmu_fit]]                        
        processed_bindicator[idx_single_worker[idx_sngl_wrk_mmu_fit]] = True
        logger.log_status("6. %s jobs in single worker x multiple mixed-use building." % idx_sngl_wrk_mmu_fit.size)            

        # 2+ workers in single residential building
        idx_more_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        #res_units = parcels.get_attribute_by_id("residential_units", businesses["parcel_id"][idx_more_workers])
        #idx_mult_wrk_multdu_fit = where(res_units >= 1)[0]
        #home_based[in1d(job_array_labels, businesses['business_id'][idx_more_workers[idx_mult_wrk_multdu_fit]])] = True
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_more_workers])
        idx_sngl_wrk_fit = where(bcode == 1)[0]
        processed_bindicator[idx_more_workers[idx_sngl_wrk_fit]] = True        
        #logger.log_status("9. %s jobs set as home-based due to having 2+ workers x residential." % idx_mult_wrk_multdu_fit.size)
        logger.log_status("9. %s jobs (%s businesses) in 2+ worker x single residential building." % (
            business_sizes[idx_more_workers[idx_sngl_wrk_fit]].sum(), idx_sngl_wrk_fit.size))
        
        # 2+ workers in multiple residential building
        idx_more_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_more_workers])
        idx_sngl_wrk_fit = where(bcode == 2)[0]
        processed_bindicator[idx_more_workers[idx_sngl_wrk_fit]] = True        
        logger.log_status("10. %s jobs (%s businesses) in 2+ worker x multiple residential building." % (
            business_sizes[idx_more_workers[idx_sngl_wrk_fit]].sum(), idx_sngl_wrk_fit.size))        


        # single workplace, 2+ workers in single non-res or mixed building (11.)
        idx_2plus_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_2plus_workers])
        workplace_filter = parcels.get_attribute_by_id("number_of_workplaces", businesses["parcel_id"][idx_2plus_workers])
        idx_sngl_wrkplace_2plus_workers = where(logical_and(logical_or(bcode==3, bcode==5), workplace_filter==1))[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]])] = business_location1wrkpl[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]]                        
        processed_bindicator[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]] = True
        logger.log_status("11. %s jobs (%s businesses) could be placed due to single workplace x 2+ workers x single non-res/mixed building fit." % (
            business_sizes[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]].sum(), idx_sngl_wrkplace_2plus_workers.size))
        
        # single workplace, 2+ workers in multiple non-res or mixed building (12.)
        idx_2plus_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_2plus_workers])
        workplace_filter = parcels.get_attribute_by_id("number_of_workplaces", businesses["parcel_id"][idx_2plus_workers])
        idx_sngl_wrkplace_2plus_workers = where(logical_and(logical_or(bcode==4, bcode==6), workplace_filter==1))[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]])] = business_location1wrkpl[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]]                                
        processed_bindicator[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]] = True
        logger.log_status("12. %s jobs (%s businesses) could be placed due to single workplace x 2+ workers x multiple non-res/mixed building fit." % (
            business_sizes[idx_2plus_workers[idx_sngl_wrkplace_2plus_workers]].sum(), idx_sngl_wrkplace_2plus_workers.size))

        # multiple workplaces, 2+ workers in single non-res or mixed building
        idx_2plus_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_2plus_workers])
        workplace_filter = parcels.get_attribute_by_id("number_of_workplaces", businesses["parcel_id"][idx_2plus_workers])
        idx_mult_wrkplace_2plus_workers = where(logical_and(logical_or(bcode==3, bcode==5), workplace_filter > 1))[0]
        job_building_id[in1d(job_array_labels, businesses['business_id'][idx_2plus_workers[idx_mult_wrkplace_2plus_workers]])] = business_location1wrkpl[idx_2plus_workers[idx_mult_wrkplace_2plus_workers]]                                        
        processed_bindicator[idx_2plus_workers[idx_mult_wrkplace_2plus_workers]] = True
        logger.log_status("13. %s jobs (%s businesses) could be placed due to multiple workplaces x 2+ workers x single non-res/mixed building fit." % (
            business_sizes[idx_2plus_workers[idx_mult_wrkplace_2plus_workers]].sum(), idx_mult_wrkplace_2plus_workers.size))
        
        # multiple workplaces, 2+ workers in multiple non-res or mixed building
        idx_2plus_workers = where(logical_and(processed_bindicator==0, business_sizes > 1))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_2plus_workers])
        workplace_filter = parcels.get_attribute_by_id("number_of_workplaces", businesses["parcel_id"][idx_2plus_workers])
        idx_mult_wrkplace_2plus_workers = where(logical_and(logical_or(bcode==4, bcode==6), workplace_filter > 1))[0]
        processed_bindicator[idx_2plus_workers[idx_mult_wrkplace_2plus_workers]] = True
        logger.log_status("14. %s jobs (%s businesses) could be placed due to multiple workplaces x 2+ workers x multiple non-res/mixed building fit." % (
            business_sizes[idx_2plus_workers[idx_mult_wrkplace_2plus_workers]].sum(), idx_mult_wrkplace_2plus_workers.size))
        
        # jobs in messy buildings
        idx_worker = where(logical_and(processed_bindicator==0, business_sizes > 0))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_worker])
        idx_messy_fit = where(bcode == 0)[0]
        processed_bindicator[idx_worker[idx_messy_fit]] = True
        logger.log_status("%s jobs (%s businesses) could not be placed due to messy buildings." % (
            business_sizes[idx_worker[idx_messy_fit]].sum(), idx_messy_fit.size))
        
        # jobs in non-existing buildings
        idx_worker = where(logical_and(processed_bindicator==0, business_sizes > 0))[0]
        nbldgs = parcels.get_attribute_by_id("number_of_buildings", businesses["parcel_id"][idx_worker])
        idx_nonexist_fit = where(nbldgs == 0)[0]
        processed_bindicator[idx_worker[idx_nonexist_fit]] = True
        logger.log_status("%s jobs (%s businesses) could not be placed due to non-existing buildings." % (
            business_sizes[idx_worker[idx_nonexist_fit]].sum(), idx_nonexist_fit.size))  
        
        logger.log_status("So far %s percent home-based jobs." % round(home_based.sum()/(home_based.size/100.),2))
        logger.log_status("So far %s percent (%s) jobs (%s businesses) processed. %s jobs (%s businesses) remain to be processed." % \
                          (round(business_sizes[processed_bindicator].sum()/(home_based.size/100.),2),
                           business_sizes[processed_bindicator].sum(), processed_bindicator.sum(),
                          business_sizes[logical_not(processed_bindicator)].sum(), business_sizes[logical_not(processed_bindicator)].size))
        pass
    
if __name__ == '__main__':
    business_dataset_name = "business"
    input_cache = "/Users/hana/workspace/data/psrc_parcel/job_data/qcew_data/2010"
    instorage = FltStorage().get(input_cache)
    CreateJobsFromQCEW().run(instorage, business_dsname=business_dataset_name)