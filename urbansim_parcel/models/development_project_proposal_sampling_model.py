#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.misc import unique_values
from opus_core.variables.variable_name import VariableName
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from numpy import zeros, arange, where, ones, logical_or, logical_and, logical_not, int32, float32, sometrue
from numpy import compress, take, alltrue, argsort, array, int8, bool8, ceil, sort, minimum, concatenate
from gc import collect
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.model import Model
from scipy import ndimage

class DevelopmentProjectProposalSamplingModel(Model):

    def __init__(self, proposal_set,
                 sampler="opus_core.samplers.weighted_sampler",
                 weight_string = "exp_roi = exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                 filter_attribute=None,
                 run_config=None, estimate_config=None,
                 debuglevel=0, dataset_pool=None):
        """
        this model sample project proposals from proposal set weighted by exponentiated ROI
        """
        self.dataset_pool = self.create_dataset_pool(dataset_pool, pool_packages=['urbansim_parcel', 'urbansim', 'opus_core'])
        self.dataset_pool.add_datasets_if_not_included({proposal_set.get_dataset_name(): proposal_set})
        self.proposal_set = proposal_set
        if not self.dataset_pool.has_dataset("development_project_proposal_component"):
            self.proposal_component_set = create_from_proposals_and_template_components(proposal_set, 
                                                       self.dataset_pool.get_dataset('development_template_component'))
            self.dataset_pool.replace_dataset(self.proposal_component_set.get_dataset_name(), self.proposal_component_set)
        else:
            self.proposal_component_set = self.dataset_pool.get_dataset("development_project_proposal_component")

        if weight_string is not None:
            if weight_string not in proposal_set.get_known_attribute_names():
                proposal_set.compute_variables(weight_string, dataset_pool=self.dataset_pool)
            self.weight = self.proposal_set.get_attribute(weight_string)
        else:
            self.weight = ones(self.proposal_set.size(), dtype="float64")  #equal weight

        ## TODO: handling of filter_attribute
#        if filter_attribute is not None:
#            if filter_attribute not in proposal_set.get_known_attribute_names():
#                proposal_set.compute_variables(filter_attribute)
#            elif not isinstance(filter_attribute, array):
#
#            self.weight = self.weight * proposal_set.get_attribute(filter_attribute)


    def run(self, n=500, run_config=None, debuglevel=0):
        """
        n - sample n proposals at a time, evaluate them one by one
        """

