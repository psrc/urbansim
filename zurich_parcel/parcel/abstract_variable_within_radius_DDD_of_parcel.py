# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from scipy.spatial import KDTree
from numpy import array, column_stack, where, arange, zeros

class abstract_variable_within_radius_DDD_of_parcel(Variable):
    """Given quantity within radius DDD of parcel.
       Set the filter to some expression on parcel, if the computation should be done on a filtered
       set of parcels (e.g. for memory reasons).
    """

    quantity = "to_be_defined_in_child_class"
    filter = None
    
    def __init__(self, radius):
        self.radius = radius        
        Variable.__init__(self)
    
    def dependencies(self):
        deps = [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                self.quantity
                ]
        if self.filter is not None:
            deps.append(self.filter)
        return deps

    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        if self.filter is not None:
            index = where(parcels[self.filter] > 0)[0]
        else:
            index = arange(parcels.size())
        arr = parcels[self.quantity][index]
        coords = column_stack( (parcels["x_coord_sp"][index], parcels["y_coord_sp"][index]) )
        kd_tree = KDTree(coords, 100)
        KDTresults = kd_tree.query_ball_tree(kd_tree, self.radius)
        result = zeros(parcels.size(), dtype=arr.dtype)
        tmp = array([arr[l].sum() for l in KDTresults])
        result[index] = tmp
        return result