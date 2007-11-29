#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from numpy import arange, zeros, logical_and, where, logical_not, logical_or, array
from opus_core.logger import logger
from opus_core.misc import clip_to_zero_if_needed
from opus_core.simulation_state import SimulationState
from urbansim_parcel.models.development_project_proposal_sampling_model import DevelopmentProjectProposalSamplingModel
from opus_core.datasets.dataset import DatasetSubset

class DevelopmentProposalSamplingModelByZones(DevelopmentProjectProposalSamplingModel):
        
    def run(self, zones, type=None, **kwargs):
        """If 'type' is None, the model runs for both, residential and non-residential space. Alternatively,
        it can be set to 'residential' or 'non_residential'.
        """
        self.type = {"residential": False,
                     "non_residential": False}
        if (type is None) or (type == 'residential'):
            self.type["residential"] = True
        if (type is None) or (type == 'non_residential'):
            self.type["non_residential"] = True
            
        zones.compute_variables(["existing_residential_units = zone.aggregate(building.residential_units, [parcel])",
                                 "existing_job_spaces = zone.aggregate(urbansim_parcel.building.total_non_home_based_job_space, [parcel])",
                                 ], dataset_pool=self.dataset_pool)

        if self.type["residential"]: 
            occupied_residential_units = zones.compute_variables(["zone.number_of_agents(household)",
                                     ], dataset_pool=self.dataset_pool)
            maxiter = 10
        if self.type["non_residential"]:    
            zones.compute_variables(["number_of_all_nhb_jobs = zone.aggregate(urbansim.job.is_building_type_non_home_based)",
                                     "number_of_placed_nhb_jobs = zone.aggregate(urbansim_parcel.building.number_of_non_home_based_jobs)"],
                                 dataset_pool=self.dataset_pool)
            
            occupied_building_sqft = zones.compute_variables(
                     ["zone.aggregate(urbansim_parcel.building.occupied_building_sqft_by_non_home_based_jobs)"
                                 ], dataset_pool=self.dataset_pool)
            existing_building_sqft = zones.compute_variables(
                     ["zone.aggregate(building.non_residential_sqft)"],
                         dataset_pool=self.dataset_pool)
            to_be_used_sqft = clip_to_zero_if_needed(existing_building_sqft - occupied_building_sqft, "Zonal Developer Model")
            to_be_placed_sqft = (zones.get_attribute("number_of_all_nhb_jobs") - 
                                 zones.get_attribute("number_of_placed_nhb_jobs")) * self.get_weighted_job_sqft()[zones.get_id_attribute()]
            maxiter = 1
        
        exisiting_residential_units = zones.get_attribute("existing_residential_units")
        existing_job_spaces = zones.get_attribute("existing_job_spaces")
        
        zone_ids_in_proposals = self.proposal_set.compute_variables("zone_id = development_project_proposal.disaggregate(parcel.zone_id)", 
                                                dataset_pool=self.dataset_pool)
        zone_ids = zones.get_id_attribute()
        # keep copy of the weights
        original_weight = self.weight.copy()
        # this is a hack: we want buildings to be built in 2000, but the simulation is running for different year
        #start_year = SimulationState().get_current_time() - 1
        start_year = 2000
        self.proposal_set.modify_attribute(name="start_year", data=array(self.proposal_set.size()*[start_year]))

        for zone_index in range(zone_ids.size):
            self.zone = zone_ids[zone_index]
            if self.type["residential"]: 
                self.existing_to_occupied_ratio_residential =  \
                            exisiting_residential_units[zone_index] / float(occupied_residential_units[zone_index])
            if self.type["non_residential"]:
                self.existing_to_occupied_ratio_non_residential =  \
                            to_be_used_sqft[zone_index] / float(to_be_placed_sqft[zone_index])
            
            
            status = self.proposal_set.get_attribute("status_id")
            where_zone = zone_ids_in_proposals == self.zone
            idx_zone = where(where_zone)[0]
            if (self.proposal_set.id_active in status[idx_zone]) or (self.proposal_set.id_refused in status[idx_zone]):
                continue # this zone was handled previously
            if idx_zone.size <= 0:
                logger.log_status("No proposals for zone %s" % self.zone)
                continue
            idx_out_zone_not_active_not_refused = where(logical_and(logical_and(status != self.proposal_set.id_active, 
                                                                               status != self.proposal_set.id_refused),
                                                                    logical_not(where_zone)))[0]
            status[idx_zone] = self.proposal_set.id_proposed
            status[idx_out_zone_not_active_not_refused] = self.proposal_set.id_not_available
            self.proposal_set.modify_attribute(name="status_id", data=status)
            self.weight[:] = original_weight[:]
            self.proposed_units_from_previous_iterations = {}
            
            logger.log_status("\nDPSM for zone %s" % self.zone)
            for iter in range(maxiter):
                self.weight[:] = original_weight[:]           
                DevelopmentProjectProposalSamplingModel.run(self, **kwargs)
                if (len(self.accepted_proposals)<=0) or self.vacancy_rate_met():
                    break
                
            status = self.proposal_set.get_attribute("status_id")
            where_not_active = where(status[idx_zone] != self.proposal_set.id_active)[0]
            status[idx_zone[where_not_active]] = self.proposal_set.id_refused
            self.proposal_set.modify_attribute(name="status_id", data=status)
            if ((zone_index+1) % 50) == 0: # flush every 50th zone 
                self.proposal_set.flush_dataset()
        return (self.proposal_set, [])
    
    def vacancy_rate_met(self):
        if self.type["non_residential"]: 
            return True
        # applies only to residential case
        is_residential = self.current_target_vacancy.get_attribute("is_residential")
        type_ids = self.current_target_vacancy.get_attribute("building_type_id")
        avg_tv = 0.0
        existing = 0
        occupied = 0
        demolished = 0
        proposed = 0
        for index in arange(self.current_target_vacancy.size())[where(is_residential)]:
            type_id = type_ids[index]
            avg_tv += self.target_vacancies[type_id]
            existing += self.existing_units[type_id]
            occupied += self.occupied_units[type_id]
            demolished += self.demolished_units[type_id]
            proposed += self.proposed_units[type_id]
            if type_id not in self.proposed_units_from_previous_iterations.keys():
                self.proposed_units_from_previous_iterations[type_id] = 0
            self.proposed_units_from_previous_iterations[type_id] += self.proposed_units[type_id]
            
        avg_tv = avg_tv/float(is_residential.sum())
        units_stock = existing - demolished + proposed
        current_vr = (units_stock - occupied) / float(units_stock)
        if current_vr >= avg_tv:
            return True
        logger.log_status("Current overall vacancy rate: %s, average vacancy rate: %s" % (current_vr, avg_tv))
        self.existing_to_occupied_ratio_residential = units_stock / float(occupied)
        return False
        
        

    def compute_job_building_type_distribution(self):
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        alldata = self.dataset_pool.get_dataset('alldata')
        building_type_ids = building_type_dataset.get_id_attribute()
        alldata.compute_variables(map(lambda type: 
            "number_of_jobs_for_bt_%s = alldata.aggregate_all(urbansim_parcel.building.number_of_non_home_based_jobs * (building.building_type_id == %s))" % (type,type),
                building_type_ids) + 
              ["number_of_nhb_jobs = alldata.aggregate_all(urbansim_parcel.building.number_of_non_home_based_jobs)"], 
                                  dataset_pool=self.dataset_pool)
        job_building_type_distribution = zeros(building_type_ids.size)
        for itype in range(building_type_ids.size):
            job_building_type_distribution[itype] = alldata.get_attribute(
              'number_of_jobs_for_bt_%s' % building_type_ids[itype])[0]/float(alldata.get_attribute('number_of_nhb_jobs')[0])
        return job_building_type_distribution
        
    def create_zone_bt_sqft_table(self):
        zone_average_dataset = self.dataset_pool.get_dataset("building_sqft_per_job")
        zone_ids_in_zad = zone_average_dataset.get_attribute("zone_id").astype("int32")
        bt_in_zad = zone_average_dataset.get_attribute("building_type_id")
        sqft_in_zad = zone_average_dataset.get_attribute("building_sqft_per_job")
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        building_type_ids = building_type_dataset.get_id_attribute()
        zone_bt_lookup = zeros((zone_ids_in_zad.max()+1, building_type_ids.max()+1)) 
        for i in range(zone_average_dataset.size()):
            zone_bt_lookup[zone_ids_in_zad[i], bt_in_zad[i]] = sqft_in_zad[i]
        return zone_bt_lookup
        
    def get_weighted_job_sqft(self):
        job_building_type_distribution = self.compute_job_building_type_distribution()
        sqft_lookup = self.create_zone_bt_sqft_table()
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        building_type_ids = building_type_dataset.get_id_attribute()
        return (sqft_lookup[:,building_type_ids] * job_building_type_distribution).sum(axis=1)
        
    def check_vacancy_rates(self, target_vacancy):
        self.current_target_vacancy = target_vacancy
        type_ids = target_vacancy.get_attribute("building_type_id")
        is_residential = target_vacancy.get_attribute("is_residential")
        buildings = self.dataset_pool.get_dataset("building")
        building_type_ids = buildings.get_attribute("building_type_id")
        building_zone_ids = buildings.get_attribute("zone_id")
        for index in arange(target_vacancy.size()):
            ##TODO allow target vacancies to vary across zones/sub region geographies
            #zone_id = target_vacancy.get_attribute_by_index("zone_id", index)
            #if zone_id != self.zone: continue
            type_id = type_ids[index]
            target = self.target_vacancies[type_id]
            is_matched_type = building_type_ids == type_id
            if is_residential[index]:
                unit_name = self.variables_for_computing_vacancies["residential"]
            else:
                unit_name = self.variables_for_computing_vacancies["non_residential"]
            is_in_right_zone = building_zone_ids == self.zone 
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            self.existing_units[type_id] = buildings.get_attribute(unit_name)[is_matched_type*is_in_right_zone].astype("float32").sum()
            self.existing_units[type_id] += self.proposed_units_from_previous_iterations.get(type_id, 0)
            self.occupied_units[type_id] = 0
            if self.existing_units[type_id] == 0:
                vr = 0
            else:
                if unit_name == "residential_units":
                    if self.type["residential"]:
                        self.occupied_units[type_id] = int(self.existing_units[type_id]/self.existing_to_occupied_ratio_residential)
                    vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(self.existing_units[type_id])
                else:
                    if self.type["non_residential"]:
                        already_occupied = buildings.get_attribute("occupied_building_sqft_by_non_home_based_jobs")[is_matched_type*is_in_right_zone].sum()
                        remaining_existing_units = clip_to_zero_if_needed(self.existing_units[type_id] - already_occupied)
                        self.occupied_units[type_id] = int(remaining_existing_units/self.existing_to_occupied_ratio_non_residential)
                        vr = (self.existing_units[type_id] - (self.occupied_units[type_id]+already_occupied)) / float(self.existing_units[type_id])
                        self.existing_units[type_id] = remaining_existing_units
                    else:
                        vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(self.existing_units[type_id])
                    
            if vr < target:
                self.accepting_proposals[type_id] = True

                