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

class value_of_SSS_space_within_walking_distance(abstract_within_walking_distance):
    """Sum of given units of locations within walking distance of this gridcell"""
    
    def __init__(self, type):
        self.dependent_variable = "total_value_%s" % type
        abstract_within_walking_distance.__init__(self)
