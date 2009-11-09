# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from numpy import array, exp, arange, zeros
from opus_core.resources import Resources
from opus_core.regression_model import RegressionModel
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState

class WaterDemandModel(RegressionModel):
    """
    """
#    filter_attribute = "include_in_housing_value_estimation"
    model_name = "Water Demand Model"
    model_short_name = "WDM"

    def __init__(self, regression_procedure="opus_core.linear_regression",
                 outcome_attribute="month_combination_2",
                 filter_attribute=None,
                 submodel_string="land_use_type_id",
                 run_config=None,
                 estimate_config=None,
                 debuglevel=0,
                 dataset_pool=None):
        self.outcome_attribute = outcome_attribute
        if (self.outcome_attribute is not None) and not isinstance(self.outcome_attribute, VariableName):
            self.outcome_attribute = VariableName(self.outcome_attribute)
        
        self.filter_attribute = filter_attribute
        RegressionModel.__init__(self,
                                 regression_procedure=regression_procedure,
                                 submodel_string=submodel_string,
                                 run_config=run_config,
                                 estimate_config=estimate_config,
                                 debuglevel=debuglevel,
                                 dataset_pool=dataset_pool)

    def run(self, specification, coefficients, dataset, 
            index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """
        outcome_attribute_short = self.outcome_attribute.get_alias()
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.filter_attribute <> None:
            res = Resources({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
                                               dataset_pool=self.dataset_pool, resources=res)
        
        current_year = SimulationState().get_current_time()
        current_month = int( re.search('\d+$', outcome_attribute_short).group() )
        # date in YYYYMM format, matching to the id_name field of weather dataset
        date = int( "%d%02d" % (current_year, current_month) )
        date = array([date] * dataset.size())
        
        if "date" in dataset.get_known_attribute_names():
            dataset.set_values_of_one_attribute("date", date)
        else:
            dataset.add_primary_attribute(date, "date")

        water_demand = RegressionModel.run(self, specification, coefficients, dataset, 
                                           index, chunk_specification,
                                           run_config=run_config, debuglevel=debuglevel)
        if (water_demand == None) or (water_demand.size <=0):
            return water_demand
        
        if index == None:
            index = arange(dataset.size())
            
        if re.search("^ln_", outcome_attribute_short): 
            # if the outcome attr. name starts with 'ln_' the results will be exponentiated.
            outcome_attribute_name = outcome_attribute_short[3:len(outcome_attribute_short)]
            water_demand = exp(water_demand)
        else:
            outcome_attribute_name = outcome_attribute_short

        if outcome_attribute_name in dataset.get_known_attribute_names():
            dataset.set_values_of_one_attribute(outcome_attribute_name, water_demand, index)
        else:
            results = zeros(dataset.size(), dtype=water_demand.dtype)
            results[index] = water_demand
            dataset.add_primary_attribute(results, outcome_attribute_name)

        return water_demand

#    def estimate(self, specification, dataset, outcome_attribute="housing_price", index = None,
#                        procedure="opus_core.estimate_linear_regression", data_objects=None,
#                        estimate_config=None,  debuglevel=0):
#        if data_objects is not None:
#            self.dataset_pool.add_datasets_if_not_included(data_objects)
#        if self.filter_attribute <> None:
#            res = Resources({"debug":debuglevel})
#            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index,
#                                               dataset_pool=self.dataset_pool, resources=res)
#        return RegressionModel.estimate(self, specification, dataset, outcome_attribute, index, procedure,
#                                     estimate_config=estimate_config, debuglevel=debuglevel)
#
#    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
#                              specification_table=None, dataset=None,
#                              filter_variable="housing_price",
#                              threshold=0):
#        from opus_core.model import get_specification_for_estimation
#        specification = get_specification_for_estimation(specification_dict,
#                                                          specification_storage,
#                                                          specification_table)
#        index = None
#        if dataset is not None:
#            dataset.compute_variables(filter_variable)
#            index = where(dataset.get_attribute(filter_variable) >= threshold)[0]
#        return (specification, index)
#
#
