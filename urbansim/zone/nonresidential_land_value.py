# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class nonresidential_land_value(abstract_sum_from_gridcells):
    """Sum of nonresidential land values over zones.
"""
    gc_variable = "nonresidential_land_value"
