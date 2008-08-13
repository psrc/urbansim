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

from urbansim.models.development_project_location_choice_model_creator import DevelopmentProjectLocationChoiceModelCreator

class DevelopmentProjectResidentialLocationChoiceModelCreator(object):
    def get_model(self, location_set,
                  sampler = "opus_core.samplers.weighted_sampler", 
                  utilities = "opus_core.linear_utilities", 
                  choices = "opus_core.random_choices", 
                  probabilities = "opus_core.mnl_probabilities", 
                  estimation = "opus_core.bhhh_mnl_estimation", 
                  sample_proportion_locations = None, 
                  sample_size_locations = 10, 
                  estimation_size_agents = 1.0, 
                  compute_capacity_flag = True, 
                  filter = None,
                  submodel_string = "size_category",
                  run_config = None, 
                  estimate_config=None, 
                  development_project_config=None,
                  debuglevel=0):
        creator = DevelopmentProjectLocationChoiceModelCreator()
        creator.get_model('residential',
                          location_set,
                          development_project_config,                          
                          sampler,
                          utilities,
                          choices,
                          probabilities,
                          estimation,
                          sample_proportion_locations, 
                          sample_size_locations,
                          estimation_size_agents,
                          compute_capacity_flag,
                          filter,
                          submodel_string,
                          run_config,
                          estimate_config, 
                          debuglevel)
