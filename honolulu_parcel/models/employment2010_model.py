# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from numpy import arange, zeros, logical_and, where, array, unique, ones
from numpy.random import randint, shuffle
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration

class Employment2010Model(Model):
    """
    """
    model_name = "Allocating Zonal LEHD Job Totals Model"

    def run(self):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        job_set = dataset_pool.get_dataset('job')
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')
        job_set.add_primary_attribute(name='job_zone', data=job_set.compute_variables('job.disaggregate(parcel.zone_id,intermediates=[building])'))
        ##Non-home-based jobs by zone.  Allocate home-based jobs later (regionally, instead of by zone)
        job_controls = dataset_pool.get_dataset('jobs2010_to_allocate')

        #Remove all existing jobs
        all_jobs = job_set.compute_variables('_all_jobs = job.job_id > 0')
        idx_all_jobs = where(all_jobs)[0]
        job_set.remove_elements(idx_all_jobs)

        #For each zone, generate 2010 non-home-based jobs
        zone_ids = job_controls['zone_id']
        for zone_id in zone_ids:
            logger.log_status("ZONE: %s" % (zone_id) )
            building_set.delete_computed_attributes()
            job_set.delete_computed_attributes()
            parcel_set.delete_computed_attributes()
            index_zone = where(job_controls['zone_id']==zone_id)[0]
            for sector_id in arange(1, 20):
                sector_array_name = 'sector' + str(sector_id)
                employment = job_controls["%s"%(sector_array_name)][index_zone]
                logger.log_status("employment: %s" % (employment) )
                if employment > 0:
                    jobs_to_add = {}
                    jobs_to_add['job_zone'] = array(employment[0]*[zone_id])
                    jobs_to_add['sector_id'] = array(employment[0]*[sector_id])
                    jobs_to_add['building_id'] = array(employment[0]*[-1])
                    jobs_to_add['dpa_id'] = array(employment[0]*[-1])
                    jobs_to_add['home_based_status'] = zeros(employment[0], dtype="int32")
                    job_set.add_elements(data=jobs_to_add, require_all_attributes=False, change_ids_if_not_unique=True)

            #Place non-residential jobs within appropriate zone
            unplaced_jobs = job_set.compute_variables('_unplaced_jobs = job.building_id == -1')
            idx_unplaced_jobs = where(unplaced_jobs)[0]
            for job in idx_unplaced_jobs:
                available_job_capacity = building_set.compute_variables('_available_job_capacity = (building.disaggregate(parcel.zone_id) == %s) * ((building.non_residential_sqft/250.0)>building.number_of_agents(job))'%(zone_id))
                idx_available_job_capacity = where(available_job_capacity)[0]
                if idx_available_job_capacity.size < 1:
                    logger.log_status("No non-residential job capacity remaining in zone %s"%(zone_id))
                    building_in_zone = building_set.compute_variables('(building.disaggregate(parcel.zone_id)==%s)*(building.building_type_id>3)'%(zone_id))
                    idx_building = where(building_in_zone)[0]
                    if idx_building.size < 1:
                        building_in_zone = building_set.compute_variables('(building.disaggregate(parcel.zone_id)==%s)'%(zone_id))
                        idx_building = where(building_in_zone)[0]
                        if idx_building.size < 1:
                            logger.log_status("No buildings in zone %s, but jobs need to be placed.  Adding one 500sqft office."%(zone_id))
                            building_to_add = {}
                            building_to_add['building_type_id'] = array([8])
                            building_to_add['non_residential_sqft'] = array([500])
                            building_to_add['residential_units'] = array([0])
                            building_to_add['hotel_units'] = array([0])
                            building_to_add['resort_units'] = array([0])
                            building_to_add['stories'] = array([1])
                            building_to_add['total_building_sqft'] = array([500])
                            building_to_add['year_built'] = array([2010])
                            parcel_in_zone = parcel_set.compute_variables('_parcel_in_zone = (parcel.zone_id==%s)'%(zone_id))
                            idx_parcel = where(parcel_in_zone)[0]
                            parcel_ids_in_zone=(parcel_set.get_attribute('parcel_id'))[idx_parcel]
                            shuffle(parcel_ids_in_zone)
                            parcel_id_to_assign = parcel_ids_in_zone[:1]
                            building_to_add['parcel_id'] = parcel_id_to_assign
                            building_set.add_elements(data=building_to_add, require_all_attributes=False, change_ids_if_not_unique=True)
                            building_in_zone = building_set.compute_variables('(building.disaggregate(parcel.zone_id)==%s)'%(zone_id))
                            idx_building = where(building_in_zone)[0]
                    building_ids_in_zone=(building_set.get_attribute('building_id'))[idx_building]
                    shuffle(building_ids_in_zone)
                    building_id_to_assign = building_ids_in_zone[:1]
                    job_set.modify_attribute('building_id', building_id_to_assign, job)
                else:
                    building_ids_with_enough_capacity = (building_set.get_attribute('building_id'))[idx_available_job_capacity] 
                    shuffle(building_ids_with_enough_capacity)
                    building_id_to_assign = building_ids_with_enough_capacity[:1]
                    job_set.modify_attribute('building_id', building_id_to_assign, job)
        job_set.delete_one_attribute('job_zone')   

        home_based_job_controls = dataset_pool.get_dataset('jobs2010_home_based')
        for sector in arange(1,20):
            logger.log_status("Sector: %s"%(sector))
            idx_sector = where(home_based_job_controls['sector_id'] == sector)
            num_home_based_jobs = home_based_job_controls['home_based_jobs'][idx_sector]
            logger.log_status("num_home_based_jobs: %s"%(num_home_based_jobs))
            if num_home_based_jobs > 0:
                jobs_to_add = {}
                jobs_to_add['job_zone'] = array(num_home_based_jobs[0]*[-1])
                jobs_to_add['sector_id'] = array(num_home_based_jobs[0]*[sector])
                jobs_to_add['building_id'] = array(num_home_based_jobs[0]*[-1])
                jobs_to_add['dpa_id'] = array(num_home_based_jobs[0]*[-1])
                jobs_to_add['home_based_status'] = ones(num_home_based_jobs[0], dtype="int32")
                job_set.add_elements(data=jobs_to_add, require_all_attributes=False, change_ids_if_not_unique=True)
        unplaced_jobs = job_set.compute_variables('job.building_id == -1')
        idx_unplaced_jobs = where(unplaced_jobs)[0]
        for job in idx_unplaced_jobs:
            res_buildings_with_capacity = building_set.compute_variables('(building.number_of_agents(job)<building.residential_units)*(building.building_type_id<4)')
            idx_building = where(res_buildings_with_capacity)[0]
            building_ids = (building_set.get_attribute('building_id'))[idx_building]
            shuffle(building_ids)
            building_id_to_assign = building_ids[:1]
            job_set.modify_attribute('building_id', building_id_to_assign, job)

        job_dpa = job_set.compute_variables('job.disaggregate(parcel.dpa_id,intermediates=[building])')
        job_set.modify_attribute('dpa_id', job_dpa)
