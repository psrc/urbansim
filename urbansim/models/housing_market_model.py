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

from opus_core.market_model import MarketModel

class HousingMarketModel(MarketModel):
    def __init__(self, location_set, 
                        sampler="opus_core.samplers.weighted_sampler", 
                        utilities="opus_core.linear_utilities", 
                        probabilities="opus_core.mnl_probabilities", 
                        choices="opus_core.random_choices_from_index",
                        sample_proportion_locations = None, 
                        sample_size_locations = 10, 
                        filter=None, submodel_string=None,
                        run_config=None):
        compute_capacity_flag = True
        self.hlcm = HouseholdLocationChoiceModelCreator.get_model(
                location_set=location_set, sampler=sampler,  
                utilities=utilities, probabilities=probabilities, 
                choices=choices, 
                sample_proportion_locations=sample_proportion_locations, 
                sample_size_locations=sample_size_locations, 
                compute_capacity_flag = compute_capacity_flag,
                filter=filter, submodel_string=submodel_string,
                run_config=run_config)
    
    def run(self):
        pass