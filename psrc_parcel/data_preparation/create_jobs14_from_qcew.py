from numpy import cumsum, zeros, where, in1d, logical_and, logical_not, logical_or, ones, arange, unique, maximum, vstack, array, tile
from numpy.random import shuffle, seed
from math import ceil
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.logger import logger

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
    
class CreateJobsFromQCEW:
    number_of_jobs_attr = "job_count"
    
    def run(self, in_storage, business_dsname="business"):
        dataset_pool = DatasetPool(storage=in_storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'] )
        seed(1)
        allbusinesses = dataset_pool.get_dataset(business_dsname)
        parcels = dataset_pool.get_dataset('parcel')
        buildings = dataset_pool.get_dataset('building')
        parcels.compute_variables(["urbansim_parcel.parcel.residential_units", "number_of_buildings = parcel.number_of_agents(building)", 
                                   "non_residential_sqft = (parcel.aggregate(building.non_residential_sqft)).astype(int32)",
                                   "number_of_res_buildings = parcel.aggregate(urbansim_parcel.building.is_residential)",
                                   "number_of_nonres_buildings = parcel.aggregate(urbansim_parcel.building.is_non_residential)",
                                   "number_of_mixed_use_buildings = parcel.aggregate(urbansim_parcel.building.is_generic_building_type_6)"
                                   ], 
                                  dataset_pool=dataset_pool)
        restypes = [12, 4, 19, 11, 34, 10, 33]
        reslutypes = [13,14,15,24]
        is_valid_business = ones(allbusinesses.size(), dtype='bool8')
        parcels_not_matched = logical_and(in1d(allbusinesses["parcel_id"], parcels.get_id_attribute(), invert=True), allbusinesses["parcel_id"] > 0)
        if(parcels_not_matched.sum() > 0):
            is_valid_business[where(parcels_not_matched)] = False
            logger.log_warning(message="No parcel exists for %s businesses (%s jobs)" % (parcels_not_matched.sum(), 
                                                                                         allbusinesses[self.number_of_jobs_attr][where(parcels_not_matched)].sum()))
        zero_parcel = allbusinesses["parcel_id"]<=0
        if zero_parcel.sum() > 0:
            is_valid_business[where(zero_parcel)] = False
            logger.log_warning(message="%s businesses (%s jobs) located on zero parcel_id" % (zero_parcel.sum(), 
                                                                                         allbusinesses[self.number_of_jobs_attr][where(zero_parcel)].sum()))            
            
        zero_size = logical_and(is_valid_business, allbusinesses[self.number_of_jobs_attr].round() == 0)
        if(sum(zero_size) > 0):
            is_valid_business[where(zero_size)] = False
            logger.log_warning(message="%s businesses are of size 0." % sum(zero_size))
        
        businesses = DatasetSubset(allbusinesses, index=where(is_valid_business)[0])
            
        parcels.add_attribute(name="number_of_workplaces", data=parcels.sum_dataset_over_ids(businesses, constant=1))
        
        has_single_res_buildings = logical_and(parcels["number_of_buildings"] == 1, parcels["number_of_res_buildings"] == 1) # 1 (1 residential)
        parcels.add_attribute(data=has_single_res_buildings.astype("int32"), name="buildings_code")
        has_mult_res_buildings = logical_and(parcels["number_of_buildings"] > 1,  parcels["number_of_nonres_buildings"] == 0) # 2 (mult residential)
        parcels.modify_attribute("buildings_code", data=2*ones(has_mult_res_buildings.sum()), index=where(has_mult_res_buildings)) 
        has_single_nonres_buildings = logical_and(logical_and(parcels["number_of_buildings"] == 1, parcels["number_of_nonres_buildings"] == 1), parcels["number_of_mixed_use_buildings"] == 0) # 3 (1 non-res)
        parcels.modify_attribute("buildings_code", data=3*ones(has_single_nonres_buildings.sum()), index=where(has_single_nonres_buildings)) 
        has_mult_nonres_buildings = logical_and(logical_and(parcels["number_of_buildings"] > 1, parcels["number_of_res_buildings"] == 0), parcels["number_of_mixed_use_buildings"] == 0) # 4 (mult non-res)
        parcels.modify_attribute("buildings_code", data=4*ones(has_mult_nonres_buildings.sum()), index=where(has_mult_nonres_buildings))
        has_single_mixed_buildings = logical_and(parcels["number_of_buildings"] == 1, parcels["number_of_mixed_use_buildings"] == 1) # 5 (1 mixed-use)
        parcels.modify_attribute("buildings_code", data=5*ones(has_single_mixed_buildings.sum()), index=where(has_single_mixed_buildings))
        has_mult_mixed_buildings = logical_and(parcels["number_of_buildings"] > 1, 
                                               logical_or(logical_and(parcels["number_of_res_buildings"] > 0, parcels["number_of_nonres_buildings"] > 0), 
                                                          logical_or(parcels["number_of_mixed_use_buildings"] > 1, 
                                                                     logical_and(parcels["number_of_res_buildings"] == 0, 
                                                                                 parcels["number_of_mixed_use_buildings"] > 0)))) # 6
        parcels.modify_attribute("buildings_code", data=6*ones(has_mult_mixed_buildings.sum()), index=where(has_mult_mixed_buildings))
        has_no_building_res_lutype = logical_and(parcels["number_of_buildings"] == 0, in1d(parcels["land_use_type_id"], reslutypes)) # 7 (vacant with res LU type)
        parcels.modify_attribute("buildings_code", data=7*ones(has_no_building_res_lutype.sum()), index=where(has_no_building_res_lutype)) 
        has_no_building_nonres_lutype = logical_and(parcels["number_of_buildings"] == 0, in1d(parcels["land_use_type_id"], reslutypes)==0) # 8 (vacant with non-res LU type)
        parcels.modify_attribute("buildings_code", data=8*ones(has_no_building_nonres_lutype.sum()), index=where(has_no_building_nonres_lutype))
        
        business_sizes = businesses[self.number_of_jobs_attr].round().astype("int32") 
        business_location = {}
        business_location1wrkpl = zeros(businesses.size(), dtype="int32")
        business_location1wrkplres = zeros(businesses.size(), dtype="int32")
        business_ids = businesses.get_id_attribute()
        # sample one building for cases when sampling is required.
        for ibusid in range(businesses.size()):
            idx = where(buildings['parcel_id'] == businesses['parcel_id'][ibusid])[0]
            bldgids = buildings['building_id'][idx]
            business_location[business_ids[ibusid]] = bldgids
            if bldgids.size == 1:
                business_location1wrkpl[ibusid] = bldgids[0]
            elif bldgids.size > 1:
                business_location1wrkpl[ibusid] = bldgids[sample_noreplace(arange(bldgids.size), 1)]
                if buildings['residential_units'][idx].sum() > 0:
                    # Residential buildings are sampled with probabilities proportional to residential units
                    business_location1wrkplres[ibusid] = bldgids[probsample_noreplace(arange(bldgids.size), 1, prob_array=buildings['residential_units'][idx])]
                else:
                    business_location1wrkplres[ibusid] = business_location1wrkpl[ibusid]
        
        home_based = zeros(business_sizes.sum(), dtype="bool8")
        job_building_id = zeros(business_sizes.sum(), dtype="int32")
        job_array_labels = business_ids.repeat(business_sizes)
        job_assignment_case = zeros(business_sizes.sum(), dtype="int32")
        processed_bindicator = zeros(businesses.size(), dtype="bool8")
        business_codes = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"])
        business_nworkplaces = parcels.get_attribute_by_id("number_of_workplaces", businesses["parcel_id"])
        logger.log_status("Total number of jobs: %s" % home_based.size)
        
        # 1. 1-2 worker business in 1 residential building
        idx_sngl_wrk_1bld_fit = where(logical_and(business_sizes < 3, business_codes == 1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_1bld_fit])
        home_based[jidx] = True
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_1bld_fit].repeat(business_sizes[idx_sngl_wrk_1bld_fit])
        job_assignment_case[jidx] = 1
        processed_bindicator[idx_sngl_wrk_1bld_fit] = True
        logger.log_status("1. %s jobs (%s businesses) set as home-based due to 1-2 worker x 1 residential building fit." % (
            business_sizes[idx_sngl_wrk_1bld_fit].sum(), idx_sngl_wrk_1bld_fit.size))
        
        # 2. 1-2 worker business in multiple residential buildings
        idx_sngl_wrk_multbld_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 2))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_multbld_fit])
        home_based[jidx] = True
        job_building_id[jidx] = business_location1wrkplres[idx_sngl_wrk_multbld_fit].repeat(business_sizes[idx_sngl_wrk_multbld_fit])
        job_assignment_case[jidx] = 2
        processed_bindicator[idx_sngl_wrk_multbld_fit] = True
        logger.log_status("2. %s jobs (%s businesses) set as home-based due to 1-2 worker x multiple residential buildings fit." % (
            business_sizes[idx_sngl_wrk_multbld_fit].sum(), idx_sngl_wrk_multbld_fit.size))
               
        # 3. 1-2 worker in single non-res building (not mixed-use)
        idx_sngl_wrk_single_nonres_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 3))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_single_nonres_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_single_nonres_fit].repeat(business_sizes[idx_sngl_wrk_single_nonres_fit])
        job_assignment_case[jidx] = 3
        processed_bindicator[idx_sngl_wrk_single_nonres_fit] = True
        logger.log_status("3. %s jobs could be placed due to 1-2 worker x single non-res building fit." % idx_sngl_wrk_single_nonres_fit.size)        
        
        # 4. 1-2 worker in multiple non-res building (not mixed-use)
        idx_sngl_wrk_mult_nonres_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 4))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_mult_nonres_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_mult_nonres_fit].repeat(business_sizes[idx_sngl_wrk_mult_nonres_fit])
        job_assignment_case[jidx] = 4
        processed_bindicator[idx_sngl_wrk_mult_nonres_fit] = True
        logger.log_status("4. %s jobs could be placed due to 1-2 worker x multiple non-res building fit." % idx_sngl_wrk_mult_nonres_fit.size)        
                
        # 5. 1-2 worker in single mixed-use building
        idx_sngl_wrk_smu_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 5))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_smu_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_smu_fit].repeat(business_sizes[idx_sngl_wrk_smu_fit])
        job_assignment_case[jidx] = 5
        processed_bindicator[idx_sngl_wrk_smu_fit] = True
        logger.log_status("5. %s jobs in 1-2 worker x single mixed-use building." % idx_sngl_wrk_smu_fit.size)          
        
        # 6. 1-2 worker in multiple mixed-type buildings
        idx_sngl_wrk_mmu_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 6))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_mmu_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_mmu_fit].repeat(business_sizes[idx_sngl_wrk_mmu_fit])
        bldtype = buildings.get_attribute_by_id("building_type_id", business_location1wrkpl[idx_sngl_wrk_mmu_fit])
        is_bldtype_res = in1d(bldtype, restypes)
        home_based[in1d(job_array_labels, business_ids[idx_sngl_wrk_mmu_fit][where(is_bldtype_res)])] = True
        job_assignment_case[jidx] = 6
        processed_bindicator[idx_sngl_wrk_mmu_fit] = True
        logger.log_status("6. %s jobs in 1-2 worker x multiple mixed-type buildings. %s jobs classified as home-based." % (idx_sngl_wrk_mmu_fit.size, is_bldtype_res.sum()))            

        # 7. 1-2 worker business in residential parcel with no building
        idx_sngl_wrk_vacant_res = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 7))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_vacant_res])
        job_assignment_case[jidx] = 7
        home_based[jidx] = True
        processed_bindicator[idx_sngl_wrk_vacant_res] = True
        logger.log_status("7. %s jobs (%s businesses of size 1-2) could not be placed due to non-existing buildings in parcels with residential LU type." % (
            business_sizes[idx_sngl_wrk_vacant_res].sum(), idx_sngl_wrk_vacant_res.size))        

        # 9. 3+ workers in single residential building. Make two of them home based.
        idx_sngl_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 2), business_codes == 1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_fit].repeat(business_sizes[idx_sngl_wrk_fit])
        bsizeminus2 = vstack((2*ones(idx_sngl_wrk_fit.size), business_sizes[idx_sngl_wrk_fit]-2)).ravel("F").astype("int32") # interweaving 2 and remaining business size
        hbidx = tile(array([True, False]), bsizeminus2.size/2).repeat(bsizeminus2) # set the first two jobs of every business to True, others to False
        home_based[(where(jidx)[0])[hbidx]] = True
        job_assignment_case[jidx] = 9
        processed_bindicator[idx_sngl_wrk_fit] = True        
        logger.log_status("9. %s jobs (%s businesses) in 3+ worker x single residential building. %s jobs assigned as home-based." % (
            business_sizes[idx_sngl_wrk_fit].sum(), idx_sngl_wrk_fit.size, hbidx.sum()))
        
        # 10. 3+ workers in multiple residential buildings. Make two of them home based.
        idx_sngl_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 2), business_codes == 2))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_fit])
        job_assignment_case[jidx] = 10
        processed_bindicator[idx_sngl_wrk_fit] = True
        # sample buildings to businesses by parcels 
        bpcls = unique(businesses["parcel_id"][idx_sngl_wrk_fit])
        for ipcl in range(bpcls.size):
            bidx = where(buildings['parcel_id'] == bpcls[ipcl])[0]
            bldgids = buildings['building_id'][bidx]
            bussids = business_ids[businesses["parcel_id"] == bpcls[ipcl]]
            # multiply by units for sampling prop. to units rather than buildings
            bldgids = bldgids.repeat(maximum(1, buildings['residential_units'][bidx].astype('int32'))) 
            if bldgids.size < bussids.size:
                bldarray = bldgids.repeat(1+ceil((bussids.size - bldgids.size)/float(bldgids.size)) )
            else:
                bldarray = bldgids
            shuffle(bldarray) # randomly reorder in-place
            for ib in range(bussids.size):
                jidx = where(job_array_labels == bussids[ib])[0]
                job_building_id[jidx] = bldarray[ib]
                home_based[jidx[0:2]] = True
        logger.log_status("10. %s jobs (%s businesses) in 3+ worker x multiple residential building. %s jobs assigned as home-based." % (
            business_sizes[idx_sngl_wrk_fit].sum(), idx_sngl_wrk_fit.size, idx_sngl_wrk_fit.size*2))        


        # 11. single workplace, 3+ workers in single non-res or mixed-use building (11.)
        idx_sngl_wrkplace_2plus_workers = where(logical_and(logical_and(logical_and(processed_bindicator==0, business_sizes > 2), 
                                                            logical_or(business_codes==3, business_codes==5)),
                                                business_nworkplaces==1))[0]
        which_labels = where(in1d(job_array_labels, business_ids[idx_sngl_wrkplace_2plus_workers]))[0]
        job_building_id[which_labels] = business_location1wrkpl[idx_sngl_wrkplace_2plus_workers].repeat(business_sizes[idx_sngl_wrkplace_2plus_workers])   
        job_assignment_case[which_labels] = 11
        processed_bindicator[idx_sngl_wrkplace_2plus_workers] = True
        logger.log_status("11. %s jobs (%s businesses) could be placed due to single workplace x 3+ workers x single non-res/mixed-use building fit." % (
            business_sizes[idx_sngl_wrkplace_2plus_workers].sum(), idx_sngl_wrkplace_2plus_workers.size))
        
        # 12. single workplace, 3+ workers in multiple mixed-type building
        idx_sngl_wrkplace_2plus_workers = where(logical_and(logical_and(logical_and(processed_bindicator==0, business_sizes > 2),
                                                                        logical_or(business_codes==4, business_codes==6)),
                                                            business_nworkplaces==1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrkplace_2plus_workers])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrkplace_2plus_workers].repeat(business_sizes[idx_sngl_wrkplace_2plus_workers])    
        job_assignment_case[jidx] = 12
        processed_bindicator[idx_sngl_wrkplace_2plus_workers] = True
        logger.log_status("12. %s jobs (%s businesses) could be placed due to single workplace x 3+ workers x multiple non-res/mixed building fit." % (
            business_sizes[idx_sngl_wrkplace_2plus_workers].sum(), idx_sngl_wrkplace_2plus_workers.size))

        # 13. multiple workplaces, 3+ workers in single non-res or mixed building
        idx_mult_wrkplace_2plus_workers = where(logical_and(logical_and(logical_and(processed_bindicator==0, business_sizes > 2),
                                                                        logical_or(business_codes==3, business_codes==5)),
                                                            business_nworkplaces > 1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_mult_wrkplace_2plus_workers])
        job_building_id[jidx] = business_location1wrkpl[idx_mult_wrkplace_2plus_workers].repeat(business_sizes[idx_mult_wrkplace_2plus_workers])
        job_assignment_case[jidx] = 13
        processed_bindicator[idx_mult_wrkplace_2plus_workers] = True
        logger.log_status("13. %s jobs (%s businesses) could be placed due to multiple workplaces x 3+ workers x single non-res/mixed building fit." % (
            business_sizes[idx_mult_wrkplace_2plus_workers].sum(), idx_mult_wrkplace_2plus_workers.size))
        
        # 14. multiple workplaces, 3+ workers in multiple non-res or mixed building
        idx_mult_wrkplace_2plus_workers = where(logical_and(logical_and(logical_and(processed_bindicator==0, business_sizes > 2),
                                                                        logical_or(business_codes==4, business_codes==6)),
                                                            business_nworkplaces > 1))[0]
        processed_bindicator[idx_mult_wrkplace_2plus_workers] = True
        # sample buildings to businesses by parcels 
        bpcls = unique(businesses["parcel_id"][idx_mult_wrkplace_2plus_workers])
        hbasedsum = home_based.sum()
        for ipcl in range(bpcls.size):
            bldgids = buildings['building_id'][buildings['parcel_id'] == bpcls[ipcl]]
            bussids = business_ids[businesses["parcel_id"] == bpcls[ipcl]]
            if bldgids.size < bussids.size:
                bldarray = bldgids.repeat(1+ceil((bussids.size - bldgids.size)/float(bldgids.size)))
            else:
                bldarray = bldgids
            shuffle(bldarray) # randomly reorder in-place
            is_res = in1d(bldarray, restypes)
            for ib in range(bussids.size):
                jidx = where(job_array_labels == bussids[ib])
                job_building_id[jidx] = bldarray[ib]   
                home_based[jidx] = is_res
                job_assignment_case[jidx] = 14
        logger.log_status("14. %s jobs (%s businesses) could be placed due to multiple workplaces x 3+ workers x multiple non-res/mixed building fit. Classify %s jobs as home-based." % (
            business_sizes[idx_mult_wrkplace_2plus_workers].sum(), idx_mult_wrkplace_2plus_workers.size, home_based.sum()-hbasedsum))
        
        # 15. 3+ workers in residential parcel with no building
        idx_wrk_vacant_res = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 2), business_codes == 7))[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_vacant_res])
        job_assignment_case[jidx] = 15
        processed_bindicator[idx_wrk_vacant_res] = True
        logger.log_status("15. %s jobs (%s businesses of 2+ workers) could not be placed due to non-existing buildings in parcels with residential LU type." % (
            business_sizes[idx_wrk_vacant_res].sum(), idx_wrk_vacant_res.size))
        
        # 16. nonresidential parcel with no building
        idx_any_workers = where(processed_bindicator==0)[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_any_workers]) 
        idx_wrk_vacant_nonres = where(bcode == 8)[0]
        jidx = in1d(job_array_labels, business_ids[idx_any_workers[idx_wrk_vacant_nonres]])
        job_assignment_case[jidx] = 16
        processed_bindicator[idx_any_workers[idx_wrk_vacant_nonres]] = True
        logger.log_status("16. %s jobs (%s businesses) could not be placed due to non-existing buildings in parcels with rnon-esidential LU type." % (
            business_sizes[idx_any_workers[idx_wrk_vacant_nonres]].sum(), idx_wrk_vacant_nonres.size))        
        
        
        
        # jobs in messy buildings
        idx_worker = where(logical_and(processed_bindicator==0, business_sizes > 0))[0]
        bcode = parcels.get_attribute_by_id("buildings_code", businesses["parcel_id"][idx_worker])
        idx_messy_fit = where(bcode == 0)[0]
        processed_bindicator[idx_worker[idx_messy_fit]] = True
        logger.log_status("%s jobs (%s businesses) could not be placed due to messy buildings." % (
            business_sizes[idx_worker[idx_messy_fit]].sum(), idx_messy_fit.size))         

        
        logger.log_status("So far %s (%s percent) home-based jobs." % (home_based.sum(), round(home_based.sum()/(home_based.size/100.),2)))
        logger.log_status("So far %s percent (%s) jobs (%s businesses) processed. %s jobs (%s businesses) remain to be processed." % \
                          (round(business_sizes[processed_bindicator].sum()/(home_based.size/100.),2),
                           business_sizes[processed_bindicator].sum(), processed_bindicator.sum(),
                          business_sizes[logical_not(processed_bindicator)].sum(), business_sizes[logical_not(processed_bindicator)].size))
        
        # create job dataset
        job_data = {"job_id": arange(job_building_id.size)+1,
                    "home_based" : home_based,
                    "building_id": job_building_id,
                    "business_id": job_array_labels,
                    "sector_id": zeros(job_building_id.size),
                    "parcel_id": zeros(job_building_id.size),
                    "assignment_case": job_assignment_case}
        
        for ib in range(businesses.size()):
            idx = where(job_data['business_id'] == business_ids[ib])
            job_data["sector_id"][idx] = businesses['sector_id'][ib]
            job_data["parcel_id"][idx] = businesses['parcel_id'][ib]

        dictstorage = StorageFactory().get_storage('dict_storage')
        dictstorage.write_table(table_name="jobs", table_data=job_data)        
        return Dataset(in_storage=dictstorage, in_table_name="jobs", dataset_name="job", id_name="job_id")
    
