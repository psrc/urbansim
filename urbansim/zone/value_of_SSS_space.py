# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class value_of_SSS_space(abstract_sum_from_gridcells):
    """ Aggregation over the corresponding gridcell variable """ 

    def __init__(self, type):
        self.gc_variable = "total_value_%s" % type
        abstract_sum_from_gridcells.__init__(self)
