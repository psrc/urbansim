# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from urbansim.models.location_choice_model import LocationChoiceModel
from opus_core.variables.variable_name import VariableName
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.datasets.development_project_dataset import DevelopmentProjectCreator
from numpy import zeros, arange, where, ones, logical_and, int32
from numpy import take, argsort, array, int8, bool8, ndarray
from opus_core.logger import logger

class DevelopmentProjectLocationChoiceModel(LocationChoiceModel):

    model_name = "Development Project Location Choice Model"
    model_short_name = "DPLCM"

    def __init__(self, location_set, project_type, units,
                 developable_maximum_unit_variable_full_name,
                 developable_minimum_unit_variable_full_name=None,
                 model_name=None, **kargs):
        """
        'project_type' is a string such as 'Residential', or 'Commercial'.
        """
        self.project_type = project_type
        self.units = units
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = "%s %s" % (self.project_type, self.model_name)
        self.model_short_name = "%s %s" % (self.project_type[:3], self.model_short_name)

        self.developable_maximum_unit_full_name = developable_maximum_unit_variable_full_name
        self.developable_maximum_unit_short_name = VariableName(self.developable_maximum_unit_full_name).get_alias()
        self.developable_minimum_unit_full_name = developable_minimum_unit_variable_full_name
        if self.developable_minimum_unit_full_name is not None:
            self.developable_minimum_unit_short_name = VariableName(self.developable_minimum_unit_full_name).get_alias()
        else:
            self.developable_minimum_unit_short_name = None
        LocationChoiceModel.__init__(self, location_set=location_set, **kargs)

    def run(self, *args, **kargs):
        """disable filter for simulation, since it's been handled by get_weights_for_sampling_locations method"""
        self.filter = None
        agent_set = kargs["agent_set"]
        if agent_set is None:
            logger.log_status("No development projects for this model")
            return None
        logger.log_status("project size: %d" % (agent_set.get_attribute(agent_set.get_attribute_name()).sum()))
        LocationChoiceModel.run(self, *args, **kargs)

    def get_sampling_weights(self, config, agent_set=None, agents_index=None, **kwargs):
        
        if isinstance(self.capacity, ndarray):
            where_developable = where(self.capacity)[0]
        else:
            where_developable = arange(self.choice_set.size())
        weight_array = ones((agents_index.size, where_developable.size), dtype=bool)
        if 'estimate' in config and config['estimate']:
            return weight_array
        varlist = [self.developable_maximum_unit_full_name]
        if self.developable_minimum_unit_full_name is not None:
            varlist.append(self.developable_minimum_unit_full_name)
        self.choice_set.compute_variables(varlist, dataset_pool = self.dataset_pool)

        max_capacity = self.choice_set.get_attribute_by_index(self.developable_maximum_unit_short_name, where_developable)
        if self.developable_minimum_unit_full_name is not None:
            min_capacity = self.choice_set.get_attribute_by_index(self.developable_minimum_unit_short_name, where_developable)
        else:
            min_capacity = zeros(max_capacity.size)

        if max_capacity.sum() == 0:
            raise RuntimeError("There are no choices with any capacity for %s projects" % agent_set.what)

        #how many projects fit in each developable location
        proposed_project_sizes = agent_set.get_attribute_by_index(agent_set.get_attribute_name(),
                                                                  agents_index)
        for iagent in arange(agents_index.size):
            proposed_project_size = proposed_project_sizes[iagent]
            weight_array[iagent, :] = \
                        logical_and(min_capacity <= proposed_project_size,
                                    proposed_project_size <= max_capacity)
#            weight_array[iagent, :] = weight_array[iagent, :] * \
#                        (max_capacity - min_capacity) / proposed_project_size

        # for memory reasons, discard columns that have only zeros
        logger.log_status("shape of weight_array: ", weight_array.shape)
        keep = where(weight_array.sum(axis=0, dtype=int32))[0]
        where_developable = where_developable[keep]
#        del weight_array
#        collect()
#        weight_array = (ones((agents_index.size,keep.size), dtype=int8)).astype(bool8)
#
#        max_capacity = self.choice_set.get_attribute_by_index(self.developable_maximum_unit_short_name,
#                                                              where_developable)
#        min_capacity = self.choice_set.get_attribute_by_index(self.developable_minimum_unit_short_name,
#                                                              where_developable)
#
#        #how many projects fit in each developable location
#        for iagent in arange(agents_index.size):
#            proposed_project_size = proposed_project_sizes[iagent]
#            weight_array[iagent, :] = \
#                    logical_and(min_capacity <= proposed_project_size,
#                                proposed_project_size <= max_capacity)

#        wk = where(keep)[0]
        weight_array = take(weight_array, keep, axis=1)
        if where_developable.size <= 0:
            logger().log_warning("No developable locations available.")
            
        self.filter_index = where_developable  ##pass filter to apply_filter

        return weight_array

