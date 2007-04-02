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
from numpy import exp, arange, logical_and, zeros, where, array

class RealEstatePriceModel(RegressionModel):
    """Updates building attribute 'unit_price'
    computed via a regression equation.
    """

    model_name = "Real Estate Price Model"
    model_short_name = "REPM"
                
    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string="building_type_id", 
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
        if self.filter_attribute <> None:         
            res = Resources(data_objects)
            res.merge({"debug":debuglevel})
            index = dataset.get_filtered_index(self.filter_attribute, threshold=0, index=index, resources=res)
        unit_price = RegressionModel.run(self, specification, coefficients, dataset, 
                                         index, chunk_specification, data_objects, 
                                         run_config, debuglevel)
        if (unit_price == None) or (unit_price.size <=0):
            return unit_price
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("unit_price", unit_price, index)
        
        return

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
