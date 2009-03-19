# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from opus_core.configuration import Configuration


class RunSetConfig(Configuration):
    """Configuration to start multiple runs in parallel
    """
    def __init__(self):
        self['run_set'] = {
                'baseline':'psrc.configs.baseline_copied_travel_data',
                'discounted_travel_data':'psrc.configs.baseline_discounted_travel_data',
                'inflated_travel_data':'psrc.configs.baseline_inflated_travel_data',
                }
        self['travel_data_directory_to_copy'] = '/urbansim_cache/run_1850.2007_01_15_17_03/'  #'/projects/urbansim5/urbansim_cache/run_1849.2007_01_15_16_09/'