#        if data_objects is not None:
#            self.dataset_pool.add_datasets_if_not_included(data_objects)

        current_year = SimulationState().get_current_time()

        self.proposal_component_set.compute_variables([
            'urbansim_parcel.development_project_proposal_component.units_proposed'],
                                        dataset_pool=self.dataset_pool)
        self.proposal_set.compute_variables([
            'urbansim_parcel.development_project_proposal.number_of_components'],
                                        dataset_pool=self.dataset_pool)
        buildings = self.dataset_pool.get_dataset("building")
        buildings.compute_variables([
                                    "occupied_building_sqft=urbansim_parcel.building.occupied_building_sqft_by_jobs",
                                    "urbansim_parcel.building.existing_units",
                                    "occupied_residential_units = urbansim_parcel.building.number_of_households",
                                    #"occupied_parcel_sqft = urbansim_parcel.building.occupied_building_sqft",
                                    ],
                                    dataset_pool=self.dataset_pool)
        parcels = self.dataset_pool.get_dataset('parcel')
        parcels.compute_variables(['urbansim_parcel.parcel.building_sqft', 'urbansim_parcel.parcel.residential_units'],
                                  dataset_pool=self.dataset_pool)
        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')
        target_vacancy.compute_variables(['type_name=target_vacancy.disaggregate(building_type.building_type_name)',
                                          'unit_name=target_vacancy.disaggregate(building_type.unit_name)',
                                          'is_residential = target_vacancy.disaggregate(building_type.is_residential)'],
                                         dataset_pool=self.dataset_pool)
        current_target_vacancy = DatasetSubset(target_vacancy, index=where(target_vacancy.get_attribute("year")==current_year)[0])

        self.existing_units = {}   #total existing units by land_use type
        self.occupied_units = {}   #total occupied units by land_use type
        self.proposed_units = {}   #total proposed units by land_use type
        self.demolished_units = {} #total (to be) demolished units by land_use type
        self.demolished_buildings = array([], dtype='int32')  #id of buildings to be demolished

        components_building_type_ids = self.proposal_component_set.get_attribute("building_type_id").astype("int32")
        proposal_ids = self.proposal_set.get_id_attribute()
        proposal_ids_in_component_set = self.proposal_component_set.get_attribute("proposal_id")
        all_units_proposed = self.proposal_component_set.get_attribute("units_proposed")
        number_of_components_in_proposals = self.proposal_set.get_attribute("number_of_components")
        
        self.accepting_proposals = zeros(components_building_type_ids.max()+1, dtype='bool8')  #whether accepting new proposals, for each building type
        self.accepted_proposals = [] # index of accepted proposals

        self.target_vacancies = {}
        tv_building_types = current_target_vacancy.get_attribute("building_type_id")
        tv_rate = current_target_vacancy.get_attribute("target_vacancy_rate")
        for itype in range(tv_building_types.size):
            self.target_vacancies[tv_building_types[itype]] = tv_rate[itype]
            
        self.check_vacancy_rates(current_target_vacancy)  #initialize self.accepting_proposal based on current vacancy rate

        # consider only those proposals that have all components of accepted type and sum of proposed units > 0
        is_accepted_type = self.accepting_proposals[components_building_type_ids]
        sum_is_accepted_type_over_proposals = array(ndimage.sum(is_accepted_type, labels = proposal_ids_in_component_set, 
                                                          index = proposal_ids))
        sum_of_units_proposed = array(ndimage.sum(all_units_proposed, labels = proposal_ids_in_component_set, 
                                                          index = proposal_ids))
        is_proposal_eligible = logical_and(sum_is_accepted_type_over_proposals == number_of_components_in_proposals,
                                     sum_of_units_proposed > 0)

        logger.log_status("Sampling from %s eligible proposals." % is_proposal_eligible.sum())
        # consider planned proposals (they are not sampled)
        for status in [self.proposal_set.id_planned, self.proposal_set.id_proposed]:
            if self.weight.sum() == 0.0:
                break
            idx = where(logical_and(self.proposal_set.get_attribute("status_id") == status, is_proposal_eligible))[0]
            if idx.size <= 0:
                continue
            isorted = self.weight[idx].argsort()[range(idx.size-1,-1,-1)]
            # consider proposals in order of the highest weights
            self.consider_proposals(idx[isorted], current_target_vacancy, build_only_in_empty_parcel=False)

        # consider tentative proposals
        for status in [self.proposal_set.id_tentative]:
            idx = where(logical_and(self.proposal_set.get_attribute("status_id") == status, is_proposal_eligible))[0]
            if idx.size <= 0:
                continue
            while (True in self.accepting_proposals):
                if self.weight[idx].sum() == 0.0:
                    break
            #    raise RuntimeError, "Running out of proposals; there aren't any proposals with non-zero weight"
                idx = idx[self.weight[idx] > 0]
                n = minimum(idx.size, n)
                sampled_proposal_indexes = probsample_noreplace(proposal_ids[idx], n, 
                                                prob_array=self.weight[idx]/float(self.weight[idx].sum()),
                                                exclude_index=None, return_indices=True)
                # sort according to the weights
                isorted = self.weight[idx[sampled_proposal_indexes]].argsort()[range(sampled_proposal_indexes.size-1,-1,-1)]
                self.consider_proposals(arange(self.proposal_set.size())[idx[sampled_proposal_indexes[isorted]]],
                                        current_target_vacancy
                                       )
                self.weight[idx[sampled_proposal_indexes]] = 0

        # set status of accepted proposals to 'active'
        self.proposal_set.modify_attribute(name="status_id", data=self.proposal_set.id_active,
                                          index=array(self.accepted_proposals, dtype='int32'))
        logger.log_status("Status of %s development proposals set to active." % len(self.accepted_proposals))
        logger.log_status("Target/existing vacancy rates (reached using eligible proposals) by building type:")
        for type_id in self.existing_units.keys():
            units_stock = self.existing_units[type_id] - self.demolished_units[type_id] + self.proposed_units[type_id]
            logger.log_status("%s: %s" % (type_id, (units_stock - self.occupied_units[type_id]) / float(units_stock)))
        # delete all tentative (not accepted) proposals from the proposal set
        self.proposal_set.remove_elements(where(
                    self.proposal_set.get_attribute("status_id") == self.proposal_set.id_tentative)[0])
