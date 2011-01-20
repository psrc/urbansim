# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.building_location_choice_model import BuildingLocationChoiceModel as UrbansimBuildingLocationChoiceModel
from numpy import where, arange, zeros
from numpy import logical_or, logical_not
from opus_core.variables.variable_name import VariableName
from opus_core.resources import Resources
from opus_core.datasets.dataset import Dataset

class BuildingLocationChoiceModel(UrbansimBuildingLocationChoiceModel):

#    def get_weights_for_sampling_locations(self, agent_set, agents_index, data_objects=None):
#        where_developable = where(self.apply_filter(self.filter, None, agent_set, agents_index, data_objects=data_objects))[0]
#        weight_array = ones((where_developable.size), dtype=int8) #.astype(bool8)
#        return (weight_array, where_developable)

    def get_weights_for_sampling_locations_for_estimation(self, agent_set, agents_index):
        if self.run_config.get("agent_units_string", None): # needs to be corrected
            agent_set.compute_variables(self.run_config["agent_units_string"], dataset_pool=self.dataset_pool)

        return self.get_weights_for_sampling_locations(agent_set, agents_index)

    def prepare_for_estimate(self, add_member_prefix=True,
                             specification_dict=None,
                             specification_storage=None,
                             specification_table=None,
                             building_set=None,
                             buildings_for_estimation_storage=None,
                             buildings_for_estimation_table=None,
                             constants=None, base_year=0,
                             building_categories=None,
                             location_id_variable=None,
                             join_datasets=False,
                             data_objects=None, **kwargs):
#        buildings = None

        if (building_set is not None):
            if location_id_variable is not None:
                building_set.compute_variables(location_id_variable, resources=Resources(data_objects))

        # create agents for estimation
        if buildings_for_estimation_storage is not None:
            estimation_set = Dataset(in_storage=buildings_for_estimation_storage,
                                     in_table_name=buildings_for_estimation_table,
                                     id_name=building_set.get_id_name(),
                                     dataset_name=building_set.get_dataset_name())
            if location_id_variable:
                estimation_set.compute_variables(location_id_variable,
                                                 resources=Resources(data_objects))
                # needs to be a primary attribute because of the join method below
                estimation_set.add_primary_attribute(estimation_set.get_attribute(location_id_variable),
                                                     VariableName(location_id_variable).alias())

            years = estimation_set.get_attribute("scheduled_year")
            recent_years = constants['recent_years']
            indicator = zeros(estimation_set.size(), dtype="int32")
            for year in range(base_year-recent_years, base_year+1):
                indicator = logical_or(indicator, years==year)
            idx = where(logical_not(indicator))[0]
            estimation_set.remove_elements(idx)

            #if filter:
                #estimation_set.compute_variables(filter, resources=Resources(data_objects))
                #index = where(estimation_set.get_attribute(filter) > 0)[0]
                #estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)

            if join_datasets:
                building_set.join_by_rows(estimation_set,
                                          require_all_attributes=False,
                                          change_ids_if_not_unique=True)
                index = arange(building_set.size()-estimation_set.size(), building_set.size())
            else:
                index = building_set.get_id_index(estimation_set.get_id_attribute())
        else:
            if building_set is not None:
                index = arange(building_set.size())
            else:
                index = None

        if add_member_prefix:
            specification_table = self.group_member.add_member_prefix_to_table_names([specification_table])

        from opus_core.model import get_specification_for_estimation
        #from urbansim.functions import compute_supply_and_add_to_location_set
        specification = get_specification_for_estimation(specification_dict,
                                                         specification_storage,
                                                         specification_table)

        #specification, dummy = AgentLocationChoiceModelMember.prepare_for_estimate(self, add_member_prefix,
                                                               #specification_dict, specification_storage,
                                                               #specification_table,
                                                               #location_id_variable=location_id_variable,
                                                               #data_objects=data_objects, **kwargs)
        return (specification, index)