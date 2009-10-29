# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.location_choice_model import LocationChoiceModel
from numpy import arange, int32, float32
from numpy import array, int8, bool8, concatenate, where, ndarray
from opus_core.logger import logger
from randstad.datasets.landuse_developments import create_landuse_developments_from_history
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset

class LandUseDevelopmentLocationChoiceModel(LocationChoiceModel):

    def __init__(self, location_set, opus_package, model_name, **kargs):
        """

        """

        self.opus_package = opus_package
        self.model_name = model_name
        self.max_runs = 100
        LocationChoiceModel.__init__(self, location_set=location_set, **kargs)

    def settings(self):
        return {"agent":"landuse_development",
                "name":"Landuse Development Location Choice Model",
                "short_name":"LUDLCM" }

    def run(self, specification, coefficients, agent_set,
            agents_index=None, *args, **kargs):

        if agent_set is None:
            logger.log_status('No developments need to be allocated')
            return

        if agents_index is None:
            agents_index = arange(agent_set.size())
        if not isinstance(agents_index, ndarray):
            try:
                agents_index = array(agents_index)
            except:
                raise TypeError, "Argument agents_index is of wrong type (numpy array or list allowed.)"
        id_name = self.choice_set.get_id_name()[0]
        unplaced = arange(agents_index.size)
        for run in range(self.max_runs):
            choices = LocationChoiceModel.run(self, specification, coefficients, agent_set,
                                              agents_index[unplaced], *args, **kargs)
            if run == 0:
                all_choices=choices
            else:
                all_choices[unplaced]=choices

            from opus_core.sampling_toolbox import find_duplicates
            unplaced = where(find_duplicates(all_choices))[0]
            if unplaced.size <= 0:
                break
            agent_set.set_values_of_one_attribute(id_name, -1, agents_index[unplaced])
        return all_choices

        LocationChoiceModel.run(self, *args, **kargs)

    def get_agents_order(self, agents):
        """Sort landuse development agents according to its priority order
        """
        priority_attribute = 'development_type_id'
        priority_order = [101, 102, 103, 104, 105, 33, 34, 36]
        index = array([], dtype='int32')
        for order_id in priority_order:
            index = concatenate((index, where(agents.get_attribute(priority_attribute)==order_id)[0]))
        return index

#    def determine_capacity(self, agent_set, agents_index, data_objects=None):
#        capacity = LocationChoiceModel.determine_capacity(self, agent_set, agents_index, data_objects)
#        # subtract locations taken in previous chunks
#        taken_locations = self.choice_set.sum_over_ids(agent_set.get_attribute(self.choice_set.get_id_name()[0]), \
#                                                       ones((agent_set.size(),)))
#        return capacity - taken_locations

    def apply_filter(self, filter, submodel=-2):
        """ apply filter
        """
        if submodel != -2:
            filter = filter + "_for_development_type_" + str(submodel)

        return LocationChoiceModel.apply_filter(self, filter, submodel=submodel)

    def prepare_for_estimate(self,specification_dict = None,
                                  specification_storage=None,
                                  specification_table=None,
                                  events_for_estimation_storage=None,
                                  events_for_estimation_table=None):

        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        development = None
        # create agents for estimation
        if events_for_estimation_storage is not None:
            event_set = DevelopmentEventDataset(in_storage = events_for_estimation_storage,
                                            in_table_name= events_for_estimation_table)
            development = create_landuse_developments_from_history(event_set)
        return (specification, development)