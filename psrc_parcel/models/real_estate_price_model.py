# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable_name import VariableName
from urbansim.models.real_estate_price_model import RealEstatePriceModel as USRealEstatePriceModel

class RealEstatePriceModel(USRealEstatePriceModel):
    model_name = "Real Estate Price Model (with post-processing)"
    
    """Like REPM in urbansim, but the run method contains a post-processing step that computes a given variable
        and stores it as a primary attribute.
    """
    def run(self, add_attribute, specification, coefficients, dataset, **kwargs):
        result = USRealEstatePriceModel.run(self, specification, coefficients, dataset, **kwargs)
        self.postprocess(dataset, add_attribute)
        return result
    
    def postprocess(self, dataset, attribute=None):
        if attribute is None:
            return
        values = dataset.compute_variables([attribute], dataset_pool=self.dataset_pool).copy()
        short_name = VariableName(attribute).get_alias()
        dataset.delete_one_attribute(short_name)
        dataset.add_primary_attribute(name=short_name, data=values)
        