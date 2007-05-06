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
from opus_core.datasets.dataset import Dataset
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
from opus_core.model import Model

class DevelopmentProjectProposalSamplingModel(Model):

    def __init__(self, proposal_set,
                 sampler="opus_core.samplers.weighted_sampler",
                 weight_string = "exp_ROI = exp(psrc_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                 filter_attribute=None,
                 run_config=None, estimate_config=None,
                 debuglevel=0, dataset_pool=None):
        """
        this model sample project proposals from proposal set weighted by exponentiated ROI
        """
        self.dataset_pool = self.create_dataset_pool(dataset_pool, pool_packages=['psrc_parcel', 'urbansim', 'opus_core'])
        self.dataset_pool.add_datasets_if_not_included({proposal_set.get_dataset_name(): proposal_set})
        self.proposal_set = proposal_set

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
        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')
        target_vacancy.compute_variables(['type_name=target_vacancy.disaggregate(land_use_type.land_use_type_name)', 
                                          'unit_name=target_vacancy.disaggregate(land_use_type.unit_name)'],
                                         dataset_pool=self.dataset_pool)
        current_target_vacancy = DatasetSubset(target_vacancy, index=where(target_vacancy.get_attribute("year")==current_year)[0])

        self.existing_units = {}   #total existing units by land_use type
        self.occupied_units = {}   #total occupied units by land_use type
        self.proposed_units = {}   #total proposed units by land_use type
        self.demolished_units = {} #total (to be) demolished units by land_use type
        self.demolished_buildings = array([], dtype='int32')  #id of buildings to be demolished

        self.accepting_proposals = {}  #whether accepting new proposals, for each land_use type
        self.accepted_proposals = None # accepted proposals

        self.check_vacancy_rates(current_target_vacancy)  #initialize self.accepting_proposal based on current vacancy rate

        while self.accepting_proposal:
            sampled_proposals = probsample_noreplace(self.proposal_set.get_id_attribute(), n, prob_array=self.weight,
                                                     exclude_index=None, return_indices=False)
            self.consider_proposals(sampled_proposals,
                                    target_vacancy_rates
                                   )

#        schedule_development_projects = self.schedule_accepted_proposals()
        return self.accepted_proposals  #schedule_development_projects

    def check_vacancy_rates(self, target_vacancy):
        for index in arange(target_vacancy.size()):
            type_id = target_vacancy_rates.get_attribute_by_index("land_use_type_id", index)
            type_name = target_vacancy_rates.get_attribute_by_index("type_name", index)            
            unit_name = target_vacancy.get_attribute_by_index("unit_name", index)  #vacancy by type, could be residential, non-residential, or by building_type
            
            target = target_vacancy.get_attribute_by_index("target_vacancy_rate", index)
            parcels = self.dataset_pool.get_dataset("parcel")
            is_matched_type = parcels.get_attribute("land_use_type_id") == type_id
            existing_units = zeros(parcels.size(), dtype="int32")
            existing_units[is_with_matched_type] = parcels.get_attribute(unit_name)[is_with_matched_type]
            parcels.compute_variables("psrc_parcel.parcel.occupied_units", dataset_pool=self.dataset_pool)
            occupied_units = parcels.get_attribute("occupied_units")

            self.existing_units[type_id] = existing_units.sum()
            self.occupied_units[type_id] = occupied_units.sum()
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            vr = (self.existing_units[type_id] - self.occupied_units[type_id]) / float(self.existing_units[type_id])
            if vr < target:
                self.accepting_proposals[type_id] = True
            else:
                self.accepting_proposals[type_id] = False

    def consider_proposals(self, proposals, target_vacancy_rates):
        parcels = self.dataset_pool.get_dataset("parcel")
        building_site = parcels.get_attribute("parcel_id")
        proposal_indexes = self.proposal_set.get_id_index(proposals)
        is_proposal_rejected = zeros(proposals.size(), dtype=bool8)
        proposal_site = self.proposal_set.get_attribute_by_index("parcel_id", proposal_indexes)
        #proposal_type = self.proposal_set.get_attribute_by_index("unit_type", proposal_indexes)
