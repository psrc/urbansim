#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from average_land_value_per_acre_within_walking_distance import average_land_value_per_acre_within_walking_distance

class average_land_value_per_acre_from_buildings_within_walking_distance(average_land_value_per_acre_within_walking_distance):
    """Average land value per acre within walking distance, computed by dividing the 
    total land value within walking distance by the number of acres within walking distance 
    (computed using the buildings dataset). (See implementation of the parent class)
    """

    total_land_value_within_walking_distance = "total_land_value_from_buildings_within_walking_distance"
    