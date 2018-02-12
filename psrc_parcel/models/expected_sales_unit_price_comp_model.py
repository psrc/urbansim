# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable_name import VariableName
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from urbansim_parcel.models.development_project_proposal_regression_model import DevelopmentProjectProposalRegressionModel
from opus_core.model import get_specification_for_estimation
from opus_core.datasets.dataset import Dataset
from opus_core.models.regression_model import RegressionModel
from numpy import where, exp, zeros, minimum, maximum
import re

class ExpectedSalesUnitPriceModel(DevelopmentProjectProposalRegressionModel, RegressionModel):
    model_name = "Expected Sales Unit Price Model"
    model_short_name = "ESUPM"
    
    """For estimating expected sales price per unit as a function of REPM result on parcel basis.
    """
    def run(self, specification=None, coefficients=None, dataset=None,  **kwargs):
        outcome = RegressionModel.run(self, specification, coefficients, dataset, **kwargs)
        
        if (outcome is None) or (outcome.size <= 0):
            return outcome
        if re.search("^ln_", self.outcome_attribute_name): # if the outcome attr. name starts with 'ln_'
                                                      # the results will be exponentiated.
            self.outcome_attribute_name = self.outcome_attribute_name[3:len(self.outcome_attribute_name)]
            outcome = exp(outcome)

        if self.outcome_attribute_name not in dataset.get_known_attribute_names():
            dataset.add_primary_attribute(name=self.outcome_attribute_name, data=zeros(dataset.size(), dtype='f'))

        dataset.set_values_of_one_attribute(self.outcome_attribute_name,  outcome)
        self.correct_infinite_values(dataset, self.outcome_attribute_name, clip_all_larger_values=True)
            
        #values = 6.7 * dataset['land_value']/dataset['parcel_sqft'].astype('float32')
        #dataset.add_primary_attribute(name=self.outcome_attribute_name, data=values)
        
        #props_values = proposal_dataset.compute_variables(['development_project_proposal.disaggregate(parcel.%s)' % self.outcome_attribute_name], 
        #                                           dataset_pool=self.dataset_pool)
        #proposal_dataset.add_primary_attribute(name=self.outcome_attribute_name, data=props_values)
        return outcome
    
    def prepare_for_run(self, *args, **kwargs):
        proposal_set, specification, coefficients = DevelopmentProjectProposalRegressionModel.prepare_for_run(self, *args, **kwargs)
        proposal_component_set = create_from_proposals_and_template_components(proposal_set, 
                                                self.dataset_pool.get_dataset('development_template_component'))
        self.dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        self.dataset_pool.replace_dataset(proposal_set.get_dataset_name(), proposal_set)
        # reduce units_proposed 
        proposal_set.compute_variables(["is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0",
                                        "is_nonres = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential==0) > 0",
                                        "parcel_res_units = development_project_proposal.disaggregate(urbansim_parcel.parcel.residential_units)",
                                        "parcel_bld_sqft = development_project_proposal.disaggregate(urbansim_parcel.parcel.building_sqft)"],
                                       dataset_pool=self.dataset_pool)
        units_proposed = proposal_set["units_proposed"]
        units_proposed[proposal_set["is_res"]] = minimum(units_proposed[proposal_set["is_res"]], maximum(proposal_set["parcel_res_units"] + 1000))
        units_proposed[proposal_set["is_nonres"]] = minimum(units_proposed[proposal_set["is_nonres"]], maximum(proposal_set["parcel_bld_sqft"] + 1000000))
        proposal_set.modify_attribute("units_proposed", units_proposed)
        self.dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        self.dataset_pool.replace_dataset(proposal_set.get_dataset_name(), proposal_set)
        return (proposal_set, proposal_component_set, specification, coefficients)
    
    def prepare_for_estimate(self, estimation_storage=None, estimation_table=None, dataset_filter=None, 
                            filter_threshold=0, **kwargs):
        spec = get_specification_for_estimation(**kwargs)
        if estimation_storage is not None and estimation_table is not None:
            dataset = Dataset(in_storage = estimation_storage, in_table_name=estimation_table,
                                     id_name='proposal_component_id', 
                                     dataset_name='development_project_proposal_component')
        if (dataset is not None) and (dataset_filter is not None):
            filter_values = dataset.compute_variables([dataset_filter], dataset_pool=self.dataset_pool)
            index = where(filter_values > filter_threshold)[0]
        else:
            index = None
        return (dataset, spec, index)