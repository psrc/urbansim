# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .abstract_sum_from_gridcells import abstract_sum_from_gridcells

class total_maximum_development_SSS(abstract_sum_from_gridcells):
    _return_type = "int32"
    
    def __init__(self, sss):
        abstract_sum_from_gridcells.__init__(self)
        self.gc_variable = "total_maximum_development_" + sss

        