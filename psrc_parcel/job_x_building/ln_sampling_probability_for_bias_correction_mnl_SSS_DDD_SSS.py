# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.ln_sampling_probability_for_bias_correction_mnl import ln_sampling_probability_for_bias_correction_mnl

class ln_sampling_probability_for_bias_correction_mnl_SSS_DDD_SSS(ln_sampling_probability_for_bias_correction_mnl):
    def __init__(self, part1, part2, part3):
        attribute = "%s_%s_%s" % (part1, part2, part3)
        ln_sampling_probability_for_bias_correction_mnl.__init__(self, attribute)
        
    def dependencies_to_add(self, dataset_name, package=None):
        return ln_sampling_probability_for_bias_correction_mnl.dependencies_to_add(self, dataset_name, 
                                                                                   package="psrc_parcel")
        
