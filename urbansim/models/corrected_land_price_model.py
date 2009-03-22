# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.land_price_model import LandPriceModel
from urbansim.models.correct_land_value import CorrectLandValue

class CorrectedLandPriceModel(LandPriceModel):
    """Runs LandPriceModel and CorrectLandValue"""
        
    def run(self, n_simulated_years, specification, coefficients, dataset, **kwargs):
        LandPriceModel.run(self, specification, coefficients, dataset, **kwargs)
        if n_simulated_years >= 2:
            clv = CorrectLandValue()
            clv.run(dataset)