# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from average_land_value_per_acre_within_walking_distance import average_land_value_per_acre_within_walking_distance

class average_land_value_per_acre_from_buildings_within_walking_distance(average_land_value_per_acre_within_walking_distance):
    """Average land value per acre within walking distance, computed by dividing the 
    total land value within walking distance by the number of acres within walking distance 
    (computed using the buildings dataset). (See implementation of the parent class)
    """

    total_land_value_within_walking_distance = "total_land_value_from_buildings_within_walking_distance"
    