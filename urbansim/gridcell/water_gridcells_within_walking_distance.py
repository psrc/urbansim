# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class water_gridcells_within_walking_distance(abstract_within_walking_distance):
    """Number of gridcells that are fully in water within walking distance of this gridcell"""

    _return_type = "int32"
    dependent_variable = "is_fully_in_water"

