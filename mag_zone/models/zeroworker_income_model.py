
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, exp, arange, zeros, where
from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from opus_core.logger import logger
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.misc import unique
from opus_core.simulation_state import SimulationState

class ZeroworkerIncomeModel(RegressionModel):
    """
    """
    model_name = "Zeroworker Income Model"
    model_short_name = "ZIM"

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
        zeroworkers = dataset.compute_variables('household.workers == 0')
        index_zeroworker = where(zeroworkers)[0]
        #Run regression model
        incomes = RegressionModel.run(self, specification, coefficients, dataset, index_zeroworker, chunk_specification,
                                     run_config=run_config, debuglevel=debuglevel)
        dataset.set_values_of_one_attribute("income", incomes, index_zeroworker)
        #Bump up all negative incomes to zero
        negative_income = dataset.compute_variables('household.income < 0')
        index_neg_inc = where(negative_income==1)[0]
        if index_neg_inc.size > 0:
            dataset.modify_attribute('income', zeros(index_neg_inc.size, dtype="int32"), index_neg_inc)

        return

