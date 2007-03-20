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
from psrc_parcel.datasets.proposed_development_project_dataset import ProposedDevelopmentProjectDataset
from psrc_parcel.datasets.proposed_development_project_dataset import create_from_parcel_and_development_template
from numarray import exp, arange, logical_and, zeros, where, NumArray, array

class ProposedDevelopmentProjectCostModel(RegressionModel):
    """calculate the costs for proposed development projects
    computed via a regression equation.
    """

    model_name = "Proposed Development Project Cost Model"
    model_short_name = "PDPCM"
                
    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string="template_id", 
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
        parcels = data_objects['parcel']
        if self.filter_attribute <> None:    
            res = Resources(data_objects)
            res.merge({"debug":debuglevel})
            index = parcels.get_filtered_index(self.filter_attribute, threshold=0, index=index, resources=res)
        
        if not isinstance(dataset, ProposedDevelopmentProjectDataset):
            templates = data_objects['development_template']
            dataset = create_from_parcel_and_development_template(parcels, templates, index=index)
            
        costs = RegressionModel.run(self, specification, coefficients, dataset, 
                                    chunk_specification, data_objects, 
                                    run_config, debuglevel)
        if (costs == None) or (costs.size() <=0):
            return costs
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("costs", sale_price)
        
        return dataset
