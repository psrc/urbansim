# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from urbansim.models.real_estate_price_model import RealEstatePriceModel
from opus_core.models.regression_model_with_addition_initial_residuals import RegressionModelWithAdditionInitialResiduals
from numpy import exp, arange, logical_and, zeros, where, array, float32
from scipy.stats.distributions import norm
import re

class EstablishmentEvolutionModel(RealEstatePriceModel, RegressionModelWithAdditionInitialResiduals):
    """Predicts/estimates a dataset attribute of real estate price using a regression model.
    It can be configured for example for a building dataset or a gridcell dataset.
    """

    model_name = "Establishment Evolution Model"
    model_short_name = "EEM"

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None,
            years = 4,
            data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, dataset_pool=self.dataset_pool,
                                               resources=res)
        init_outcome = RegressionModelWithAdditionInitialResiduals.run(self, specification, coefficients, dataset,
                                         index, chunk_specification=chunk_specification,
                                         run_config=run_config, debuglevel=debuglevel)

        initial_error_name = "_init_error_%s" % self.outcome_attribute.get_alias()
        initial_error = dataset[initial_error_name][index]
        mean = init_outcome - initial_error

        rmse = dataset.compute_variables("paris.establishment.rmse_ln_emp_ratio")
        _epsilon = norm.rvs(location=0, scale=rmse) / years  # convert lump prediction to annual prediction
        _epsilon_name = "_epsilon_%s" % self.outcome_attribute.get_alias()

        if _epsilon_name not in dataset.get_known_attribute_names():
            dataset.add_primary_attribute(name=_epsilon_name, data=zeros(dataset.size(), dtype="float32"))
        dataset.set_values_of_one_attribute(_epsilon_name, _epsilon, index)
        outcome = mean + _epsilon[index]

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
            values = zeros(dataset.size(), dtype='f')

        values[index] = outcome.astype(values.dtype)
        dataset.add_primary_attribute(name=outcome_attribute_name, data=values)
        self.correct_infinite_values(dataset, outcome_attribute_name, clip_all_larger_values=True)
        return outcome

