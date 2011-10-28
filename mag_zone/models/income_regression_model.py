
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, exp, arange, zeros, where
from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from opus_core.logger import logger

class IncomeRegressionModel(RegressionModel):
    """
    """
    model_name = "Income Regression Model"
    model_short_name = "IRM"

    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string=None, 
                 outcome_attribute=None,
                 run_config=None, 
                 estimate_config=None, 
                 debuglevel=0, dataset_pool=None):
        self.filter_attribute = filter_attribute
        if outcome_attribute is not None:
            self.outcome_attribute = outcome_attribute
        
        RegressionModel.__init__(self, 
                                 regression_procedure=regression_procedure, 
                                 submodel_string=submodel_string, 
                                 run_config=run_config, 
                                 estimate_config=estimate_config, 
                                 debuglevel=debuglevel, dataset_pool=dataset_pool)

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None, 
             data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
                                               dataset_pool=self.dataset_pool, resources=res)
        incomes = RegressionModel.run(self, specification, coefficients, dataset, index, chunk_specification,
                                     run_config=run_config, debuglevel=debuglevel)
        if (incomes == None) or (incomes.size <=0):
            return incomes
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("income", incomes, index)

        #Bump up all negative incomes to zero
        negative_income = dataset.compute_variables('household.income < 0')
        index_neg_inc = where(negative_income==1)[0]
        if index_neg_inc.size > 0:
            dataset.modify_attribute('income', zeros(index_neg_inc.size, dtype="int32"), index_neg_inc)

        #Now bump up all incomes depending on civ_emp ratio?

        return

    def prepare_for_estimate(self, dataset=None, dataset_for_estimation_storage=None, dataset_for_estimation_table=None, join_datasets=False, **kwargs):
        from opus_core.model import get_specification_for_estimation
        from opus_core.datasets.dataset import Dataset
        spec = get_specification_for_estimation(**kwargs)
        if (dataset_for_estimation_storage is not None) and (dataset_for_estimation_table is not None):
            estimation_set = Dataset(in_storage = dataset_for_estimation_storage,
                                      in_table_name=dataset_for_estimation_table,
                                      id_name=dataset.get_id_name(), dataset_name=dataset.get_dataset_name())
            if join_datasets:
                dataset.join_by_rows(estimation_set, require_all_attributes=False,
                                    change_ids_if_not_unique=True)
                index = arange(dataset.size()-estimation_set.size(),dataset.size())
            else:
                index = dataset.get_id_index(estimation_set.get_id_attribute())
        else:
                index = None
        return (spec, index)


    # def prepare_for_estimate(self, dataset=None, dataset_for_estimation_storage=None, dataset_for_estimation_table=None, join_datasets=False, dataset_filter=None, filter_threshold=0, **kwargs):
        # from opus_core.model import get_specification_for_estimation
        # from opus_core.datasets.dataset import Dataset
        # spec = get_specification_for_estimation(**kwargs)
        # if (dataset_for_estimation_storage is not None) and (dataset_for_estimation_table is not None):
            # estimation_set = Dataset(in_storage = dataset_for_estimation_storage,
                                      # in_table_name=dataset_for_estimation_table,
                                      # id_name=dataset.get_id_name(), dataset_name=dataset.get_dataset_name())
            # if dataset_filter is not None:
                # filter_values = dataset.compute_variables([dataset_filter], dataset_pool=self.dataset_pool)
                # index = where(filter_values > filter_threshold)[0]
                # estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)
            # if join_datasets:
                # dataset.join_by_rows(estimation_set, require_all_attributes=False,
                                    # change_ids_if_not_unique=True)
                # index = arange(dataset.size()-estimation_set.size(),dataset.size())
            # else:
                # index = dataset.get_id_index(estimation_set.get_id_attribute())
        # else:
            # if (dataset is not None) and (dataset_filter is not None):
                # filter_values = dataset.compute_variables([dataset_filter], dataset_pool=self.dataset_pool)
                # index = where(filter_values > filter_threshold)[0]
            # else:
                # index = None
        # return (spec, index)