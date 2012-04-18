# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable_name import VariableName
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from urbansim_parcel.models.development_project_proposal_regression_model import DevelopmentProjectProposalRegressionModel

class ExpectedSalesUnitPriceModel(DevelopmentProjectProposalRegressionModel):
    model_name = "Expected Sales Unit Price Model"
    model_short_name = "ESUPM"
    
    """For estimating expected sales price per unit as a function of REPM result on parcel basis.
    """
    def run(self, specification=None, coefficients=None, dataset=None, proposal_dataset=None, **kwargs):
        """At the moment it's a mock-up model."""
        if proposal_dataset is None:
            proposal_dataset = self.dataset_pool.get_dataset('development_project_proposal')
        proposal_component_set = create_from_proposals_and_template_components(proposal_dataset, 
                                                self.dataset_pool.get_dataset('development_template_component'))
        
        self.dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        #result = RealEstatePriceModel.run(self, specification, coefficients, dataset, **kwargs)
        values = 6.7 * dataset['land_value']/dataset['parcel_sqft'].astype('float32')
        dataset.add_primary_attribute(name=self.outcome_attribute_name, data=values)
        
        props_values = proposal_dataset.compute_variables(['development_project_proposal.disaggregate(parcel.%s)' % self.outcome_attribute_name], 
                                                   dataset_pool=self.dataset_pool)
        proposal_dataset.add_primary_attribute(name=self.outcome_attribute_name, data=props_values)
        return values
    
