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
from psrc_parcel.datasets.development_project_proposal_dataset import DevelopmentProjectProposalDataset
from psrc_parcel.datasets.development_project_proposal_dataset import create_from_parcel_and_development_template
from numpy import exp, arange, logical_and, zeros, where, NumArray, array

class ProposedDevelopmentProjectSalePriceModel(RegressionModel):
    """calculate the expected sale price for proposed development projects
    computed via a regression equation, usually share the specification and coefficients  with real estate price (property value) model
    """

    model_name = "Prposed Development Project Sale Price Model"
    model_short_name = "PDPSPM"
                
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
        dataset should be an instance of DevelopmentProjectProposalDataset, if it isn't,
        create on the fly with parcel and development template
        index and self.filter_attribute (passed in __init___) are supposed to relative to dataset,
            if dataset is not an instance DevelopmentProjectProposalDataset, then index is relative
            to parcels
        """
        if not isinstance(dataset, DevelopmentProjectProposalDataset):
            parcels = data_objects['parcel']
            templates = data_objects['development_template']

            res = Resources(data_objects)
            res.merge({"debug":debuglevel})            
            dataset = create_from_parcel_and_development_template(parcels, templates, 
                                                                  index=index, 
                                                                  filter=self.filter_attribute,
                                                                  resources=res)
            index = None
        unit_price = RegressionModel.run(self, specification, coefficients, dataset, 
                                         index, chunk_specification, data_objects,
                                         run_config, debuglevel)
        if (unit_price == None) or (unit_price.size <=0):
            return None
        if index == None:
             index = arange(dataset.size())
        dataset.set_values_of_one_attribute("unit_price", sale_price, index)
        
        return dataset