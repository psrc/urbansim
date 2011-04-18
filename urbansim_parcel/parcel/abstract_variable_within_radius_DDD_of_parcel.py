# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from scipy.spatial import KDTree
from numpy import array, column_stack

class abstract_variable_within_radius_DDD_of_parcel(Variable):
    """Given quantity within radius DDD of parcel"""

    quantity = "to_be_defined_in_child_class"
    
    def __init__(self, radius):
        self.radius = radius        
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                self.quantity
                ]

    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        arr = parcels[self.quantity]
        coords = column_stack( (parcels["x_coord_sp"], parcels["y_coord_sp"]) )
        kd_tree = KDTree(coords, 100)
        results = kd_tree.query_ball_tree(kd_tree, self.radius)
        return array(map(lambda l: arr[l].sum(), results))
