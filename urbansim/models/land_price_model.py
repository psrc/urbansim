# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from numpy import exp, arange, where, isinf
from opus_core.logger import logger

class LandPriceModel(RegressionModel):
    """Updates location attributes 'residential_land_value' and 'nonresidential_land_value'
    computed via a regression equation.
    """
    maxfloat32 = 1e+38
    model_name = "Land Price Model"
    model_short_name = "LPM"


    def __init__(self, regression_procedure="opus_core.linear_regression",
                 filter = "urbansim.gridcell.is_in_development_type_group_developable",
                 submodel_string = "development_type_id",
                 run_config=None,
                 estimate_config=None,
                 debuglevel=0, dataset_pool=None):
        self.filter = filter
        if filter is None:
            if run_config is not None and 'filter' in run_config:
                self.filter = run_config["filter"]
            elif estimate_config is not None and 'filter' in estimate_config:
                self.filter = estimate_config["filter"]

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
        if self.filter <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter, threshold=0, index=index, dataset_pool=self.dataset_pool,
                                               resources=res)
        ln_total_land_value = RegressionModel.run(self, specification, coefficients, dataset, index, chunk_specification,
                                     run_config=run_config, debuglevel=debuglevel)
        if (ln_total_land_value == None) or (ln_total_land_value.size <=0):
            return ln_total_land_value
        if index == None:
             index = arange(dataset.size())
        total_land_value = exp(ln_total_land_value)
        residential_land_value = total_land_value * dataset.get_attribute_by_index("fraction_residential_land", index)
        nonresidential_land_value = total_land_value - residential_land_value
        dataset.set_values_of_one_attribute("residential_land_value", residential_land_value, index)
        dataset.set_values_of_one_attribute("nonresidential_land_value", nonresidential_land_value,
                                            index)
        self.post_check(dataset)
        return index

    def estimate(self, specification, dataset, outcome_attribute="urbansim.gridcell.ln_total_land_value", index = None,
                        procedure="opus_core.estimate_linear_regression", data_objects=None,
                        estimate_config=None,  debuglevel=0):
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter, threshold=0, index=index, dataset_pool=self.dataset_pool,
                                               resources=res)
        return RegressionModel.estimate(self, specification, dataset, outcome_attribute, index, procedure,
                                     estimate_config=estimate_config, debuglevel=debuglevel)

    def post_check(self, dataset, resources=None):
        """Check if the model resulted in infinite values. If yes,
        print warning and clip the values to maximum of float32"""
        infidx = where(isinf(dataset.get_attribute("residential_land_value")))[0]

        if infidx.size > 0:
            logger.log_warning("Infinite values in residential_land_value.")
            dataset.set_values_of_one_attribute("residential_land_value", self.maxfloat32,
                                                 infidx)
        infidx = where(isinf(dataset.get_attribute("nonresidential_land_value")))[0]
        if infidx.size > 0:
            logger.log_warning("Infinite values in nonresidential_land_value.")
            dataset.set_values_of_one_attribute("nonresidential_land_value", self.maxfloat32,
                                                 infidx)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, dataset=None,
                              filter_variable="urbansim.gridcell.total_land_value",
                              threshold=0):
        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        index = None
        if dataset is not None:
            dataset.compute_variables(filter_variable)
            index = where(dataset.get_attribute(filter_variable) >= threshold)[0]
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

    def test_do_nothing_if_empty_set(self):
        storage = StorageFactory().get_storage('dict_storage')

        gridcell_set_table_name = 'gridcell_set'
        storage.write_table(
            table_name=gridcell_set_table_name,
            table_data={"grid_id": array([], dtype='int32')}
            )
        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        specification = EquationSpecification(variables=(
            "percent_residential_within_walking_distance",
            "gridcell_year_built", "constant"),
            coefficients=("PRWWD", "YB", "constant"))
        coefficients = Coefficients(names=("constant", "PRWWD", "YB"), values=(10.0, -0.0025, 0.0001))
        lp = LandPriceModel(filter=None, debuglevel=4)
        result = lp.run(specification, coefficients, gridcell_set)
        self.assertEqual(result.size, 0)

    def test_land_price_model(self):
        storage = StorageFactory().get_storage('dict_storage')

        gridcell_set_table_name = 'gridcell_set'
        storage.write_table(
            table_name=gridcell_set_table_name,
            table_data={
                "percent_residential_within_walking_distance":array([30, 0, 90, 100]),
                "gridcell_year_built":array([2002, 1968, 1880, 1921]),
                "fraction_residential_land":array([0.5, 0.1, 0.3, 0.9]),
                "residential_land_value":array([0, 0, 0, 0]),
                "nonresidential_land_value":array([0, 0, 0, 0]),
                "development_type_id":array(  [1, 1,  1, 1]),
                "grid_id": array([1,2,3,4])
                }
            )
        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        specification = EquationSpecification(variables=(
            "percent_residential_within_walking_distance",
            "gridcell_year_built", "constant"),
            coefficients=("PRWWD", "YB", "constant"))
        coefficients = Coefficients(names=("constant", "PRWWD", "YB"), values=(10.0, -0.0025, 0.0001))
        lp = LandPriceModel(filter=None, debuglevel=3)
        lp.run(specification, coefficients, gridcell_set)
        result1 = gridcell_set.get_attribute("residential_land_value")
        result2 = gridcell_set.get_attribute("nonresidential_land_value")
        self.assertEqual(ma.allclose(result1, array([12482.124,  2681.723,  6367.914, 18708.617]), rtol=1e-3), True)
        self.assertEqual(ma.allclose(result2, array([12482.124,  24135.510, 14858.466,  2078.735]), rtol=1e-3), True)

    def test_infinite_values(self):
        storage = StorageFactory().get_storage('dict_storage')

        gridcell_set_table_name = 'gridcell_set'
        storage.write_table(
            table_name=gridcell_set_table_name,
            table_data={
                "residential_land_value":array([100, 1e+50, 800, 0], dtype=float32),
                "nonresidential_land_value":array([1e+100, 0, 20, 0], dtype=float32),
                "grid_id": array([1,2,3,4])
                }
            )
        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        lp = LandPriceModel()

        logger.enable_hidden_error_and_warning_words()
        lp.post_check(gridcell_set)
        logger.disable_hidden_error_and_warning_words()

        result1 = gridcell_set.get_attribute("residential_land_value")
        result2 = gridcell_set.get_attribute("nonresidential_land_value")
        self.assertEqual(ma.allclose(result1, array([100,  1e+38,  800, 0]), rtol=1e-3), True)
        self.assertEqual(ma.allclose(result2, array([1e+38,  0, 20,  0]), rtol=1e-3), True)


if __name__=="__main__":
    opus_unittest.main()
