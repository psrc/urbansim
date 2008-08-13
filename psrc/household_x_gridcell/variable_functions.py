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

from numpy import ones

def my_attribute_label(attribute_name):
    """Return a string package.dataset_name.attribute_name.
    """
    return "psrc.household_x_gridcell." + attribute_name

def get_mask_for_gridcells(index, n, m):
    """index is an array of size n x m where should be no mask placed."""
    mask = ones((n, m), dtype="int8")
    for i in index:
        mask[i,:] = 0
    return mask
