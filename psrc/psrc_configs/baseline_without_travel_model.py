# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from psrc.configs.baseline import Baseline

run_configuration = Baseline()
del run_configuration['travel_model_configuration']
run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = 'e:/urbansim_cache'