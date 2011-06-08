# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.ndimage import correlate
from numpy import ma, where, ones, float32
from scipy.ndimage import distance_transform_edt
from opus_core.variables.variable import Variable

class abstract_within_DDD_radius(Variable):
    """Abstract variable for any '_in_neighborhood' variable within DDD radius.
"""
    _return_type= "float32"
    dependent_variable = "not_defined" # to be defined in the child class (must be defined for a gridcell dataset)
    filled_value = 0.0 # value that goes to the masked spots
    mode = "reflect" # mode for the 'correlate' function

    def __init__(self, radius):
        self.radius = radius        
        Variable.__init__(self)
        
    def dependencies(self):
        return [self.dependent_variable]

    def compute(self, dataset_pool):
        footprint = self.get_neighborhood_footprint(dataset_pool)
        ds = self.get_dataset()
        summed = correlate( ma.filled( ds.get_2d_attribute( self.dependent_variable ),
                                      self.filled_value ).astype(self._return_type),
                            footprint, mode=self.mode)
        return ds.flatten_by_id( summed )

    def get_neighborhood_footprint(self, dataset_pool):
        cell_size = dataset_pool.get_dataset('urbansim_constant')["cell_size"]
        wd_gc = int(2*self.radius/cell_size+1)
        distance = ones((wd_gc,wd_gc), dtype=float32)
        center = (wd_gc-1)/2
        distance[center,center]=0.0
        distance = distance_transform_edt(distance)
        return where(distance*cell_size <= self.radius, 1, 0)
