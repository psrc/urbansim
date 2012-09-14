# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy
from numpy import ones, array, where, logical_and, around
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.datasets.control_total_dataset import ControlTotalDataset

class GovEdJobsModel(Model):
    """Executes experimental code.
    """
    model_name = "Zonal Gov-Ed Jobs Model"

    def run(self):
        """Runs the test model. 
        """

        dataset_pool = SessionConfiguration().get_dataset_pool()

        zone_set = dataset_pool.get_dataset('zone')

        zone_pop = zone_set.compute_variables('_zone_pop = zone.aggregate(household.persons,intermediates=[building,parcel])')

        local_gov_jobs = zone_set.compute_variables('_local_gov_jobs = zone._zone_pop * zone.disaggregate(zone_gov_ed_job.local_gov)')

        local_ed_k12_jobs = zone_set.compute_variables('_ed_k12 = zone._zone_pop * zone.disaggregate(zone_gov_ed_job.ed_k12)')

        county_gov_jobs = zone_set.compute_variables('_county_gov_jobs = zone.disaggregate(zone_gov_ed_job.disaggregate(county.aggregate(household.persons,intermediates=[building,parcel]))) * zone.disaggregate(zone_gov_ed_job.county_gov)')

        state_gov_jobs = zone_set.compute_variables('_state_gov_jobs = zone.disaggregate(alldata.aggregate_all(household.persons)) * zone.disaggregate(zone_gov_ed_job.state_gov)')

        fed_gov_jobs = zone_set.compute_variables('_fed_gov_jobs = zone.disaggregate(alldata.aggregate_all(household.persons)) * zone.disaggregate(zone_gov_ed_job.fed_gov)')

        ed_high_jobs = zone_set.compute_variables('_ed_high_jobs = zone.disaggregate(alldata.aggregate_all(household.persons)) * zone.disaggregate(zone_gov_ed_job.ed_high)')
        
        gov_jobs =  zone_set.compute_variables('_gov_jobs = _local_gov_jobs + _county_gov_jobs + _state_gov_jobs + _fed_gov_jobs')
        
        edu_jobs =  zone_set.compute_variables('_ed_jobs = _ed_k12 + _ed_high_jobs')
        
        current_year = SimulationState().get_current_time()
        base_year = '2010'
        base_cache_storage = AttributeCache().get_flt_storage_for_year(base_year)
        control_totals = ControlTotalDataset(in_storage=base_cache_storage, in_table_name="annual_business_control_totals")
        number_of_jobs = control_totals.get_attribute("total_number_of_jobs")
        
        idx_current_edother = where(logical_and(control_totals.get_attribute("year")==current_year,control_totals.get_attribute("sector_id")==618320))[0]
        jobs_current_edother = number_of_jobs[idx_current_edother].sum()
        
        idx_current_edhigh = where(logical_and(control_totals.get_attribute("year")==current_year,control_totals.get_attribute("sector_id")==618330))[0]
        jobs_current_edhigh = number_of_jobs[idx_current_edhigh].sum()
        
        idx_current_edk12 = where(logical_and(control_totals.get_attribute("year")==current_year,control_totals.get_attribute("sector_id")==618340))[0]
        jobs_current_edk12 = number_of_jobs[idx_current_edk12].sum()
        
        idx_current_gov = where(logical_and(control_totals.get_attribute("year")==current_year,control_totals.get_attribute("sector_id")==618319))[0]
        total_gov_jobs = number_of_jobs[idx_current_gov].sum()
        
        total_edu_jobs = jobs_current_edother + jobs_current_edhigh + jobs_current_edk12
        
        gov_scaling_ratio=total_gov_jobs*1.0/gov_jobs.sum()
        
        edu_scaling_ratio=total_edu_jobs*1.0/edu_jobs.sum()
        
        gov_jobs = around(gov_jobs*gov_scaling_ratio)
        
        edu_jobs = around(edu_jobs*edu_scaling_ratio)
        
        zone_set.add_primary_attribute(name='gov_jobs', data=gov_jobs)

        zone_set.add_primary_attribute(name='edu_jobs', data=edu_jobs)