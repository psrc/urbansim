# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.cache.cache_scenario_database import CacheScenarioDatabase

"""
This script creates a new urbansim_cache and populates it with all 
the tables_to_cache, the lag data, and unrolled gridcells.
It only needs to be run when you need to create or update a cache.
Once the cache is there, you can keep reusing it, e.g. for estimation.
"""

from randstad.estimation.estimation_config import config
CacheScenarioDatabase().run(config, unroll_gridcells=False)

