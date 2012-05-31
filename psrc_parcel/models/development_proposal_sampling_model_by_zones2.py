# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, logical_not, logical_or, array, ones, isinf
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

        target_vacancies = self.dataset_pool.get_dataset('target_vacancy')
        tv_building_types = unique(target_vacancies.get_attribute('building_type_id'))
        
        bldgs = self.dataset_pool.get_dataset('building')
        bts = self.dataset_pool.get_dataset('building_type')
        all_building_types = bts.get_id_attribute()
        
        self.bt_do_not_count = array(map(lambda x: x not in tv_building_types, all_building_types))
        self.bt_do_not_count =  all_building_types[self.bt_do_not_count]
        self.do_not_count_residential_units  = self.get_do_not_count_residential_units(zones)
        
        zones.compute_variables(["existing_residential_units = zone.aggregate(building.residential_units, [parcel])",
                                 "existing_job_spaces = zone.aggregate(psrc_parcel.building.total_spaces, [parcel])",
                                 "placed_households = zone.aggregate(building.number_of_agents(household))"
                                 ], dataset_pool=self.dataset_pool)
        bldgs.compute_variables(["psrc_parcel.building.occupied_spaces", "urbansim_parcel.building.zone_id"], dataset_pool=self.dataset_pool)
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
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + hhdistr[ibt]*to_be_placed_households
            maxiter = 20
        if self.type["non_residential"]:    
            zones.compute_variables(["number_of_all_nhb_jobs = zone.aggregate(job.home_based_status==0)",
                                     "number_of_placed_nhb_jobs = zone.aggregate(psrc_parcel.building.number_of_non_home_based_jobs)"],
                                 dataset_pool=self.dataset_pool)
            
            occupied_building_sqft = zones.compute_variables(
                     ["zone.aggregate(urbansim_parcel.building.occupied_spaces)"
                                 ], dataset_pool=self.dataset_pool)
            existing_building_sqft = zones.compute_variables(
                     ["zone.aggregate(building.non_residential_sqft)"],
                         dataset_pool=self.dataset_pool)
            to_be_used_sqft = existing_building_sqft - occupied_building_sqft
            to_be_placed_sqft = (zones.get_attribute("number_of_all_nhb_jobs") - 
                                 zones.get_attribute("number_of_placed_nhb_jobs")) * self.get_weighted_job_sqft()[zones.get_id_attribute()]
            job_building_type_distribution = self.compute_job_building_type_distribution()
            sqft_lookup = self.create_zone_bt_sqft_table()
            to_be_placed_jobs = (zones.get_attribute("number_of_all_nhb_jobs") - 
                                 zones.get_attribute("number_of_placed_nhb_jobs"))
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count or bts['is_residential'][ibt]:
                    continue
                self.occuppied_estimate[(bt,)] = zones.sum_over_ids(bldgs['zone_id'], 
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + to_be_placed_jobs * sqft_lookup[zones['zone_id'],bt] * job_building_type_distribution[ibt]
            maxiter = 1
                             
        existing_residential_units = zones.get_attribute("existing_residential_units") - self.do_not_count_residential_units
        existing_job_spaces = zones.get_attribute("existing_job_spaces")
        
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
                if occupied_residential_units[zone_index] > 0:
                    self.existing_to_occupied_ratio_residential =  \
                            max(existing_residential_units[zone_index],1) / float(occupied_residential_units[zone_index])
                    self.build_in_zone["residential"] = True
            if self.type["non_residential"]:
                if to_be_placed_sqft[zone_index] > 0:
                    self.existing_to_occupied_ratio_non_residential =  \
                            max(to_be_used_sqft[zone_index],1) / float(to_be_placed_sqft[zone_index])
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
            for iter in range(maxiter):
                self.weight[:] = original_weight[:]
                if self.weight[idx_zone].sum() <= 0:
                    logger.log_status("No non-zero weights for zone %s in iteration %s." % (self.zone, iter))
                    break  
                while isinf(self.weight[idx_zone].sum()):
                    self.weight[idx_zone] = self.weight[idx_zone]/10
                self.first_pass = True
                DevelopmentProjectProposalSamplingModel.run(self, **kwargs)
                if self.type["residential"]:
                    if (len(self.accepted_proposals)<=0) or self.vacancy_rate_met(existing_residential_units[zone_index],
                                                                              occupied_residential_units[zone_index]):
                        break
                    #print "ratio:", self.existing_to_occupied_ratio_residential
                
            status = self.proposal_set.get_attribute("status_id")
            where_not_active = where(status[idx_zone] != self.proposal_set.id_active)[0]
            status[idx_zone[where_not_active]] = self.proposal_set.id_refused
            self.proposal_set.modify_attribute(name="status_id", data=status)
            if ((zone_index+1) % 50) == 0: # flush every 50th zone 
                self.proposal_set.flush_dataset()
                
        self.proposal_set.set_values_of_one_attribute("status_id", self.proposal_set.id_not_available, where(status != self.proposal_set.id_active)[0])
        return (self.proposal_set, [])
    
    def vacancy_rate_met(self, existing, occupied):
        if self.type["non_residential"] or not self.build_in_zone["residential"]: 
            return True
        # applies only to residential case
        is_residential = self.current_target_vacancy.get_attribute("is_residential")
        type_ids = self.current_target_vacancy.get_attribute("building_type_id")
        avg_tv = 0.0
        demolished = 0
        proposed_total = 0
        for index in arange(self.current_target_vacancy.size())[where(is_residential)]:
            type_id = type_ids[index]
            avg_tv += self.target_vacancies[type_id]
            demolished += self.demolished_units[type_id]
            if type_id not in self.proposed_units_from_previous_iterations.keys():
                self.proposed_units_from_previous_iterations[type_id] = 0
            self.proposed_units_from_previous_iterations[type_id] += self.proposed_units[type_id]
            proposed_total += self.proposed_units_from_previous_iterations[type_id]
            
        avg_tv = avg_tv/float(is_residential.sum())
        units_stock = existing - demolished + proposed_total
        current_vr = (units_stock - occupied) / float(max(units_stock,1))
        logger.log_status("Current overall vacancy rate: %s, average vacancy rate: %s" % (current_vr, avg_tv))
        #print "units_stock:", units_stock
        #print "occupied:", occupied
        if current_vr >= avg_tv:
            return True
        logger.log_status("Current overall vacancy rate: %s, average vacancy rate: %s" % (current_vr, avg_tv))
        self.existing_to_occupied_ratio_residential = max(units_stock,1) / float(occupied)
        return False
    
    def _is_target_reached(self, column_value=()):
        if self.first_pass:
            self.first_pass = False
            # set occupied spaces and target spaces
            for column_value, accounting in self.accounting.items():
                self.accounting[column_value]["occupied_spaces"] = self.occuppied_estimate[column_value][self.zone_index]
                self.accounting[column_value]["target_spaces"] = int( round( self.accounting[column_value]["occupied_spaces"] /\
                                                     (1 - accounting["target_vacancy"])))
                
        if column_value:
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
            unit_name = self.unit_name[is_residential[index]]
            is_in_right_zone = building_zone_ids == self.zone 
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            self.existing_units[type_id] = buildings.get_attribute(unit_name)[is_matched_type*is_in_right_zone].astype("float32").sum()
            self.existing_units[type_id] += self.proposed_units_from_previous_iterations.get(type_id, 0)
            self.occupied_units[type_id] = 0
            if is_residential[index]:
                if self.type["residential"] and self.build_in_zone["residential"]:
                    self.occupied_units[type_id] = int(max(self.existing_units[type_id],1)/self.existing_to_occupied_ratio_residential)
                    vr = max(self.existing_units[type_id] - self.occupied_units[type_id], 0) / float(max(self.existing_units[type_id],1))
                else:
                    vr=1.0
            else:
                if self.type["non_residential"] and self.build_in_zone["non_residential"]:
                    already_occupied = buildings.get_attribute("occupied_building_sqft_by_non_home_based_jobs")[is_matched_type*is_in_right_zone].sum()
                    remaining_existing_units = clip_to_zero_if_needed(self.existing_units[type_id] - already_occupied)
                    self.occupied_units[type_id] = int(remaining_existing_units/self.existing_to_occupied_ratio_non_residential)
                    vr = max(self.existing_units[type_id] - (self.occupied_units[type_id]+already_occupied), 1) / float(max(self.existing_units[type_id],1))
                    self.existing_units[type_id] = remaining_existing_units
                else:
                    #vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(max(self.existing_units[type_id],1))
                    vr = 1.0
            #print 'vacancy_rates:', type_id, vr
            if is_residential[index]:
                self.accepting_proposals[type_id] = self.build_in_zone["residential"] and vr < target
            else:
                self.accepting_proposals[type_id] = self.build_in_zone["non_residential"] and vr < target

                