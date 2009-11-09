# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class SSS_improvement_value(abstract_sum_from_gridcells):

    def __init__(self, sss):
        abstract_sum_from_gridcells.__init__(self)
        self.gc_variable = "%s_improvement_value" % sss
