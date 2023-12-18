# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .abstract_within_DDD_radius import abstract_within_DDD_radius


class SSS_within_DDD_radius(abstract_within_DDD_radius):
    """sum given variable within DDD radius.
"""
    # mode='constant' # zeros on edges
    
    def __init__(self, name, radius):
        self.dependent_variable = "gridcell.aggregate(psrc_parcel.parcel.%s)" % name        
        abstract_within_DDD_radius.__init__(self, radius)

