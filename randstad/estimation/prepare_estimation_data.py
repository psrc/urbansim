# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.cache.cache_scenario_database import CacheScenarioDatabase

"""
This script creates a new urbansim_cache and populates it with all 
the tables_to_cache, the lag data, and unrolled gridcells.
It only needs to be run when you need to create or update a cache.
Once the cache is there, you can keep reusing it, e.g. for estimation.
"""

from randstad.estimation.estimation_config import config
CacheScenarioDatabase().run(config, unroll_gridcells=False)

