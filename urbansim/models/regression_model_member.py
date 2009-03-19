# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import arange, ones, zeros, float32
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults, Resources
from opus_core.regression_model import RegressionModel

class RegressionModelMember(RegressionModel):
    """It sets the RegressionModel as a member of a model group."""

    def __init__(self, group_member, datasets_grouping_attribute,  **kwargs):
        """ 'group_member' is of type ModelGroupMember. 'datasets_grouping_attribute' is attribute of the dataset
        (passed to the 'run' and 'estimate' method) that is used for grouping.
        """
        self.group_member = group_member
        group_member_name = group_member.get_member_name()
        self.group_member.set_agents_grouping_attribute(datasets_grouping_attribute)
        self.model_name = "%s %s" % (group_member_name.capitalize(), self.model_name)
        self.model_short_name = "%s %s" % (group_member_name.capitalize(), self.model_short_name),
        RegressionModel.__init__(self, **kwargs)

    def run(self, specification, coefficients, dataset, index=None, **kwargs):
        if index is None:
            index = arange(dataset.size())
        data_objects = kwargs.get("data_objects",{})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        # filter out agents for this group
        new_index = self.group_member.get_index_of_my_agents(dataset, index, dataset_pool=self.dataset_pool)
        regresult = RegressionModel.run(self,  specification, coefficients, dataset,
                                               index=index[new_index], **kwargs)
        result = zeros(index.size, dtype=float32)
        result[new_index] = regresult
        return result

    def estimate(self, specification, dataset, outcome_attribute, index=None, **kwargs):
        if index is None:
            index = arange(dataset.size())
        data_objects = kwargs.get("data_objects",{})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        # filter out agents for this group
        new_index = self.group_member.get_index_of_my_agents(dataset, index, dataset_pool=self.dataset_pool)
        return RegressionModel.estimate(self,  specification, dataset, outcome_attribute,
                                               index=index[new_index], **kwargs)

    def prepare_for_run(self, add_member_prefix=True, specification_storage=None, specification_table=None, coefficients_storage=None,
                         coefficients_table=None, **kwargs):
        if add_member_prefix:
            specification_table, coefficients_table = \
                self.group_member.add_member_prefix_to_table_names([specification_table, coefficients_table])

        return RegressionModel.prepare_for_run(self, specification_storage=specification_storage, specification_table=specification_table, 
                                               coefficients_storage=coefficients_storage, coefficients_table=coefficients_table, **kwargs)

    def prepare_for_estimate(self, add_member_prefix=True, specification_dict=None, specification_storage=None,
                             specification_table=None, **kwargs):
        if add_member_prefix:
            specification_table = self.group_member.add_member_prefix_to_table_names([specification_table])
        return RegressionModel.prepare_for_estimate(specification_dict=specification_dict, specification_storage=specification_storage,
                                                          specification_table=specification_table, **kwargs)
    