#        schedule_development_projects = self.schedule_accepted_proposals()
        
        return self.proposal_set  #schedule_development_projects

    def check_vacancy_rates(self, target_vacancy):
        type_ids = target_vacancy.get_attribute("building_type_id")
        type_names = target_vacancy.get_attribute("type_name")
        unit_names = target_vacancy.get_attribute("unit_name")
        is_residential = target_vacancy.get_attribute("is_residential")
        buildings = self.dataset_pool.get_dataset("building")
        building_type_ids = buildings.get_attribute("building_type_id")
        parcels = self.dataset_pool.get_dataset('parcel')
        self.units_built = {}
        self.units_built_pointer = {}
        for index in arange(target_vacancy.size()):
            type_id = type_ids[index]
            type_name = type_names[index]
            unit_name = unit_names[index]  #vacancy by type, could be residential, non-residential, or by building_type
            target = self.target_vacancies[type_id]           
            is_matched_type = building_type_ids == type_id
            if is_residential[index]:
                unit_name = "residential_units"
            self.existing_units[type_id] = buildings.get_attribute(unit_name)[is_matched_type].astype("float32").sum()
            self.occupied_units[type_id] = buildings.get_attribute("occupied_%s" % unit_name)[is_matched_type].astype("float32").sum()
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(self.existing_units[type_id])
            if vr < target:
                self.accepting_proposals[type_id] = True
                if unit_name not in self.units_built.keys():
                    self.units_built[unit_name] = parcels.get_attribute_by_index(unit_name, 
                                                        parcels.get_id_index(self.proposal_set.get_attribute('parcel_id')))
                self.units_built_pointer[type_id] = self.units_built[unit_name]

    def consider_proposals(self, proposal_indexes, target_vacancy, build_only_in_empty_parcel=True):
        #buildings = self.dataset_pool.get_dataset("building")
        #building_site = buildings.get_attribute("parcel_id")

        proposals_parcel_ids = self.proposal_set.get_attribute("parcel_id")
        
        #proposal_type = self.proposal_set.get_attribute_by_index("unit_type", proposal_indexes)
