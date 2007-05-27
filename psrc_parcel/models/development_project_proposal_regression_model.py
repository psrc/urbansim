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
from psrc_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from numpy import exp, arange, logical_and, zeros, where, array, float32, int16
import re

class DevelopmentProjectProposalRegressionModel(RegressionModel):
    """Generic regression model on development project proposal dataset
    """
    model_name = "Development Project Proposal Regression Model"
    model_short_name = "PDPRM"
    outcome_attribute_name = "regression_result"
    defalult_value = array([0], dtype="int32")  
    # or defalult_value = 0.0, use 1 element array to control the type of the outcome attribute
    
    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string="building_type_id", 
                 outcome_attribute_name=None,
                 model_name=None,
                 model_short_name=None,
                 run_config=None, 
                 estimate_config=None, 
                 debuglevel=0, dataset_pool=None):
        self.filter = filter_attribute
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name
        if outcome_attribute_name is not None:
            self.outcome_attribute_name = outcome_attribute_name
        
        RegressionModel.__init__(self, 
                                 regression_procedure=regression_procedure, 
                                 submodel_string=submodel_string, 
                                 run_config=run_config, 
                                 estimate_config=estimate_config, 
                                 debuglevel=debuglevel, dataset_pool=dataset_pool)
                    
    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None, 
             data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        dataset should be an instance of DevelopmentProjectProposalDataset, if it isn't,
        create dataset on the fly with parcel and development template
        index and self.filter_attribute (passed in __init___) are relative to dataset
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        proposal_component_set = create_from_proposals_and_template_components(dataset, 
                                                           self.dataset_pool.get_dataset('development_template_component'))
        self.dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        self.dataset_pool.add_datasets_if_not_included({dataset.get_dataset_name(): dataset})
        result = RegressionModel.run(self, specification, coefficients, dataset, 
                                         index, chunk_specification, data_objects,
                                         run_config, debuglevel)

        if re.search("^ln_", self.outcome_attribute_name): # if the outcome attr. name starts with 'ln_'
                                                           # the results will be exponentiated.
            self.outcome_attribute_name = self.outcome_attribute_name[3:len(self.outcome_attribute_name)]
            result = exp(result)

        if self.outcome_attribute_name not in dataset.get_known_attribute_names():
            dataset.add_primary_attribute(self.defalult_value + zeros(dataset.size()),
                                             self.outcome_attribute_name)
        
        dataset.set_values_of_one_attribute(self.outcome_attribute_name, 
                                                 result, index=index)
        
        return dataset
    
    def prepare_for_run(self, dataset_pool, parcel_filter=None, spec_replace_module_variable_pair=None, 
                        *args, **kwargs):
        """create development project proposal dataset from parcels and development templates.
        spec_replace_module_variable_pair is a tuple with two elements: module name, variable within the module
        that contans a dictionary of model variables to be replaced in the specification.
        """
        specification, coefficients = RegressionModel.prepare_for_run(self, *args, **kwargs)

        #data_objects = kwargs['data_objects']
        parcels = dataset_pool.get_dataset('parcel')
        templates = dataset_pool.get_dataset('development_template')

        if parcel_filter is not None:
            parcels.compute_variables(parcel_filter)
            index1 = where(parcels.get_attribute(parcel_filter))[0]
        else:
            index1 = None
            
#        from opus_core.misc import sample
#        from opus_core.datasets.dataset import DatasetSubset
#        n = parcels.size()
#        index1=sample(arange(n), int(n*0.001))

        proposal_set = create_from_parcel_and_development_template(parcels, templates, 
                                                              filter_attribute=self.filter,
                                                              index = index1,
                                                              dataset_pool=dataset_pool,
                                                              resources = kwargs.get("resources", None))
        if spec_replace_module_variable_pair is not None:
            exec("from %s import %s as spec_replacement" % (spec_replace_module_variable_pair[0], 
                                                            spec_replace_module_variable_pair[1]))
            specification.replace_variables(spec_replacement)
            
        return (proposal_set, specification, coefficients)
        