#    def get_probability_array_for_estimation_sampling_locations(self, location_set=None, \
#                    agent_set=None, agents_index=None, data_objects=None, resources=None):
#        self.capacity = location_set.get_attribute(resources[
#            "estimation_capacity_string"]).astype(float32)
#        return self.get_probability_array_for_sampling_locations(location_set, agent_set, \
#                agents_index, data_objects, resources)

    def preprocess_projects(self, agent_set, agents_index=None, data_objects=None):
        """Split projects that don't find enough choices to smaller ones (of average size).
        """
        resources=Resources(data_objects)
        resources.merge({"debug":self.debug})

        self.choice_set.compute_variables([self.developable_maximum_unit_full_name,
                                           self.developable_minimum_unit_full_name],
                                          resources=resources)

        max_capacity = self.choice_set.get_attribute(self.developable_maximum_unit_short_name)
        min_capacity = self.choice_set.get_attribute(self.developable_minimum_unit_short_name)

        self.set_choice_set_size()
        nchoices = self.get_choice_set_size()
        project_average_size = agent_set.get_attribute(agent_set.get_attribute_name()).mean()
        add_projects = 0
        remove_projects = 0

        if agents_index == None:
            agents_index=arange(agent_set.size())
        # order agents by size
        ordered_indices = argsort(-1*agent_set.get_attribute_by_index(agent_set.get_attribute_name(), agents_index))
        improvement_values=[]
        projects_ids = agent_set.get_id_attribute()[agents_index].tolist()
        #   how many projects fit in each developable location
        project_sizes = agent_set.get_attribute_by_index(agent_set.get_attribute_name(), agents_index)
        for iagent in ordered_indices:
            project_size = project_sizes[iagent]
            capacity =  logical_and(project_size > min_capacity, (max_capacity / project_size) > 0)
            if where(capacity)[0].size < nchoices: # not enough choices found
                nsplitted = int(project_size/project_average_size)
                add_projects += nsplitted
                remove_projects+=1
                projects_ids.remove(agent_set.get_id_attribute()[agents_index[iagent]])
                improvement_values = improvement_values + \
                    nsplitted*[agent_set.get_attribute_by_index("improvement_value", agents_index[iagent])]
            else:
                break # we can break here, since the projects are sorted by size

        if remove_projects > 0:
            agent_set.remove_elements(agents_index[ordered_indices[0:remove_projects]])
            agents_index = agent_set.get_id_index(projects_ids)

        if add_projects > 0:
            max_id = agent_set.get_attribute(agent_set.get_id_name()[0]).max()
            ids = arange(max_id+1,max_id+1+add_projects)
            agent_set.add_elements(data={"project_id":ids,
                self.location_set.get_id_name()[0]:zeros((add_projects,)),
                "improvement_value":array(improvement_values),
                agent_set.get_attribute_name(): project_average_size*ones((add_projects,))},
                require_all_attributes=False)
            agents_index = agent_set.get_id_index(projects_ids + ids.tolist())

    def get_agents_order(self, movers):
        """Sort in descending order according to the size in order to locate larger agents first.
        """
        return argsort(movers.get_attribute(movers.parent.get_attribute_name()))[arange(movers.size()-1,-1,-1)]

    def determine_capacity(self, capacity_string=None, agent_set=None, **kwargs):
        capacity = LocationChoiceModel.determine_capacity(self, capacity_string=capacity_string, agent_set=agent_set, **kwargs)
        # subtract locations taken in previous chunks
        taken_locations = self.choice_set.sum_over_ids(agent_set.get_attribute(self.choice_set.get_id_name()[0]),
                                                       ones((agent_set.size(),)))
        return capacity - taken_locations

    def apply_filter(self, filter, agent_set, agents_index, submodel=-2):
        """ apply filter comparing to mean project size by submodel instead of 0, by shifting self.filter
        """
        project_size_filter = None
        if (filter is not None):
            if isinstance(filter, dict):
                submodel_filter = filter[submodel]
            else:
                submodel_filter = filter

            mean_project_size = agent_set.get_attribute(agent_set.get_attribute_name())[agents_index].mean()

            if isinstance(submodel_filter, str):
                resources = Resources({"debug":self.debug})
                self.choice_set.compute_variables([submodel_filter], dataset_pool=self.dataset_pool, resources=resources)
                filter_name = VariableName(submodel_filter)
                project_size_filter = self.choice_set.get_attribute(filter_name.get_alias()) - mean_project_size
            else:
                project_size_filter = submodel_filter - mean_project_size
                
        return LocationChoiceModel.apply_filter(self, project_size_filter, 
                                                        agent_set=agent_set, 
                                                        agents_index=agents_index, 
                                                        submodel=submodel)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None,
                              events_for_estimation_storage=None,
                              events_for_estimation_table=None, urbansim_constant=None, base_year=0,
                              categories=None):

        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        projects = None
        # create agents for estimation
        if events_for_estimation_storage is not None:
            event_set = DevelopmentEventDataset(in_storage = events_for_estimation_storage,
                                            in_table_name= events_for_estimation_table)
            event_set.remove_non_recent_data(base_year, urbansim_constant['recent_years'])
            projects = DevelopmentProjectCreator().create_projects_from_history(
                                               event_set, self.project_type,
                                               self.units, categories)
        return (specification, projects)
    
    def prepare_for_run(self, *args, **kwargs):
        spec, coef, dummy = LocationChoiceModel.prepare_for_run(self, *args, **kwargs)
        return (spec, coef)