#        pro_rated = self.proposal_set.get_attribute_by_index("pro_rated", proposal_indexes) #whether the project is pro_rated
#        years = self.proposal_set.get_attribute_by_index("years", proposal_indexes)         #how many years it take to build
#        proposal_construction_type = self.proposal_set.get_attribute_by_index("construction_type", proposal_indexes)  #redevelopment or addition

        components_building_type_ids = self.proposal_component_set.get_attribute("building_type_id").astype("int32")
        proposal_ids = self.proposal_set.get_id_attribute()
        proposal_ids_in_component_set = self.proposal_component_set.get_attribute("proposal_id")
        all_units_proposed = self.proposal_component_set.get_attribute("units_proposed")
        number_of_components_in_proposals = self.proposal_set.get_attribute("number_of_components")
        
        is_proposal_rejected = zeros(proposal_indexes.size, dtype=bool8)
        proposal_site = proposals_parcel_ids[proposal_indexes]
        
        for i in range(proposal_indexes.size):
            if not (True in self.accepting_proposals):
                # if none of the types is accepting_proposals, exit
                # this is put in the loop to check if the last accepted proposal has sufficed
                # the target vacancy rates for all types
                return
            if is_proposal_rejected[i]:
                continue
            proposal_index = proposal_indexes[i]  # consider 1 proposed project at a time
            proposal_index_in_component_set = where(proposal_ids_in_component_set == proposal_ids[proposal_index])[0]
            units_proposed = all_units_proposed[proposal_index_in_component_set]
            component_types = components_building_type_ids[proposal_index_in_component_set]

            this_site = proposal_site[i]
            if False: #proposal_construction_type[i] == 'R':
                ##TODO:if it's a redevelopment project,demolish existing buildings of this site
                affected_building = where(building_site==this_site)[0]
                self.demolished_buildings = concatenate((self.demolished_buildings, affected_building))
                for type in existing_units.keys():
                    self.demolished_units[type] += existing_units[type][affected_building].sum() #demolish affected buildings
                    #existing_units[affected_building] = 0
                    #moving_agents += occupied_units[affected_building].sum()
                    #occupied_units[affected_building] = 0
            for itype_id in range(component_types.size): #
                type_id = component_types[itype_id]
                if build_only_in_empty_parcel and self.units_built_pointer[type_id][proposal_indexes[i]] > 0: # don't build anything in a parcel that has units built
                    is_proposal_rejected[i] = True
                    break
                # this loop is only needed when a proposal could provide units from more than 1 generic building types

                #if pro_rated[i]:
                    #self.proposed_units[type_id] += round(unit_proposed / years[i])
                    ##TODO: handle pro-rated projects
                #else:
                self.proposed_units[type_id] += units_proposed[itype_id]
                units_stock = self.existing_units[type_id] - self.demolished_units[type_id] + self.proposed_units[type_id]
                vr = (units_stock - self.occupied_units[type_id]) / float(units_stock)
                if vr >= self.target_vacancies[type_id]:
                    self.accepting_proposals[type_id] = False
                    # reject all proposals that have one of the components of this type
                    consider_idx = proposal_indexes[(i+1):proposal_indexes.size] # consider only proposals to be processed
                    if consider_idx.size > 0:
                        is_accepted_type = self.accepting_proposals[components_building_type_ids]
                        sum_is_accepted_type_over_proposals = array(ndimage.sum(is_accepted_type, 
                                                                            labels = proposal_ids_in_component_set, 
                                                          index = proposal_ids[consider_idx]))                   
                        is_rejected_indices = where(sum_is_accepted_type_over_proposals < 
                                                number_of_components_in_proposals[consider_idx])[0]
                        is_proposal_rejected[arange((i+1),proposal_indexes.size)[is_rejected_indices]] = True
                        self.weight[consider_idx[is_rejected_indices]] = 0.0

            if not is_proposal_rejected[i]:
                # proposal accepted
                self.accepted_proposals.append(proposal_index)
            # reject all pending proposals for this site
            is_proposal_rejected[proposal_site == this_site] = True
            if is_proposal_rejected.sum() == is_proposal_rejected.size:
                return
            # don't consider proposed projects for this site in the future (i.e. in further sampling)
            self.weight[proposals_parcel_ids == this_site] = 0.0
            if self.weight[proposal_indexes].sum() == 0.0:
                return

        ## TODO: because of demolition, this won't work
        ## a type reaching target vacancy rates may become less than target

    def schedule_accepted_proposals(self):
        ##TODO: handle demolished buildings in self.demolished_buildings
        years_to_build = self.proposal_set.get_attribute("years")[self.accepted_proposals]
        types = self.proposal_set.get_attribute("type")[self.accepted_proposals]   #building componenet
        units = self.proposal_set.get_attribute("units")[self.accepted_proposals]  #building componenet

        scheduled_year = this_year * ones(len(self.accepted_proposals), dtype="int32") + 1
        unprorated = logical_not(self.proposal_set.get_attribute("prorated")[self.accepted_proposals])
        scheduled_year[unprorated] = this_year + years_to_build[unprorated]

        #create new 'compounded' buildings for each prorated projects, for each year
        prorated = where(self.proposal_set.get_attribute("prorated")[self.accepted_proposals])[0]
        for index in prorated:
            years = arange(2, years_to_build[index]) + this_year
            scheduled_year = concatenate((scheduled_year, years))
            types = concatenate((types, repeat(types[index],years.size)))
            units[index] = round(units[index] / years_to_build[index])  ##TODO: we may want a different prorating function
            units = concatenate((units, units[index] * ones(years.size, dtype="int32")))
            ## append other building attributes

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='buildings_exogeneous',
            table_data={
                    'building_id':max_building_id + arange(1, scheduled_year.size+1, 1),
                    'type': types,
                    'template_id': self.proposal_set.get_attribute("template_id")[self.accepted_proposals],
                    'units': units,
                    'scheduled_year': scheduled_year
                    },
                )

        scheduled_buildings = BuildingDataset(
            in_storage = storage,
            in_table_name = storage_table_name,
            id_name = 'building_id',
            dataset_name = 'building_exogeneous',
            )
        ##TODO: flush dataset


