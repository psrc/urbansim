# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class number_of_developed_with_buildings_within_walking_distance(abstract_within_walking_distance):
    """Total number of developed locations (computed from buildings) within walking distance of a given gridcell"""
    _return_type = "int32"
    dependent_variable = "is_developed_with_buildings"
