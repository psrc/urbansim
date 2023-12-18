# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, arange
from opus_core.models.regression_model import RegressionModel
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger


class RegressionModelWithAdditionInitialResiduals(RegressionModel):

    """
    It is a RegressionModel that computes an initial error of the observations to the predictions
    when run for the first time. Then every time it runs, it adds this error to the outcome. The 'error' attribute
    is called '_init_error_%s' % outcome_attribute and it is stored as a primary attribute.
    """
    model_name = "Regression Model With Addition of Initial Residuals"
    model_short_name = "RMWAIR"

    def __init__(self, regression_procedure="opus_core.linear_regression",
                  submodel_string=None, outcome_attribute = None,
                  run_config=None, estimate_config=None, debuglevel=None, dataset_pool=None):
        """'outcome_attribute' must be specified in order to compute the residuals.
        """
        RegressionModel.__init__(self,
                                 regression_procedure=regression_procedure,
                                 submodel_string=submodel_string,
                                 run_config=run_config,
                                 estimate_config=estimate_config,
                                 debuglevel=debuglevel, dataset_pool=dataset_pool)
        self.outcome_attribute = outcome_attribute
        if (self.outcome_attribute is not None) and not isinstance(self.outcome_attribute, VariableName):
            self.outcome_attribute = VariableName(self.outcome_attribute)

    def run(self, specification, coefficients, dataset, index=None, 
            outcome_with_inital_error=True, **kwargs):
        """
        See description above. If missing values of the outcome attribute are suppose to be excluded from
        the addition of the initial residuals, set an entry of run_config 'exclude_missing_values_from_initial_error' to True.
        Additionaly, an entry 'outcome_attribute_missing_value' specifies the missing value (default is 0).
        Similarly, if outliers are to be excluded, the run_config entry "exclude_outliers_from_initial_error" should be set to True.
        In such a case, run_config entries 'outlier_is_less_than' and 'outlier_is_greater_than' can define lower and upper bounds for outliers. 
        By default, an outlier is a data point smaller than 0. There is no default upper bound.
        """
        if self.outcome_attribute is None:
            raise Exception("An outcome attribute must be specified for this model. Pass it into the initialization.")
        
        if self.outcome_attribute.get_alias() not in dataset.get_known_attribute_names():
            try:
                dataset.compute_variables(self.outcome_attribute, dataset_pool=self.dataset_pool)
            except:
                raise Exception("The outcome attribute %s must be a known attribute of the dataset %s." % (
                                                                self.outcome_attribute.get_alias(), dataset.get_dataset_name()))
            
        if index is None:
            index = arange(dataset.size())
        original_data = dataset.get_attribute_by_index(self.outcome_attribute, index)
        
        outcome = RegressionModel.run(self, specification, coefficients, dataset, index, initial_values=original_data.astype('float32'), **kwargs)
        initial_error_name = "_init_error_%s" % self.outcome_attribute.get_alias()


        if initial_error_name not in dataset.get_known_attribute_names():
            initial_error = original_data - outcome
            dataset.add_primary_attribute(name=initial_error_name, data=zeros(dataset.size(), dtype="float32"))
            exclude_missing_values = self.run_config.get("exclude_missing_values_from_initial_error", False)
            exclude_outliers = self.run_config.get("exclude_outliers_from_initial_error", False)
            if exclude_missing_values:
                missing_value = self.run_config.get("outcome_attribute_missing_value", 0)
                initial_error[original_data == missing_value] = 0
                logger.log_status('Values equal %s were excluded from adding residuals.' % missing_value)
            if exclude_outliers:
                outlier_low = self.run_config.get("outlier_is_less_than", 0)
                initial_error[original_data < outlier_low] = 0
                outlier_high = self.run_config.get("outlier_is_greater_than", original_data.max())
                initial_error[original_data > outlier_high] = 0
                logger.log_status('Values less than %s and larger than %s were excluded from adding residuals.' % (outlier_low, outlier_high))
            dataset.set_values_of_one_attribute(initial_error_name, initial_error, index)
        else:
            initial_error = dataset.get_attribute_by_index(initial_error_name, index)

        logger.log_status("initial_error saved to %s.%s" % (dataset.dataset_name, initial_error_name))
        if outcome_with_inital_error:
            return outcome + initial_error
        else:
            logger.log_status("initial_error not added to outcome %s" % self.outcome_attribute.get_alias())
            return outcome

    def run_after_estimation(self, *args, **kwargs):
        return RegressionModel.run(self, *args, **kwargs)
    
from opus_core.tests import opus_unittest
from numpy import array, ma
from opus_core.datasets.dataset import Dataset
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.configuration import Configuration


class Test(opus_unittest.OpusTestCase):
    def test_regression_model_with_constant_variation(self):
        """Estimate the model and run it on the same data as the estimation. The result should be equal to the original data.
        If there is a change in the explanatory variables, the result should not be equal.
        """
        storage = StorageFactory().get_storage('dict_storage')

        table_name = 'dataset_table'
        data = {
                "attr1":array([30, 0, 90, 100, 65, 50]),
                "attr2":array([2002, 1968, 1880, 1921, 1956, 1989]),
                "attr3":array([0.5, 0.1, 0.3, 0.9, 0.2, 0.8]),
                "outcome": array([20, 40, 15, 5, 40, 30], dtype="int32"),
                "id": array([1,2,3,4, 5, 6])
                }
        storage.write_table(
            table_name=table_name,
            table_data=data
            )
        dataset = Dataset(in_storage=storage, in_table_name=table_name, id_name= "id")

        specification = EquationSpecification(variables=(
            "attr1", "attr2", "attr3", "constant"),
            coefficients=("b1", "b2", "b3", "constant"))

        model = RegressionModelWithAdditionInitialResiduals(outcome_attribute = "outcome")
        coef, dummy = model.estimate(specification, dataset, outcome_attribute = "outcome",
                                     procedure = "opus_core.estimate_linear_regression")
        result = model.run(specification, coef, dataset)

        # if estimated and run on the same data, it should give the original outcome
        self.assertEqual(ma.allequal(result, data["outcome"]), True)

        # if some values changed it shoudn't be the same for those elements
        dataset.set_values_of_one_attribute("attr1", array([32, 10]), arange(2))
        result2 = model.run(specification, coef, dataset)
        self.assertEqual(ma.allequal(result2[0:2], data["outcome"][0:2]), False)
        self.assertEqual(ma.allequal(result2[2:], data["outcome"][2:]), True)
        
        # check if exclusion of missing values is working
        dataset.set_values_of_one_attribute("outcome", array([0,0]), array([2,4]))
        dataset.delete_one_attribute("_init_error_outcome")
        model.run(specification, coef, dataset, run_config=Configuration({
                                          'exclude_missing_values_from_initial_error': True}))
        initial_error = dataset.get_attribute("_init_error_outcome")
        self.assertEqual(ma.allequal(initial_error[array([2,4])], 0), True)
        self.assertEqual(ma.allequal(initial_error[array([0,1,3,4,5])], 0), False)
        

if __name__=="__main__":
    opus_unittest.main()