#    def estimate(self, *args, **kargs):
#        agent_set = kargs["agent_set"]
#        data_objects = kargs.get("data_objects", {})
#        data_objects[agent_set.get_dataset_name()] = agent_set
#        estimate_config = kargs.get("estimate_config", {})
#        return LocationChoiceModel.estimate(self, *args, **kargs)
#
#    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
#                              specification_table=None, #agent_set=None,
#                              agents_for_estimation_storage=None,
#                              agents_for_estimation_table=None,
#                              filter_attribute=None, location_id_variable=None,
#                              data_objects={}):
#
#        """similar to prepare_for_estimation method of AgentLocationChoiceModel
#         agent_set is not needed because agents are virtual investors
#        """
#        from urbansim.estimation.estimator import get_specification_for_estimation
#        specification = get_specification_for_estimation(specification_dict,
#                                                          specification_storage,
#                                                          specification_table)
#
#        #def prepare_for_estimate(self, agent_set, specification_dict=None, specification_storage=None,
#                                  #specification_table=None, urbansim_constant=None,
#                                  #location_id_variable=None, dataset_pool=None, **kwargs):
#    #        Return index of buildings that are younger than 'recent_years'+2"""
#        #if location_id_variable:
#            #agent_set.compute_variables(location_id_variable, dataset_pool=dataset_pool)
#        if agents_for_estimation_storage is not None:
#            estimation_set = Dataset(in_storage = agents_for_estimation_storage,
#                                     in_table_name=agents_for_estimation_table,
#                                     id_name='building_id',
#                                     dataset_name='building')
#            if location_id_variable:  #map buildings to proposed development project, proposal_id
#                estimation_set.compute_variables(location_id_variable, resources=Resources(data_objects))
#                # needs to be a primary attribute because of the join method below
#                #estimation_set.add_primary_attribute(estimation_set.get_attribute(location_id_variable), VariableName(location_id_variable).alias())
#            if filter_attribute:
#                estimation_set.compute_variables(filter_attribute, resources=Resources(data_objects))
#                index = where(estimation_set.get_attribute(filter_attribute) > 0)[0]
#                estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)
#        else:
#            raise DataError, 'agents_for_estimation_storage unspecified, which must be a subset of buildings.'
#
#        return (specification, estimation_set)