#        pro_rated = self.proposal_set.get_attribute_by_index("pro_rated", proposal_indexes) #whether the project is pro_rated
#        years = self.proposal_set.get_attribute_by_index("years", proposal_indexes)         #how many years it take to build
#        proposal_construction_type = self.proposal_set.get_attribute_by_index("construction_type", proposal_indexes)  #redevelopment or addition

        existing_units = {}
        proposal_units = {}
        for type_id in target_vacancy_rates.get_attribute("land_use_type_id"):  #iterate all unit types, not necessary from vacancy_rates table
            #occupied_units[type_id] = parcels.get_attribute("occupied_%s" % )
            existing_units[type_id] = parcels.get_attribute(type_id)
            proposal_units[type_id] = self.proposal_set.get_attribute_by_index(type_id, proposal_indexes)

        for proposal_index in proposal_indexes:  # consider 1 proposed project at a time
            if not sometrue(array(self.accepting_proposals.values())):
                # if none of the types is accepting_proposals, exit
                # this is put in the loop to check if the last accepted proposal has sufficed
                # the target vacancy rates for all types
                return

            sum_units = 0
            for this_type in self.accepting_proposals.keys():
                # if this_type is not accepting proposal, but this proposal have non-zero units of this_type
                # reject this proposal
                sum_units += proposal_units[this_type][proposal_index]
                if not self.accepting_proposals[this_type] and proposal_units[this_type] > 0:
                    is_proposal_rejected[proposal_index] = 1

            if sum_units == 0:
                # if there aren't any meaningful units, reject this project
                is_proposal_rejected[proposal_index] = 1

            # try next if this proposal has been rejected
            if is_proposal_rejected[proposal_index]:
                continue

            this_site = proposal_site[proposal_index]
            #this_type = proposal_type[proposal_index]
            if proposal_construction_type[proposal_index] == 'R':  #if it's a redevelopment project,demolish existing buildings of this site
                affected_building = where(building_site==this_site)[0]
                self.demolished_buildings = concatenate((self.demolished_buildings, affected_building))
                for type in existing_units.keys():
                    self.demolished_units[type] += existing_units[type][affected_building].sum() #demolish affected buildings
                    #existing_units[affected_building] = 0
                    #moving_agents += occupied_units[affected_building].sum()
                    #occupied_units[affected_building] = 0
            for type in target_vacancy_rates.get_attribute("type_name"): #
                if pro_rate[proposal_index]:
                    self.proposed_units[type] += round(proposal_units[type][proposal_index] / years[proposal_index])
                    #TODO: handle pro-rated projects
                else:
                    self.proposed_units[type] += proposal_units[type][proposal_index]
                units_stock = self.existing_units[type] - self.demolished_units[type] + self.proposed_units[type]
                vr = (units_stock - self.occupied_units[type]) / float(units_stock)
                if vr >= target_vacancy_rates[target_vacancy_rates.types==type]:
                    self.accepting_proposals[type] = False
                else:
                    self.accepting_proposals[type] = True

            # proposal accepted
            self.accepted_proposals.append(proposal_index)
            # reject all pending proposals for this site
            is_proposal_rejected[proposal_site == this_site] = 1
            # don't consider proposed projects for this site in the future
            self.weight[self.proposal_set.get_attribute("parcel_id")==this_site] = 0.0

        ## TODO: because of demolition, this won't work
        ## a type reaching target vacancy rates may become less than target
        for type, accepting_proposal in self.accepting_proposals.iteritems():
            if not accepting_proposal:
                # if a type isn't accepting proposal, don't propose any projects of this type in the future
                self.weight[self.proposal_set.get_attribute(type_name)>0] = 0.0

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
        storage._write_dataset(
            {'buildings_exogeneous':{
                    'building_id':max_building_id + arange(1, scheduled_year.size+1, 1),
                    'type': types,
                    'template_id': self.proposal_set.get_attribute("template_id")[self.accepted_proposals],
                    'units': units,
                    'scheduled_year': scheduled_year
                    },
                })

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


