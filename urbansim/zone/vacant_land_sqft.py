# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class vacant_land_sqft(abstract_sum_from_gridcells):
    """Sum of vacant land values for the zone.
"""
    _return_type = "float32"
    gc_variable = "vacant_land_sqft"
