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
from opus_core.regression_model import RegressionModel
from numpy import exp, arange, logical_and, zeros, where, NumArray, array

class RealEstatePriceModel(RegressionModel):
    """Updates gridcell attributes 'real_estate_price'
    computed via a regression equation.
    """

    model_name = "Real Estate Price Model"
    model_short_name = "REPM"
                
    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string="building_use_id", 
                 outcome_attribute = "unit_price",
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
        self.outcome_attribute = outcome_attribute
                    
    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None, 
            data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        """            
        if self.filter_attribute <> None:         
            res = Resources(data_objects)
            res.merge({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, resources=res)
        outcome = RegressionModel.run(self, specification, coefficients, dataset, 
                                         index, chunk_specification, data_objects, 
                                         run_config, debuglevel)
        if (outcome == None) or (outcome.size <=0):
            return unit_price
        if index == None:
             index = arange(dataset.size())
        if re.search("^ln_", self.outcome_attribute): # if the outcome attr. name starts with 'ln_'
                                                      # the results will be exponentiated.
            self.outcome_attribute = self.outcome_attribute[3:len(self.outcome_attribute)]
            outcome = exp(outcome)
        if self.outcome_attribute not in dataset.get_known_attribute_names():
            dataset.add_primary_attribute(name=self.outcome_attribute, data=zeros(dataset.size(), float32)) 
             
        dataset.set_values_of_one_attribute(self.outcome_attribute, outcome, index)
        return outcome

    def estimate(self, specification, dataset, outcome_attribute="unit_price", index = None, 
                        procedure="opus_core.estimate_linear_regression", data_objects=None, 
                        estimate_config=None,  debuglevel=0):
        if self.filter_attribute <> None:
            res = Resources(data_objects)
            res.merge({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, resources=res)
        return RegressionModel.estimate(self, specification, dataset, outcome_attribute, index, procedure, data_objects, 
                                     estimate_config, debuglevel)

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
