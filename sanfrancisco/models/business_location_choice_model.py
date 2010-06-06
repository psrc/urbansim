# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from urbansim.models.location_choice_model import LocationChoiceModel
from numpy import arange, where, ones
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset

class BusinessLocationChoiceModel(LocationChoiceModel):

    model_name = "Business Location Choice Model"
    model_short_name = "BLCM"

    def __init__(self, location_set, model_name=None, short_name=None, **kargs):
        if model_name is not None:
            self.model_name = model_name
        if short_name is not None:
            self.model_short_name = short_name

        LocationChoiceModel.__init__(self, location_set=location_set, **kargs)

#    def run(self, *args, **kargs):
#        """disable filter for simulation, since it's been handled by get_weights_for_sampling_locations method"""
#        self.filter = None
#        agent_set = kargs["agent_set"]
#        if agent_set is None:
#            logger.log_status("No agents for this model")
#            return None
#        LocationChoiceModel.run(self, *args, **kargs)
#
#    def get_weights_for_sampling_locations(self, agent_set, agents_index):
#        
#        where_available = where(self.capacity)[0]
#        weight_array = (ones((agents_index.size, where_available.size), dtype=int8)).astype(bool8)
#
#        building_sqft = self.choice_set.get_attribute_by_index('building_sqft', where_available)
##
#        proposed_agent_sizes = agent_set.get_attribute_by_index('sqft', agents_index)
#        proposed_agent_use_ids = agent_set.get_attribute_by_index('sector_id', agents_index)
#
#        for iagent in arange(agents_index.size):
#            proposed_agent_size = proposed_agent_sizes[iagent]
#            proposed_agent_use_id = proposed_agent_use_ids[iagent]
#            weight_array[iagent, :] = \
#                        building_sqft >= proposed_agent_size
#                        #logical_and(building_sqft >= proposed_agent_size,
#                                    #sector_id == proposed_agent_use_id)
#
#        # for memory reasons, discard columns that have only zeros
#        logger.log_status("shape of weight_array: ", weight_array.shape)
#        keep = where(weight_array.sum(axis=0, dtype=int32))[0]
#        where_available = where_available[keep]
#
#        weight_array = take(weight_array, keep, axis=1)
#        if where_available.size <= 0:
#            logger().log_warning("No developable locations available.")
#        return (weight_array, where_available)


#    def apply_filter(self, filter, agent_set=None, agents_index=None, submodel=-2):
#        """ apply filter comparing to mean size by submodel instead of 0, by shifting self.filter
#        """
#        
#        (numpy.bitwise_and(sanfrancisco.building.activity_constraint, 2**(SUBMODEL-1)) > 0) * \
#        
#        ( building.sqft > ( numpy.sum(business.sqft*business.activity_id==SUBMODEL)/float(numpy.sum(business.sqft * business.activity_id==SUBMODEL)) ))
#        
##        size_filter = None
##        if (filter is not None):
##            if isinstance(filter, dict):
##                submodel_filter = filter[submodel]
##            else:
##                submodel_filter = filter
##
##            mean_size = agent_set.get_attribute("sqft")[agents_index].mean()
##            if isinstance(submodel_filter, str):
##                resources = Resources({"debug":self.debug})
##                self.choice_set.compute_variables([submodel_filter, self.submodel_string],
##                                                  dataset_pool=self.dataset_pool, resources=resources)
##                filter_name = VariableName(submodel_filter)
##                submodel_string = VariableName(self.submodel_string)
##                size_filter = self.choice_set.get_attribute(filter_name.alias()) - mean_size
##                if submodel != -2:
##                    size_filter = size_filter * (self.choice_set.get_attribute(submodel_string.alias())==submodel)
##            else:
##                size_filter = submodel_filter - mean_size
##            filter_index = where(size_filter>0)[0]
#            
#        return LocationChoiceModel.apply_filter(self, filter_index, 
#                                                agent_set=agent_set, 
#                                                agents_index=agents_index, 
#                                                submodel=submodel)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, agent_set=None,
                              agents_for_estimation_storage=None,
                              agents_for_estimation_table=None, join_datasets=False,
                              index_to_unplace=None, portion_to_unplace=1.0,
                              agent_filter=None,
                              data_objects={}):
        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        if (agent_set is not None) and (index_to_unplace is not None):
            if self.location_id_string is not None:
                agent_set.compute_variables(self.location_id_string, resources=Resources(data_objects))
            if portion_to_unplace < 1:
                unplace_size = int(portion_to_unplace*index_to_unplace.size)
                end_index_to_unplace = sample_noreplace(index_to_unplace, unplace_size)
            else:
                end_index_to_unplace = index_to_unplace
            logger.log_status("Unplace " + str(end_index_to_unplace.size) + " agents.")
            agent_set.modify_attribute(self.choice_set.get_id_name()[0],
                                        -1*ones(end_index_to_unplace.size), end_index_to_unplace)
        # create agents for estimation
        if agents_for_estimation_storage is not None:
            estimation_set = Dataset(in_storage = agents_for_estimation_storage,
                                      in_table_name=agents_for_estimation_table,
                                      id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
            if agent_filter is not None:
                estimation_set.compute_variables(agent_filter, resources=Resources(data_objects))
                index = where(estimation_set.get_attribute(agent_filter) > 0)[0]
                estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)

            if join_datasets:
                agent_set.join_by_rows(estimation_set, require_all_attributes=False,
                                    change_ids_if_not_unique=True)
                index = arange(agent_set.size()-estimation_set.size(),agent_set.size())
            else:
                index = agent_set.get_id_index(estimation_set.get_id_attribute())
        else:
            index = arange(agent_set.size())
        return (specification, index)