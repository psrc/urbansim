# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.model_coordinators.cache_scenario_database import CacheScenarioDatabase
from opus_core.session_configuration import SessionConfiguration

"""
This script creates a new urbansim_cache and populates it with all 
the tables_to_cache, the lag data, and unrolled gridcells.
It only needs to be run when you need to create or update a cache.
Once the cache is there, you can keep reusing it, e.g. for estimation.
"""

from washtenaw.estimation.my_estimation_config import run_configuration
CacheScenarioDatabase().run(run_configuration)

