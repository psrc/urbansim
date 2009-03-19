# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
