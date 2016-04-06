import os
from numpy import cumsum, zeros, where, in1d, logical_and, logical_not, logical_or, ones, arange, unique, maximum, vstack, array, tile, concatenate, minimum, intersect1d
from numpy.random import shuffle, seed
from opus_core.ndimage import maximum as ndmax
from opus_core.ndimage import sum as ndsum
from math import ceil
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.variables.attribute_type import AttributeType
from opus_core.datasets.dataset import DatasetSubset, Dataset
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.logger import logger

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
def sector2building_type(sectors):
    transl = {
    1: 8, #      Natural resources and mining    TO   industrial
    2: 8,  #      Construction    TO      industrial
    3: 8,  #       Aerospace      TO       industrial
    4: 8,  #      Other durable goods     TO       industrial
    5:21,  #      Nondurable goods        TO       warehousing
    6:21,  #       Wholesale trade TO       warehousing
    7: 3,  #     Retail trade    TO       commercial
    8: 21, #      Transportation and warehousing  TO      warehousing
    9: 13, #      Utilities       TO      office
    10:13, #      Telecommunications      TO      office
    11:13, #      Other information       TO      office
    12:13, #      Financial activities    TO      office
    13:13, #      Professional and business services      TO      office
    14: 3, #      Food services and drinking places       TO       commercial
    15:13, #      Educational services    TO      office
    16:13, #      Health services TO       office
    17: 3, #      Other services  TO      commercial
    18: 5, #      Government      TO government         
    19:18  #      Education    TO School
    }
    trans_array = zeros(max(transl.keys())+1, dtype='int32')
    for sector, bt in transl.iteritems():
        trans_array[sector] = bt
    return trans_array[sectors]
    
