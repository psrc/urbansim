#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from abstract_within_walking_distance import abstract_within_walking_distance

class number_of_developed_with_buildings_within_walking_distance(abstract_within_walking_distance):
    """Total number of developed locations (computed from buildings) within walking distance of a given gridcell"""
    _return_type = "int32"
    dependent_variable = "is_developed_with_buildings"
