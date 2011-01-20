# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

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

