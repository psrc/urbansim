# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, logical_not, logical_or, array, ones, isinf, round
from opus_core.logger import logger
from opus_core.misc import clip_to_zero_if_needed, unique
from opus_core.simulation_state import SimulationState
from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel
from opus_core.datasets.dataset import DatasetSubset

class DevelopmentProposalSamplingModelByZones(DevelopmentProjectProposalSamplingModel):
    max_zone = 938
    max_building_type = 22
        
    def run(self, zones, zone_ids_to_process=None, type=None, year=2000, **kwargs):
        """If 'type' is None, the model runs for both, residential and non-residential space. Alternatively,
        it can be set to 'residential' or 'non_residential'.
        """

        self.type = {"residential": False,
                     "non_residential": False}
        if (type is None) or (type == 'residential'):
            self.type["residential"] = True
        if (type is None) or (type == 'non_residential'):
            self.type["non_residential"] = True

        self.proposal_set.id_planned = 99999 # to switch processing of planned proposals of
        
        target_vacancies = self.dataset_pool.get_dataset('target_vacancy')
        tv_building_types = unique(target_vacancies.get_attribute('building_type_id'))
        
        bldgs = self.dataset_pool.get_dataset('building')
        bts = self.dataset_pool.get_dataset('building_type')
        all_building_types = bts.get_id_attribute()
        
        self.bt_do_not_count = array(map(lambda x: x not in tv_building_types, all_building_types))
        self.bt_do_not_count =  all_building_types[self.bt_do_not_count]
        self.do_not_count_residential_units  = self.get_do_not_count_residential_units(zones)
        
        zones.compute_variables(["placed_households = zone.aggregate(building.number_of_agents(household))",
                                 "occupied_spaces = zone.aggregate(psrc_parcel.building.occupied_spaces, [parcel])"
                                 ], dataset_pool=self.dataset_pool)
        bldgs.compute_variables(["urbansim_parcel.building.zone_id"], dataset_pool=self.dataset_pool)
        self.occuppied_estimate = {}
        if self.type["residential"]: 
            occupied_residential_units = zones.compute_variables(["total_number_of_households = zone.number_of_agents(household)",
                                     ], dataset_pool=self.dataset_pool) - self.do_not_count_residential_units
            to_be_placed_households = zones["total_number_of_households"] - zones["placed_households"]
            hhdistr = self.compute_household_building_type_distribution()
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count or not bts['is_residential'][ibt]:
                    continue
                self.occuppied_estimate[(bt,)] = zones.sum_over_ids(bldgs['zone_id'], 
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + round(hhdistr[ibt]*to_be_placed_households)
        if self.type["non_residential"]:    
            zones.compute_variables(["number_of_all_nhb_jobs = zone.aggregate(job.home_based_status==0)"],
                                 dataset_pool=self.dataset_pool)
            job_building_type_distribution = self.compute_job_building_type_distribution()
            to_be_placed_jobs = zones.get_attribute("number_of_all_nhb_jobs") - zones['occupied_spaces']                                
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count or bts['is_residential'][ibt]:
                    continue
                self.occuppied_estimate[(bt,)] = zones.sum_over_ids(bldgs['zone_id'], 
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + round(to_be_placed_jobs * job_building_type_distribution[ibt])
              
        self.is_residential_bt = {}
        for ibt in range(all_building_types.size):
            self.is_residential_bt[(all_building_types[ibt],)] = bts['is_residential'][ibt]
            
        zone_ids_in_proposals = self.proposal_set.compute_variables("zone_id = development_project_proposal.disaggregate(urbansim_parcel.parcel.zone_id)", 
                                                dataset_pool=self.dataset_pool)
        zone_ids = zones.get_id_attribute()
        # keep copy of the weights
        original_weight = self.weight.copy()
        # this is a hack: we want buildings to be built in 2000, but the simulation is running for different year
        #start_year = SimulationState().get_current_time() - 1
        start_year = year
        self.proposal_set.modify_attribute(name="start_year", data=array(self.proposal_set.size()*[start_year]))
        status = self.proposal_set.get_attribute("status_id")
        for zone_index in range(zone_ids.size):
            self.zone = zone_ids[zone_index]
            self.zone_index = zone_index
            if (zone_ids_to_process is not None) and (self.zone not in zone_ids_to_process):
                continue
            self.build_in_zone = {"residential": False, "non_residential": False}
            if self.type["residential"]:
                if to_be_placed_households[zone_index] > 0:
                    self.build_in_zone["residential"] = True
            if self.type["non_residential"]:
                if to_be_placed_jobs[zone_index] > 0:
                    self.build_in_zone["non_residential"] = True
            if not self.build_in_zone["residential"] and not self.build_in_zone["non_residential"]:
                continue
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
            self.weight[:] = original_weight[:]
            if self.weight[idx_zone].sum() <= 0:
                logger.log_status("No non-zero weights for zone %s." % self.zone)
            while isinf(self.weight[idx_zone].sum()):
                self.weight[idx_zone] = self.weight[idx_zone]/10
            self.second_pass = {}
            DevelopmentProjectProposalSamplingModel.run(self, **kwargs)                
            status = self.proposal_set.get_attribute("status_id")
            where_not_active = where(status[idx_zone] != self.proposal_set.id_active)[0]
            status[idx_zone[where_not_active]] = self.proposal_set.id_refused
            self.proposal_set.modify_attribute(name="status_id", data=status)
            if ((zone_index+1) % 50) == 0: # flush every 50th zone 
                self.proposal_set.flush_dataset()
                
        self.proposal_set.set_values_of_one_attribute("status_id", self.proposal_set.id_not_available, where(status != self.proposal_set.id_active)[0])
        return (self.proposal_set, [])
    
    def _is_target_reached(self, column_value=()):
        if column_value and not self.second_pass.has_key(column_value):
            self.second_pass[column_value] = True
            # set total spaces, occupied spaces and target spaces
            realestate_indexes = where(logical_and(self.get_index_by_condition(self.realestate_dataset.column_values, column_value), 
                                       self.realestate_dataset['zone_id'] == self.zone))
            self.accounting[column_value]["total_spaces"] = self.realestate_dataset.total_spaces[realestate_indexes].sum()
            self.accounting[column_value]["occupied_spaces"] = self.occuppied_estimate[column_value][self.zone_index]
            self.accounting[column_value]["target_spaces"] = int(round(self.accounting[column_value]["occupied_spaces"]))
                
        if column_value:
            if self.is_residential_bt[column_value] and not self.build_in_zone["residential"]:
                return True
            if not self.is_residential_bt[column_value] and not self.build_in_zone["non_residential"]:
                return True
            if self.accounting.has_key(column_value):
                accounting = self.accounting[column_value]
                result = (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                                accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                return result
            else:
                return True
        results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                   for column_value, accounting in self.accounting.items() ]
        return all(results)
        
    def get_do_not_count_residential_units(self, zones):
        result = zeros(zones.size(), dtype='int32')
        for building_type in self.bt_do_not_count:
            result += zones.compute_variables(["zone.aggregate(building.residential_units * (building.building_type_id == %s), [parcel])" % building_type],
                                    dataset_pool=self.dataset_pool)
        return result

    def compute_job_building_type_distribution(self):
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        alldata = self.dataset_pool.get_dataset('alldata')
        building_type_ids = building_type_dataset.get_id_attribute()
        alldata.compute_variables(map(lambda type: 
            "number_of_jobs_for_bt_%s = alldata.aggregate_all(psrc_parcel.building.number_of_non_home_based_jobs * (building.building_type_id == %s))" % (type,type),
                building_type_ids) + 
              ["number_of_nhb_jobs = alldata.aggregate_all(psrc_parcel.building.number_of_non_home_based_jobs)"], 
                                  dataset_pool=self.dataset_pool)
        job_building_type_distribution = zeros(building_type_ids.size)
        for itype in range(building_type_ids.size):
            job_building_type_distribution[itype] = alldata.get_attribute(
              'number_of_jobs_for_bt_%s' % building_type_ids[itype])[0]/float(alldata.get_attribute('number_of_nhb_jobs')[0])
        return job_building_type_distribution
    
    def compute_household_building_type_distribution(self):
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        alldata = self.dataset_pool.get_dataset('alldata')
        building_type_ids = building_type_dataset.get_id_attribute()
        sumhhs = 0
        for itype in range(building_type_ids.size):
            if building_type_ids[itype] in self.bt_do_not_count:
                continue
            hhs = alldata.compute_variables("number_of_households_for_bt_%s = alldata.aggregate_all(urbansim_parcel.building.number_of_households * (building.building_type_id == %s))" % (building_type_ids[itype],building_type_ids[itype]),
                                  dataset_pool=self.dataset_pool)
            sumhhs = sumhhs + hhs[0]
        building_type_distribution = zeros(building_type_ids.size)
        for itype in range(building_type_ids.size):
            if building_type_ids[itype] in self.bt_do_not_count:
                continue
            building_type_distribution[itype] = alldata['number_of_households_for_bt_%s' % building_type_ids[itype]][0]/float(sumhhs)
        return building_type_distribution
        
    def create_zone_bt_sqft_table(self):
        zone_average_dataset = self.dataset_pool.get_dataset("building_sqft_per_job")
        zone_ids_in_zad = zone_average_dataset.get_attribute("zone_id").astype("int32")
        bt_in_zad = zone_average_dataset.get_attribute("building_type_id")
        sqft_in_zad = zone_average_dataset.get_attribute("building_sqft_per_job")
        mean_value = sqft_in_zad.mean()
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        building_type_ids = building_type_dataset.get_id_attribute()
        zone_bt_lookup = mean_value*ones((self.max_zone+1, self.max_building_type+1)) 
        for i in range(zone_average_dataset.size()):
            zone_bt_lookup[zone_ids_in_zad[i], bt_in_zad[i]] = sqft_in_zad[i]
        return zone_bt_lookup
        
    def get_weighted_job_sqft(self):
        job_building_type_distribution = self.compute_job_building_type_distribution()
        sqft_lookup = self.create_zone_bt_sqft_table()
        building_type_dataset = self.dataset_pool.get_dataset('building_type')
        building_type_ids = building_type_dataset.get_id_attribute()
        return (sqft_lookup[:,building_type_ids] * job_building_type_distribution).sum(axis=1)
        