class CreateJobsFromQCEW:
    number_of_jobs_attr = "job_count"
    
    def run(self, in_storage, out_storage=None, business_dsname="business", zone_dsname=None):
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
        logger.log_status("3. %s jobs (%s businesses) placed due to 1-2 worker x single non-res building fit." % (
                          business_sizes[idx_sngl_wrk_single_nonres_fit].sum(), idx_sngl_wrk_single_nonres_fit.size))     
        
        # 4. 1-2 worker in multiple non-res building (not mixed-use)
        idx_sngl_wrk_mult_nonres_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 4))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_mult_nonres_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_mult_nonres_fit].repeat(business_sizes[idx_sngl_wrk_mult_nonres_fit])
        job_assignment_case[jidx] = 4
        processed_bindicator[idx_sngl_wrk_mult_nonres_fit] = True
        logger.log_status("4. %s jobs (%s businesses) placed due to 1-2 worker x multiple non-res building fit." % (
            business_sizes[idx_sngl_wrk_mult_nonres_fit].sum(), idx_sngl_wrk_mult_nonres_fit.size))      
                
        # 5. 1-2 worker in single mixed-use building
        idx_sngl_wrk_smu_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 5))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_smu_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_smu_fit].repeat(business_sizes[idx_sngl_wrk_smu_fit])
        job_assignment_case[jidx] = 5
        processed_bindicator[idx_sngl_wrk_smu_fit] = True
        logger.log_status("5. %s jobs (%s businesses) in 1-2 worker x single mixed-use building." % (
            business_sizes[idx_sngl_wrk_smu_fit].sum(), idx_sngl_wrk_smu_fit.size))       
        
        # 6. 1-2 worker in multiple mixed-type buildings
        idx_sngl_wrk_mmu_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 6))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_mmu_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_mmu_fit].repeat(business_sizes[idx_sngl_wrk_mmu_fit])
        bldtype = buildings.get_attribute_by_id("building_type_id", business_location1wrkpl[idx_sngl_wrk_mmu_fit])
        is_bldtype_res = in1d(bldtype, restypes)
        home_based[in1d(job_array_labels, business_ids[idx_sngl_wrk_mmu_fit][where(is_bldtype_res)])] = True
        job_assignment_case[jidx] = 6
        processed_bindicator[idx_sngl_wrk_mmu_fit] = True
        logger.log_status("6. %s jobs (%s businesses) in 1-2 worker x multiple mixed-type buildings. %s jobs classified as home-based." % (
            business_sizes[idx_sngl_wrk_mmu_fit].sum(), idx_sngl_wrk_mmu_fit.size, business_sizes[idx_sngl_wrk_mmu_fit][where(is_bldtype_res)].sum()))            

        # 7. 1-2 worker business in residential parcel with no building
        idx_sngl_wrk_vacant_res = where(logical_and(logical_and(processed_bindicator==0, business_sizes < 3), business_codes == 7))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_vacant_res])
        job_assignment_case[jidx] = 7
        home_based[jidx] = True
        processed_bindicator[idx_sngl_wrk_vacant_res] = True
        logger.log_status("7. %s jobs (%s businesses of size 1-2) could not be placed due to non-existing buildings in parcels with residential LU type." % (
            business_sizes[idx_sngl_wrk_vacant_res].sum(), idx_sngl_wrk_vacant_res.size))        

        # 8. 3+ workers of governmental workplaces in 1+ residential building
        ind_bussiness_case8 = logical_and(logical_and(processed_bindicator==0, logical_and(business_sizes > 2, in1d(businesses['sector_id'], [18,19]))), in1d(business_codes, [1,2]))
        idx_wrk_fit = where(ind_bussiness_case8)[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_fit])
        job_assignment_case[jidx] = 8
        processed_bindicator[idx_wrk_fit] = True
        logger.log_status("8. %s governmental jobs (%s businesses of size 3+) could not be placed due to residing in residential buildings only." % (
                    business_sizes[idx_wrk_fit].sum(), idx_wrk_fit.size))
        
        # 9. 3-30 workers in single residential building. Make two of them home based.
        idx_sngl_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, logical_and(business_sizes > 2, business_sizes <= 30)), business_codes == 1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_fit])
        job_building_id[jidx] = business_location1wrkpl[idx_sngl_wrk_fit].repeat(business_sizes[idx_sngl_wrk_fit])
        bsizeminus2 = vstack((2*ones(idx_sngl_wrk_fit.size), business_sizes[idx_sngl_wrk_fit]-2)).ravel("F").astype("int32") # interweaving 2 and remaining business size
        hbidx = tile(array([True, False]), bsizeminus2.size/2).repeat(bsizeminus2) # set the first two jobs of every business to True, others to False
        home_based[(where(jidx)[0])[hbidx]] = True
        job_assignment_case[jidx] = 9
        processed_bindicator[idx_sngl_wrk_fit] = True        
        logger.log_status("9. %s jobs (%s businesses) in 3-30 worker x single residential building. %s jobs assigned as home-based." % (
            business_sizes[idx_sngl_wrk_fit].sum(), idx_sngl_wrk_fit.size, hbidx.sum()))      
        
        # 10. 3-30 workers in multiple residential buildings. Make two of them home based.
        idx_sngl_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, logical_and(business_sizes > 2, business_sizes <= 30)), business_codes == 2))[0]
        jidx = in1d(job_array_labels, business_ids[idx_sngl_wrk_fit])
        job_assignment_case[jidx] = 10
        processed_bindicator[idx_sngl_wrk_fit] = True
        # sample buildings to businesses by parcels 
        bpcls = unique(businesses["parcel_id"][idx_sngl_wrk_fit])
        for ipcl in range(bpcls.size):
            bidx = where(buildings['parcel_id'] == bpcls[ipcl])[0]
            bldgids = buildings['building_id'][bidx]
            bussids = intersect1d(business_ids[businesses["parcel_id"] == bpcls[ipcl]], business_ids[idx_sngl_wrk_fit])
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
        logger.log_status("10. %s jobs (%s businesses) in 3-30 worker x multiple residential building. %s jobs assigned as home-based." % (
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
        #hbasedsum = home_based.sum()
        for ipcl in range(bpcls.size):
            bldgids = buildings['building_id'][buildings['parcel_id'] == bpcls[ipcl]]
            bussids = intersect1d(business_ids[businesses["parcel_id"] == bpcls[ipcl]], business_ids[idx_mult_wrkplace_2plus_workers])
            if bldgids.size < bussids.size:
                bldarray = bldgids.repeat(1+ceil((bussids.size - bldgids.size)/float(bldgids.size)))
            else:
                bldarray = bldgids
            shuffle(bldarray) # randomly reorder in-place
            is_res = in1d(bldarray, restypes)
            for ib in range(bussids.size):
                jidx = where(job_array_labels == bussids[ib])
                job_building_id[jidx] = bldarray[ib]
                #home_based[jidx] = is_res
                job_assignment_case[jidx] = 14
        logger.log_status("14. %s jobs (%s businesses) could be placed due to multiple workplaces x 3+ workers x multiple non-res/mixed building fit." % (
            business_sizes[idx_mult_wrkplace_2plus_workers].sum(), idx_mult_wrkplace_2plus_workers.size))
        
        
        # 15. 3+ workers in residential parcel with no building
        idx_wrk_vacant_res = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 2), business_codes == 7))[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_vacant_res])
        job_assignment_case[jidx] = 15
        processed_bindicator[idx_wrk_vacant_res] = True
        logger.log_status("15. %s jobs (%s businesses of 3+ workers) could not be placed due to non-existing buildings in parcels with residential LU type." % (
            business_sizes[idx_wrk_vacant_res].sum(), idx_wrk_vacant_res.size))
        
        # 16. nonresidential parcel with no building
        idx_wrk_vacant_nonres = where(logical_and(processed_bindicator==0, business_codes == 8))[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_vacant_nonres])
        job_assignment_case[jidx] = 16
        processed_bindicator[idx_wrk_vacant_nonres] = True
        logger.log_status("16. %s jobs (%s businesses) could not be placed due to non-existing buildings in parcels with non-esidential LU type." % (
            business_sizes[idx_wrk_vacant_nonres].sum(), idx_wrk_vacant_nonres.size))        
        
        # 17. 31+ workers in single residential building. Do not place - will go into ELCM.
        idx_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 30), business_codes == 1))[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_fit])
        job_assignment_case[jidx] = 17
        processed_bindicator[idx_wrk_fit] = True        
        logger.log_status("17. %s jobs (%s businesses) in 31+ workers x single residential building." % (
            business_sizes[idx_wrk_fit].sum(), idx_wrk_fit.size))         
    
        # 18. 31+ workers in multiple residential buildings.
        idx_wrk_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 30), business_codes == 2))[0]
        jidx = in1d(job_array_labels, business_ids[idx_wrk_fit])
        job_assignment_case[jidx] = 18
        processed_bindicator[idx_wrk_fit] = True
        logger.log_status("18. %s jobs (%s businesses) in 31+ workers x multiple residential building." % (
            business_sizes[idx_wrk_fit].sum(), idx_wrk_fit.size))                

        # jobs in messy buildings
        idx_messy_fit = where(logical_and(logical_and(processed_bindicator==0, business_sizes > 0), business_codes == 0))[0]
        processed_bindicator[idx_messy_fit] = True
        logger.log_status("%s jobs (%s businesses) could not be placed due to messy buildings." % (
            business_sizes[idx_messy_fit].sum(), idx_messy_fit.size))         
         
        # build new buildings for jobs in cases 7, 8, 15 and 16
        jidx_no_bld = where(in1d(job_assignment_case, [7,8,15,16]))[0]
        bus = unique(job_array_labels[jidx_no_bld])
        bsidx = businesses.get_id_index(bus)
        # first create buildings for single workplaces per parcel
        single_workplace_idx = where(business_nworkplaces[bsidx] == 1)[0]
        newbld_parcel_id = businesses['parcel_id'][bsidx][single_workplace_idx]
        newbld_bt = sector2building_type(businesses['sector_id'][bsidx][single_workplace_idx])
        newbids = arange(buildings.get_id_attribute().max()+1, buildings.get_id_attribute().max()+single_workplace_idx.size+1)
        bbldid = zeros(bsidx.size, dtype='int32')
        bbldid[single_workplace_idx] = newbids
        # for parcels with multiple workplaces select the largest business to determine its building type
        mult_bsidx = bsidx[where(business_nworkplaces[bsidx] > 1)[0]]
        empty_parcels = businesses['parcel_id'][mult_bsidx]
        uempty_parcels = unique(empty_parcels)
        bsize_on_empty_pcl = ndmax(business_sizes[mult_bsidx], labels=empty_parcels, index=uempty_parcels)
        newbld2_sec = zeros(uempty_parcels.size, dtype='int32')
        newbids2 = arange(newbids.max()+1, newbids.max()+uempty_parcels.size+1)
        for ipcl in range(uempty_parcels.size):
            newbld2_sec[ipcl] = businesses['sector_id'][mult_bsidx][logical_and(businesses['parcel_id'][mult_bsidx] == uempty_parcels[ipcl], 
                                                                                business_sizes[mult_bsidx]==bsize_on_empty_pcl[ipcl])][0]
            this_bidx = where(businesses['parcel_id'][bsidx] == uempty_parcels[ipcl])
            bbldid[this_bidx] = newbids2[ipcl]
            
        newbld_parcel_id = concatenate((newbld_parcel_id, uempty_parcels))
        newbld_bt = concatenate((newbld_bt, sector2building_type(newbld2_sec)))    
        
        newbldgs = {'building_id': concatenate((newbids, newbids2)),
                    'parcel_id': newbld_parcel_id,
                    'building_type_id': newbld_bt,
                    }
        buildings.add_elements(newbldgs, require_all_attributes=False)
        jidx = where(in1d(job_array_labels, business_ids[bsidx]))[0]
        job_building_id[jidx] = bbldid.repeat(business_sizes[bsidx])
        logger.log_status("Build %s new buildings to accommodate %s jobs (out of which %s are governmental) from cases 7, 15, 16." % (
            newbld_parcel_id.size, jidx.size, business_sizes[bsidx][where(in1d(businesses['sector_id'][bsidx], [18,19]))].sum()))
        
        
        logger.log_status("Assigned %s (%s percent) home-based jobs." % (home_based.sum(), round(home_based.sum()/(home_based.size/100.),2)))
        logger.log_status("Finished %s percent (%s) jobs (%s businesses) processed. %s jobs (%s businesses) remain to be processed." % \
                          (round(business_sizes[processed_bindicator].sum()/(home_based.size/100.),2),
                           business_sizes[processed_bindicator].sum(), processed_bindicator.sum(),
                          business_sizes[logical_not(processed_bindicator)].sum(), business_sizes[logical_not(processed_bindicator)].size))
        
        logger.start_block("Storing jobs data.")
        # create job dataset
        job_data = {"job_id": (arange(job_building_id.size)+1).astype("int32"),
                    "home_based_status" : home_based,
                    "building_id": job_building_id,
                    "business_id": job_array_labels.astype("int32"),
                    "sector_id": businesses['sector_id'].repeat(business_sizes).astype("int32"), 
                    "parcel_id": businesses['parcel_id'].repeat(business_sizes).astype("int32"), 
                    "assignment_case": job_assignment_case}

        # join with zones
        if zone_dsname is not None:
            zones = dataset_pool.get_dataset(zone_dsname)
            idname = zones.get_id_name()[0]
            #jpcls = buildings.get_attribute_by_id('parcel_id', job_building_id)
            job_data[idname] = parcels.get_attribute_by_id(idname, job_data["parcel_id"])
            
            
        dictstorage = StorageFactory().get_storage('dict_storage')
        dictstorage.write_table(table_name="jobs", table_data=job_data)
        jobs = Dataset(in_storage=dictstorage, in_table_name="jobs", dataset_name="job", id_name="job_id")
        if out_storage is not None:
            jobs.write_dataset(out_storage=out_storage, out_table_name="jobs")
            buildings.write_dataset(out_storage=out_storage, attributes=AttributeType.PRIMARY)
        logger.end_block()        
        return jobs
 

