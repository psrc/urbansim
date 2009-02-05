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

from baseline_multiple_travel_models_2020 import BaselineMultipleTravelModels2020

class BaselineTravelModel2020BiaspfVarpf(BaselineMultipleTravelModels2020):
    
    
    def __init__(self):
        BaselineMultipleTravelModels2020.__init__(self)
        self['number_of_runs'] = 1
        self['seed'] = 1
        self['travel_model_configuration'][2020]['bank'] = [ '2020_bpf_vpf', ]
        self['travel_model_configuration']['bm_distribution_file'] = \
                '/Users/hana/bm/psrc_parcel/simulation_results/0127/2005/bm_parameters'
        self['travel_model_configuration']['bm_posterior_procedure'] = ('inprocess.hana.uncertainty.bm_normal_posterior', 'bm_normal_posterior')           

