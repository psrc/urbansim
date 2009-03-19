# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import ones

def get_mask_for_gridcells(index, n, m):
    """index is an array of size n x m where should be no mask placed."""
    mask = ones((n, m))
    for i in index:
        mask[i,:] = 0
    return mask
