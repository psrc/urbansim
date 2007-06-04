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

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class value_of_SSS_space(abstract_sum_from_gridcells):
    """ Aggregation over the corresponding gridcell variable """ 

    def __init__(self, type):
        self.gc_variable = "total_value_%s" % type
        abstract_sum_from_gridcells.__init__(self)