if __name__ == '__main__':
    """
    The function takes a business table where businesses are assigned to parcels
    and converts it to jobs table where jobs are assigned to buildings. 
    It also classifies jobs as home-based or non-home-based.
    The input_cache below needs the following tables:
       buildings, building_types, parcels, business (name configurable below)
       The resultng jobs table is written into the output_cache.
       If write_to_csv, the jobs table is also converted into a csv file and 
       written into the output_cache.
    """
    business_dataset_name = "workplaces"
    input_cache = "/Users/hana/workspace/data/psrc_parcel/job_data/qcew_data/2014"
    output_cache = "/Users/hana/workspace/data/psrc_parcel/job_data/qcew_data/2014out"
    write_to_csv = True
    instorage = FltStorage().get(input_cache)
    jobs = CreateJobsFromQCEW().run(instorage, business_dsname=business_dataset_name)
    outstorage = FltStorage().get(output_cache)
    jobs.write_dataset(out_storage=outstorage, out_table_name="jobs")
    if write_to_csv:
        csv_storage = StorageFactory().get_storage('csv_storage', storage_location = output_cache)
        data = {}
        for attr in jobs.get_primary_attribute_names():
            data[attr] = jobs[attr]
        csv_storage.write_table(table_name="jobs", table_data=data, append_type_info=False)
