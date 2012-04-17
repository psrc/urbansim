# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable_name import VariableName
from urbansim.models.real_estate_price_model import RealEstatePriceModel

class ExpectedSalesUnitPriceModel(RealEstatePriceModel):
    model_name = "Expected Sales Unit Price Model"
    
    """For estimating expected sales price per unit as a function of REPM result on parcel basis.
    """
    def run(self, specification=None, coefficients=None, dataset=None, **kwargs):
        """At the moment it's a mock-up model."""
        #result = RealEstatePriceModel.run(self, specification, coefficients, dataset, **kwargs)
        result = 6.7 * dataset['land_value']/dataset['parcel_sqft'].astype('float32') 
        return result
    
