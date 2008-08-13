#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from urbansim.models.land_price_model import LandPriceModel
from urbansim.models.correct_land_value import CorrectLandValue

class CorrectedLandPriceModel(LandPriceModel):
    """Runs LandPriceModel and CorrectLandValue"""
        
    def run(self, n_simulated_years, specification, coefficients, dataset, **kwargs):
        LandPriceModel.run(self, specification, coefficients, dataset, **kwargs)
        if n_simulated_years >= 2:
            clv = CorrectLandValue()
            clv.run(dataset)