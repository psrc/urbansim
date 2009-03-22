# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from numpy import exp, arange, float32, zeros, where, logical_and

class ResidentialLandShareModel(RegressionModel):
    """Updates gridcell attributes 'fraction_residential_land'
       computed via a regression equation.
    """
    model_name = "Residential Land Share Model"
    model_short_name = "RLSM"
    attribute_to_modify = "fraction_residential_land"

    def get_configuration(self):
        return {
          "init":{
            "regression_procedure":{"default":"opus_core.linear_regression",
                                     "type":str},
            "submodel_string":{"default":"development_type_id",
                       "type":str},
            "run_config":{"default":None, "type":Resources},
            "estimate_config":{"default":None, "type":Resources},
            "debuglevel": {"default":0, "type":int}},
          "run": RegressionModel.get_configuration(self)["run"]
            }

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        regression_outcome = RegressionModel.run(self, specification, coefficients, dataset, 
                                index=index, chunk_specification=chunk_specification, data_objects=data_objects,
                                run_config=run_config, debuglevel=debuglevel)
        if (regression_outcome == None) or (regression_outcome.size <=0):
            return regression_outcome
        if index == None:
            index = arange(dataset.size())
        result = exp(regression_outcome)
        result = result/(1.0+result)
        if  (self.attribute_to_modify not in dataset.get_known_attribute_names()):
            dataset.add_attribute(name=self.attribute_to_modify,
                                   data=zeros((dataset.size(),), dtype=float32))
        dataset.set_values_of_one_attribute(self.attribute_to_modify, result, index)
        return result

    def estimate(self, specification, dataset, outcome_attribute="urbansim.gridcell.logistic_fraction_residential_land", index = None,
                        procedure="opus_core.estimate_linear_regression", data_objects=None,
                        estimate_config=None,  debuglevel=0):
        return RegressionModel.estimate(self, specification, dataset, outcome_attribute, index, procedure, data_objects=data_objects,
                                     estimate_config=estimate_config, debuglevel=debuglevel)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, dataset=None,
                              filter_variable="urbansim.gridcell.fraction_residential_land"):
        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        index = None
        if dataset is not None:
            dataset.compute_variables(filter_variable)
            tmp = where(dataset.get_attribute(filter_variable) > 0, 1, 0)
            tmp = logical_and(tmp, where(dataset.get_attribute(filter_variable) < 1, 1, 0))
            index = where(tmp)[0]
        return (specification, index)

    def prepare_for_run(self, *args, **kwargs):
        spec, coef, dummy = RegressionModel.prepare_for_run(self, *args, **kwargs)
        return (spec, coef)

from opus_core.tests import opus_unittest
from numpy import array, ma, float32
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):

    def test_residential_land_share_model(self):
        storage = StorageFactory().get_storage('dict_storage')

        gridcell_set_table_name = 'gridcell_set'
        storage.write_table(
            table_name=gridcell_set_table_name,
            table_data={
                "residential_units":array([1000, 0, 10, 500]),
                "development_type_id":array([8, 17, 4, 8]),
                "grid_id": array([1,2,3,4])
                }
            )

        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        specification = EquationSpecification(variables=(
            "urbansim.gridcell.devtype_8",
            "gridcell.residential_units", "constant"),
            coefficients=("DEV8", "units", "constant"))
        coefficients = Coefficients(names=("constant", "DEV8", "units"), values=(-0.4, 1.6, 0.01))
        ResidentialLandShareModel(debuglevel=3).run(specification, coefficients, gridcell_set)
        result = gridcell_set.get_attribute("fraction_residential_land")
        self.assertEqual(ma.allclose(result, array([0.9999863,  0.4013123, 0.4255575, 0.9979747]), rtol=1e-3), True)


if __name__=="__main__":
    opus_unittest.main()