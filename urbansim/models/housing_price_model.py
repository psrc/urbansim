# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from numpy import exp, arange, logical_and, zeros, where, array

class HousingPriceModel(RegressionModel):
    """Updates gridcell attributes 'housing_price'
    computed via a regression equation.
    """
#    filter_attribute = "include_in_housing_value_estimation"
    model_name = "Housing Price Model"
    model_short_name = "HPM"

    def __init__(self, regression_procedure="opus_core.linear_regression",
                 filter_attribute="urbansim.gridcell.has_residential_units",
                 submodel_string="development_type_id",
                 run_config=None,
                 estimate_config=None,
                 debuglevel=0):
        self.filter_attribute = filter_attribute
        RegressionModel.__init__(self,
                                 regression_procedure=regression_procedure,
                                 submodel_string=submodel_string,
                                 run_config=run_config,
                                 estimate_config=estimate_config,
                                 debuglevel=debuglevel)

    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute != None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
                                               dataset_pool=self.dataset_pool, resources=res)
        housing_price = RegressionModel.run(self, specification, coefficients, dataset, index, chunk_specification,
                                     run_config=run_config, debuglevel=debuglevel)
        if (housing_price == None) or (housing_price.size <=0):
            return housing_price
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("housing_price", housing_price, index)

        return

    def estimate(self, specification, dataset, outcome_attribute="housing_price", index = None,
                        procedure="opus_core.estimate_linear_regression", data_objects=None,
                        estimate_config=None,  debuglevel=0):
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute != None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
                                               dataset_pool=self.dataset_pool, resources=res)
        return RegressionModel.estimate(self, specification, dataset, outcome_attribute, index, procedure,
                                     estimate_config=estimate_config, debuglevel=debuglevel)

    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, dataset=None,
                              filter_variable="housing_price",
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
            table_data={
                "grid_id": array([], dtype='int32')
                }
            )

        gridcell_set = GridcellDataset(in_storage=storage, in_table_name=gridcell_set_table_name)

        specification = EquationSpecification(variables=(
            "percent_residential_within_walking_distance",
            "gridcell_year_built", "constant"),
            coefficients=("PRWWD", "YB", "constant"))
        coefficients = Coefficients(names=("constant", "PRWWD", "YB"), values=(10.0, -0.0025, 0.0001))
        lp = HousingPriceModel(debuglevel=4)
        lp.filter_attribute = None
        result = lp.run(specification, coefficients, gridcell_set)
        self.assertEqual(result.size, 0)

    def test_housing_price_model(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='gridcells',
            table_data={
                'percent_residential_within_walking_distance':array([30, 0, 90, 100]),
                'gridcell_year_built':array([2002, 1968, 1880, 1921]),
                'housing_price':array([0, 0, 0, 0]).astype(float32),
                'development_type_id':array([1, 1,  1, 1]),
                'grid_id':array([1,2,3,4])
                }
            )

        gridcell_set = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        specification = EquationSpecification(
            variables = (
                'percent_residential_within_walking_distance',
                'gridcell_year_built',
                'constant'
                ),
            coefficients=(
                'PRWWD',
                'YB',
                'constant'
                )
            )

        coefficients = Coefficients(names=("constant", "PRWWD", "YB"), values=(10.0, -0.25, 0.1))

        lp = HousingPriceModel(debuglevel=3)
        lp.filter_attribute = None
        lp.run(specification, coefficients, gridcell_set)
        result = gridcell_set.get_attribute("housing_price")

        self.assertEqual(ma.allclose(result, array([202.7,  206.8,  175.5, 177.1]), rtol=1e-3), True)


if __name__=="__main__":
    opus_unittest.main()