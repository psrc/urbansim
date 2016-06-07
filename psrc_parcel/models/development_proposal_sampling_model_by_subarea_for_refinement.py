# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, logical_not, logical_or, array, ones, isinf, round, in1d
from opus_core.logger import logger
from opus_core.misc import clip_to_zero_if_needed, unique, safe_array_divide
from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel
from opus_core.datasets.dataset import DatasetSubset

class DevelopmentProposalSamplingModelBySubareaForRefinement(DevelopmentProjectProposalSamplingModel):
        
    def __init__(self, subarea_name, intermediates_to_realestate, **kwargs):
        super(DevelopmentProposalSamplingModelBySubareaForRefinement, self).__init__(**kwargs)
        self.subarea_name = subarea_name
        self.intermediates_to_realestate = intermediates_to_realestate
        
    def run(self, location_ids_to_process=None, type=None, year=2000, n=500, 
            realestate_dataset_name = 'building', process_planned=False, modify_start_year=True, **kwargs):
        """If 'type' is None, the model runs for both, residential and non-residential space. Alternatively,
        it can be set to 'residential' or 'non_residential'.
        modify_start_year should be set to True if the model is run in a different year than start_year 
        of projects that should be processed.
        """

        self.type = {"residential": False,
                     "non_residential": False}
        if (type is None) or (type == 'residential'):
            self.type["residential"] = True
        if (type is None) or (type == 'non_residential'):
            self.type["non_residential"] = True
        
        regions = self.dataset_pool.get_dataset(self.subarea_name)
        self.subarea_id_name = regions.get_id_name()[0]
        if not process_planned:
            self.proposal_set.id_planned = 99999 # to switch processing of planned proposals of
        
        target_vacancies = self.dataset_pool.get_dataset('target_vacancy')
        tv_building_types = unique(target_vacancies.get_attribute('building_type_id'))
        
        bldgs = self.dataset_pool.get_dataset(realestate_dataset_name)
        bts = self.dataset_pool.get_dataset('building_type')
        all_building_types = bts.get_id_attribute()
        
        self.bt_do_not_count = array(map(lambda x: x not in tv_building_types, all_building_types))
        self.bt_do_not_count =  all_building_types[self.bt_do_not_count]
        
        regions.compute_variables(["placed_households = %s.aggregate(%s.number_of_agents(household), intermediates=[%s])" % (self.subarea_name, realestate_dataset_name, self.intermediates_to_realestate),
                                 "occupied_spaces = %s.aggregate(psrc_parcel.%s.occupied_spaces * (urbansim_parcel.%s.is_residential == 0), [%s])" % (self.subarea_name, realestate_dataset_name, realestate_dataset_name, self.intermediates_to_realestate)
                                 ], dataset_pool=self.dataset_pool)
        bldgs.compute_one_variable_with_unknown_package("%s" % self.subarea_id_name, dataset_pool=self.dataset_pool)
        self.occuppied_estimate = {}
        self.occupied_estimate_residential = 0
        self.occupied_estimate_nonresidential = 0
        btdistr = self.compute_building_type_distribution(bts, realestate_dataset_name, regions)
        btdistr_nonres = self.compute_job_building_type_distribution(bts, realestate_dataset_name, regions)
        if self.type["residential"]: 
            regions.compute_variables(["total_number_of_households = %s.number_of_agents(household)" % self.subarea_name
                                     ], dataset_pool=self.dataset_pool)
            to_be_placed_households = regions["total_number_of_households"] - regions["placed_households"]            
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count or not bts['is_residential'][ibt]:
                    continue
                # serves as target
                self.occuppied_estimate[(bt,)] = regions.sum_over_ids(bldgs[self.subarea_id_name], 
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + round(btdistr[ibt]*to_be_placed_households)
                self.occupied_estimate_residential = self.occupied_estimate_residential + self.occuppied_estimate[(bt,)]
            # add 2%
            self.occupied_estimate_residential = self.occupied_estimate_residential*1.02
                
        if self.type["non_residential"]:    
            regions.compute_variables(["number_of_all_nhb_jobs = %s.aggregate(job.home_based_status==0)" % self.subarea_name],
                                 dataset_pool=self.dataset_pool)
            to_be_placed_jobs = regions.get_attribute("number_of_all_nhb_jobs") - regions['occupied_spaces']                                
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count or bts['is_residential'][ibt]:
                    continue
                # serves as target
                self.occuppied_estimate[(bt,)] = regions.sum_over_ids(bldgs[self.subarea_id_name], 
                        bldgs['occupied_spaces']*(bldgs['building_type_id']==bt)) + round(to_be_placed_jobs * btdistr_nonres[ibt])
                self.occupied_estimate_nonresidential = self.occupied_estimate_nonresidential + self.occuppied_estimate[(bt,)]
            # add 2%
            self.occupied_estimate_nonresidential = self.occupied_estimate_nonresidential*1.02
                      
        self.is_residential_bt = {}
        for ibt in range(all_building_types.size):
            self.is_residential_bt[(all_building_types[ibt],)] = bts['is_residential'][ibt]
            
        region_ids_in_proposals = self.proposal_set.compute_variables("%s = development_project_proposal.disaggregate(urbansim_parcel.parcel.%s)" % (self.subarea_id_name, self.subarea_id_name), 
                                                dataset_pool=self.dataset_pool)
        region_ids = regions.get_id_attribute()
        # keep copy of the weights
        original_weight = self.weight.copy()
        if modify_start_year:
            start_year = year
            self.proposal_set.modify_attribute(name="start_year", data=array(self.proposal_set.size()*[start_year]))
        status = self.proposal_set.get_attribute("status_id")
        self.proposal_set.add_primary_attribute(name='original_status_id', data=status.copy())
        self.all_demolished_buildings = []
        for subarea_index in range(region_ids.size):
            self.subarea = region_ids[subarea_index]
            self.subarea_index = subarea_index
            if (location_ids_to_process is not None) and (self.subarea not in location_ids_to_process):
                continue
            self.build_in_subarea = {"residential": False, "non_residential": False}
            if self.type["residential"]:
                if to_be_placed_households[subarea_index] > 0:
                    self.build_in_subarea["residential"] = True
            if self.type["non_residential"]:
                if to_be_placed_jobs[subarea_index] > 0:
                    self.build_in_subarea["non_residential"] = True
            if not self.build_in_subarea["residential"] and not self.build_in_subarea["non_residential"]:
                continue
            where_subarea = region_ids_in_proposals == self.subarea
            idx_subarea_in_prop = where(where_subarea)[0]
            if (self.proposal_set.id_active in status[idx_subarea_in_prop]) or (self.proposal_set.id_refused in status[idx_subarea_in_prop]):
                continue # this subarea was handled previously
            if idx_subarea_in_prop.size <= 0:
                logger.log_status("No proposals for subarea %s" % self.subarea)
                continue
            idx_out_subarea_not_active_not_refused = where(logical_and(logical_and(status != self.proposal_set.id_active, 
                                                                               status != self.proposal_set.id_refused),
                                                                    logical_not(where_subarea)))[0]
            status[idx_subarea_in_prop] = self.proposal_set['original_status_id'][idx_subarea_in_prop]
            status[idx_out_subarea_not_active_not_refused] = self.proposal_set.id_not_available
            self.proposal_set.modify_attribute(name="status_id", data=status)
            
            logger.log_status("\nDPSM for subarea %s" % self.subarea)
            self.weight[:] = original_weight[:]
            if self.weight[idx_subarea_in_prop].sum() <= 0:
                logger.log_status("No non-zero weights for subarea %s." % self.subarea)
            while isinf(self.weight[idx_subarea_in_prop].sum()):
                self.weight[idx_subarea_in_prop] = self.weight[idx_subarea_in_prop]/10.
            # check building types that don't have any proposals
            no_space = []
            for ibt in range(all_building_types.size):
                bt = all_building_types[ibt]
                if bt in self.bt_do_not_count:
                    continue
                if btdistr[ibt][subarea_index] == 0:
                    no_space = no_space + [bt]
            if len(no_space) > 0:
                logger.log_warning('No developable space for building types: %s' % str(no_space).strip('[]'))
            self.second_pass = {}
            DevelopmentProjectProposalSamplingModel.run(self, n=n, realestate_dataset_name=realestate_dataset_name, **kwargs)                
            status = self.proposal_set.get_attribute("status_id")
            self.proposal_set.modify_attribute(name="original_status_id", data=status[idx_subarea_in_prop], index=idx_subarea_in_prop)
            where_not_active = where(status[idx_subarea_in_prop] != self.proposal_set.id_active)[0]
            status[idx_subarea_in_prop[where_not_active]] = self.proposal_set.id_refused
            self.proposal_set.modify_attribute(name="status_id", data=status)
            self.all_demolished_buildings.extend(self.demolished_buildings)
            if ((subarea_index+1) % 50) == 0: # flush every 50th subarea 
                self.proposal_set.flush_dataset()
                
        self.proposal_set.set_values_of_one_attribute("status_id", self.proposal_set.id_not_available, where(status != self.proposal_set.id_active)[0])
        self.proposal_set.set_values_of_one_attribute("status_id", self.proposal_set.id_planned, where(self.proposal_set["original_status_id"] == self.proposal_set.id_planned)[0])
        return (self.proposal_set, bldgs.get_id_attribute()[self.all_demolished_buildings])
    
    def _is_target_reached(self, column_value=()):
        if column_value:
            if self.is_residential_bt[column_value] and not self.build_in_subarea["residential"]:
                return True
            if not self.is_residential_bt[column_value] and not self.build_in_subarea["non_residential"]:
                return True
            
        if column_value and not self.second_pass.has_key(column_value):
            self.second_pass[column_value] = True
            # set total spaces, occupied spaces and target spaces
            realestate_indexes = where(logical_and(self.get_index_by_condition(self.realestate_dataset.column_values, column_value), 
                                       self.realestate_dataset[self.subarea_id_name] == self.subarea))
            self.accounting[column_value]["total_spaces"] = self.realestate_dataset.total_spaces[realestate_indexes].sum()
            self.accounting[column_value]["occupied_spaces"] = 0 # should not be used
            self.accounting[column_value]["target_spaces"] = int(round(self.occuppied_estimate[column_value][self.subarea_index]))
                
        if column_value:
            if self.accounting.has_key(column_value):
                column_values = [column_value]
            else:
                return True
        else:
            column_values = self.accounting.keys()
            
        is_target_met = {}
        for column_value in column_values:
            # build as long as there is demand over all types of res/nonres
            tot = 0
            prop = 0
            demol = 0
            for bt in self.occuppied_estimate.keys():
                if (self.is_residential_bt[column_value] and not self.is_residential_bt[bt]) or (not self.is_residential_bt[column_value] and self.is_residential_bt[bt]):
                    continue
                if not self.accounting.has_key(bt):
                    realestate_indexes = where(logical_and(self.get_index_by_condition(self.realestate_dataset.column_values, column_value), 
                                   self.realestate_dataset[self.subarea_id_name] == self.subarea))
                    tot = tot + self.realestate_dataset.total_spaces[realestate_indexes].sum()
                else:
                    accounting = self.accounting[bt]
                    tot = tot + accounting.get("total_spaces",0)
                    prop = prop + accounting.get("proposed_spaces",0)
                    demol = demol + accounting.get("demolished_spaces",0)
            if self.is_residential_bt[column_value]:
                if not self.build_in_subarea["residential"]:
                    target = 0
                else:
                    target = self.occupied_estimate_residential[self.subarea_index]
            else: # non-residential
                if not self.build_in_subarea["non_residential"]:
                    target = 0
                else:                
                    target = self.occupied_estimate_nonresidential[self.subarea_index]
            is_target_met[column_value] = target <= (tot + prop - demol)
        results = is_target_met.values()
        return all(results)
        

    def compute_job_building_type_distribution(self, building_type_dataset, realestate_dataset_name, regions):
        building_type_ids = building_type_dataset.get_id_attribute()
        
        regions.compute_variables(map(lambda type: 
            "number_of_jobs_for_bt_%s = %s.aggregate(psrc_parcel.%s.number_of_non_home_based_jobs * (%s.building_type_id == %s))" % (type, self.subarea_name, realestate_dataset_name, realestate_dataset_name, type),
                building_type_ids[logical_not(in1d(building_type_ids, self.bt_do_not_count))]) + 
              ["number_of_nhb_jobs = %s.aggregate(psrc_parcel.%s.number_of_non_home_based_jobs)" % (self.subarea_name, realestate_dataset_name)], 
                                  dataset_pool=self.dataset_pool)
        building_type_distribution = {}
        for itype in range(building_type_ids.size):
            building_type_distribution[itype] = zeros(regions.size())
            if building_type_ids[itype] in self.bt_do_not_count:
                continue            
            building_type_distribution[itype] = safe_array_divide(
                    regions['number_of_jobs_for_bt_%s' % building_type_ids[itype]], regions['number_of_nhb_jobs'])
        return building_type_distribution
    
    def compute_building_type_distribution(self, building_type_dataset, realestate_dataset_name, regions):
        parcels = self.dataset_pool.get_dataset('parcel')        
        building_type_ids = building_type_dataset.get_id_attribute()
        regions.compute_variables(map(lambda type:
            "units_proposed_for_bt_%s = %s.aggregate(psrc_parcel.parcel.units_proposed_for_building_type_%s)" % (type, self.subarea_name, type), 
            building_type_ids[logical_not(in1d(building_type_ids, self.bt_do_not_count))]),
                    dataset_pool=self.dataset_pool)
        sumunits_residential = zeros(regions.size(), dtype='float32')        
        sumunits_nonresidential = zeros(regions.size(), dtype='float32')
        for itype in range(building_type_ids.size):
            if building_type_ids[itype] in self.bt_do_not_count:
                continue
            potential_units = regions["units_proposed_for_bt_%s" % building_type_ids[itype]]
            if building_type_dataset['is_residential'][itype]:
                sumunits_residential = sumunits_residential + potential_units
            else:
                sumunits_nonresidential = sumunits_nonresidential + potential_units
        building_type_distribution = {}
        for itype in range(building_type_ids.size):
            building_type_distribution[itype] = zeros(regions.size())
            if building_type_ids[itype] in self.bt_do_not_count:
                continue
            if building_type_dataset['is_residential'][itype]:
                sumunits = sumunits_residential
            else:
                sumunits = sumunits_nonresidential
            building_type_distribution[itype] = safe_array_divide(regions['units_proposed_for_bt_%s' % building_type_ids[itype]], sumunits)         
        return building_type_distribution
        
    def consider_proposals(self, proposal_indexes, force_accepting=False):
        if proposal_indexes.size == 0:
            return
        is_proposal_rejected = zeros(proposal_indexes.size, dtype="bool")
        sites = self.proposal_set["parcel_id"][proposal_indexes]
        self.proposal_set.compute_variables(['is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0',
                                             'total_spaces = development_project_proposal.aggregate(psrc_parcel.development_project_proposal_component.total_spaces)'],
                                                    dataset_pool=self.dataset_pool)
        self.realestate_dataset.compute_variables(['urbansim_parcel.building.is_residential', 'psrc_parcel.building.total_spaces'], dataset_pool=self.dataset_pool)
        #is_res_prop = self.proposal_set['is_res'][proposal_indexes]
        #proposal_indexes_copy = proposal_indexes.copy()
        #proposal_indexes[0:is_res_prop.sum()] = proposal_indexes_copy[is_res_prop]
        #proposal_indexes[is_res_prop.sum():]=proposal_indexes_copy[logical_not(is_res_prop)]
        for i, proposal_index in enumerate(proposal_indexes):
            if not is_proposal_rejected[i] and ((self.weight[proposal_index] > 0) or force_accepting):
                accepted = self.has_more_cubicles(proposal_index, force_accepting=force_accepting) and self.consider_proposal(proposal_index, force_accepting=force_accepting)
                if accepted:
                    is_proposal_rejected[ sites == sites[i]] = True
                    
    def has_more_cubicles(self, proposal_index, force_accepting=False):
        if force_accepting or not self.proposal_set["is_redevelopment"][proposal_index] or self.proposal_set["is_res"][proposal_index]:
            return True
        # check this only for non-residential redevelopment proposals
        this_site = self.proposal_set["parcel_id"][proposal_index]
        building_indexes = where(self.realestate_dataset['parcel_id']==this_site)[0]
        if self.realestate_dataset['is_residential'][building_indexes].any():
            return True
        # only accept if it fits more jobs then the existing structure
        return self.proposal_set["total_spaces"][proposal_index] >= self.realestate_dataset["total_spaces"][building_indexes].sum()