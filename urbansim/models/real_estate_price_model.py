#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
from opus_core.regression_model_with_addition_initial_residuals import RegressionModelWithAdditionInitialResiduals
from numpy import exp, arange, logical_and, zeros, where, array, float32
import re

class RealEstatePriceModel(RegressionModelWithAdditionInitialResiduals):
    """Predicts/estimates a dataset attribute of real estate price using a regression model.
    It can be configured for example for a building dataset or a gridcell dataset.
    """

    model_name = "Real Estate Price Model"
    model_short_name = "REPM"

    def __init__(self, regression_procedure="opus_core.linear_regression",
                 filter_attribute=None,
                 submodel_string="building_type_id",
                 outcome_attribute = "unit_price",
                 run_config=None,
                 estimate_config=None,
                 debuglevel=0, dataset_pool=None):
        self.filter_attribute = filter_attribute
        RegressionModelWithAdditionInitialResiduals.__init__(self,
                                 regression_procedure=regression_procedure,
                                 submodel_string=submodel_string,
                                 outcome_attribute = outcome_attribute,
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
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, dataset_pool=self.dataset_pool,
                                               resources=res)
        outcome = RegressionModelWithAdditionInitialResiduals.run(self, specification, coefficients, dataset,
                                         index, chunk_specification,
                                         run_config=run_config, debuglevel=debuglevel)
        if (outcome == None) or (outcome.size <= 0):
            return outcome
        if index == None:
            index = arange(dataset.size())
        if re.search("^ln_", self.outcome_attribute.get_alias()): # if the outcome attr. name starts with 'ln_'
                                                      # the results will be exponentiated.
            outcome_attribute_name = self.outcome_attribute.get_alias()[3:len(self.outcome_attribute.get_alias())]
            outcome = exp(outcome)
        else:
            outcome_attribute_name = self.outcome_attribute.get_alias()
        if outcome_attribute_name in dataset.get_known_attribute_names():
            values = dataset.get_attribute(outcome_attribute_name).copy()
            dataset.delete_one_attribute(outcome_attribute_name)
        else:
            values = zeros(dataset.size(), float32)
        values[index] = outcome
        dataset.add_primary_attribute(name=outcome_attribute_name, data=values)
        self.correct_infinite_values(dataset, outcome_attribute_name, clip_all_larger_values=True)
        return outcome

    def estimate(self, specification, dataset, outcome_attribute="unit_price", index = None,
                        procedure="opus_core.estimate_linear_regression", data_objects=None,
                        estimate_config=None,  debuglevel=0):
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, dataset_pool=self.dataset_pool,
                                               resources=res)
        return RegressionModelWithAdditionInitialResiduals.estimate(self, specification, dataset, outcome_attribute, index, procedure,
                                     estimate_config=estimate_config, debuglevel=debuglevel)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, dataset=None,
                              filter_variable="unit_price",
                              threshold=0):
        from urbansim.estimation.estimator import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        index = None
        if dataset is not None and filter_variable is not None:
            dataset.compute_variables(filter_variable)
            index = where(dataset.get_attribute(filter_variable) >= threshold)[0]
        return (specification, index)