class MatchHouseholdsToJobs:
    def run(self, jobs, in_storage, out_storage=None):
        dataset_pool = DatasetPool(storage=in_storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'] )
        if jobs is None:
            jobs =  dataset_pool.get_dataset('job')
        else:
            dataset_pool.replace_dataset('job', jobs)
        hhs = dataset_pool.get_dataset('household')
        buildings = dataset_pool.get_dataset('building')
        buildings.compute_variables(["psrc_parcel.building.census_block_group_id", "psrc_parcel.building.number_of_home_based_jobs",
                                     "urbansim_parcel.building.number_of_households", "urbansim_parcel.building.residential_units"
                                           ], 
                                          dataset_pool=dataset_pool)
        ubusiness, ubusiness_idx = unique(jobs['business_id']*(jobs['home_based_status']==1), return_index=True)
        jobs_ubusiness = zeros(jobs.size(), dtype='bool8')
        jobs_ubusiness[ubusiness_idx] = True
        jobs_ubusiness[jobs['home_based_status']==0] = False
        nhbbus = minimum(ndsum(jobs_ubusiness, labels=jobs['building_id'], index=buildings['building_id']), buildings["residential_units"])        
        affected_buildings_ind = logical_and((buildings["number_of_households"] - nhbbus) < 0, buildings["number_of_households"] < buildings["residential_units"])
        not_affected_buildings_ind = logical_and(logical_not(affected_buildings_ind), buildings["number_of_home_based_jobs"] == 0)
        blocks = unique(buildings["census_block_group_id"][where(affected_buildings_ind)])

        hh_building_id = hhs['building_id'].copy()
        seed(1)
        logger.log_status("%s buildings in %s census block affected for moving households to jobs." % (affected_buildings_ind.sum(), blocks.size))
        logger.start_block("Moving households to jobs")
        for block in blocks:
            bidx = where(logical_and(affected_buildings_ind, buildings["census_block_group_id"] == block))[0]
            bidx_out = where(logical_and(not_affected_buildings_ind, buildings["census_block_group_id"] == block))[0]
            if bidx_out.size == 0:
                continue
            hh_idx = where(in1d(hhs['building_id'], buildings['building_id'][bidx_out]))[0]
            if hh_idx.size == 0:
                continue
            nhh_needed = maximum(nhbbus[bidx] - buildings["number_of_households"][bidx], 0)
            if nhh_needed.sum() <= 0:
                continue
            for i in arange(bidx.size):
                if nhh_needed[i] == 0:
                    continue
                hh_idx_sampled = sample_noreplace(hh_idx, nhh_needed[i])
                hh_building_id[hh_idx_sampled] = buildings['building_id'][bidx[i]]
        logger.end_block() 
        if out_storage is not None:
            households.write_dataset(out_storage=out_storage, out_table_name="households")                  
        logger.log_status("%s households re-located." % (hh_building_id <> hhs['building_id']).sum())
    
if __name__ == '__main__':
    """
    The function takes a business table where businesses are assigned to parcels
    and converts it to jobs table where jobs are assigned to buildings. 
    It also classifies jobs as home-based or non-home-based. 
    If zones_dataset_name is given, the job dataset is joined with this higher level geography. 
    The input_cache below needs the following tables:
       buildings, building_types, parcels, business (name configurable below)
       The resultng jobs table is written into the output_cache.
       If write_to_csv, the jobs table is also converted into a csv file and 
       written into the output_cache.
    """
    business_dataset_name = "workplaces"
    zones_dataset_name = 'city' # only needed if a disaggregation of a higher level geography id is desired (e.g. for a later run of ELCM)
    # input_cache = "/Users/hana/workspace/data/psrc_parcel/job_data/qcew_data/2014"
    # output_cache = "/Users/hana/workspace/data/psrc_parcel/job_data/qcew_data/2014out"
    input_cache = "E:/opusgit/urbansim_data/data/psrc_parcel/job_data/qcew_data_elcm/base_year_data/2014"
    output_cache = "E:/opusgit/urbansim_data/data/psrc_parcel/job_data/qcew_data_elcm/base_year_data/2014out"
    create_jobs = True
    write_to_csv = False
    match_with_households = False
    instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    jobs = None
    if create_jobs:
        jobs = CreateJobsFromQCEW().run(instorage, out_storage=outstorage, business_dsname=business_dataset_name, zone_dsname=zones_dataset_name)    
        if write_to_csv:
            csv_storage = StorageFactory().get_storage('csv_storage', storage_location = output_cache)
            data = {}
            for attr in jobs.get_primary_attribute_names():
                data[attr] = jobs[attr]
            csv_storage.write_table(table_name="jobs", table_data=data, append_type_info=False)
        
    if match_with_households:
        MatchHouseholdsToJobs().run(jobs, instorage, out_storage=outstorage)

# write a subset of workplaces into a file
#cases = [7,15,16]
#ind = zeros(job_assignment_case.size, dtype='bool8')
#for c in cases:
    #ind = logical_or(ind, job_assignment_case == c)
#jidx = where(ind)[0]
#bus = unique(job_array_labels[jidx])
#bidx = businesses.get_id_index(bus)
##bidx2 = bidx[businesses['sector_id'][bidx]<18] # non-public
#bidx2 = bidx
#from numpy import concatenate, newaxis
#from opus_core.misc import write_table_to_text_file, write_to_text_file
#d = concatenate((businesses['workplaces_id'][bidx2,newaxis], businesses['parcel_id'][bidx2,newaxis], businesses['job_count'][bidx2,newaxis], businesses['sector_id'][bidx2,newaxis]), axis=1)
##filename = 'non_public_workplaces_on_empty_parcels.txt'
#filename = 'workplaces_on_empty_parcels.txt'
#write_to_text_file(filename, ['workplaces_id', 'parcel_id', 'job_count', 'sector_id'], delimiter="\t")
#write_table_to_text_file(filename, d, mode='a', delimiter="\t")
