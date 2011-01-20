# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from scipy.spatial import KDTree
from numpy import column_stack

class abstract_distance_to_SSS_dataset(Variable):
    """distance of a dataset centroid to nearest SSS dataset point.
    """
    _return_type = "float32"
    
    dataset_x_coord = "x_coord"
    dataset_y_coord = "y_coord"
    my_x_coord = "x_coord"
    my_y_coord = "y_coord"
    package = "urbansim"
    from_dataset = "gridcell"
    
    def __init__(self, to_dataset):
        self.to_dataset = to_dataset
        Variable.__init__(self)
    
    def dependencies(self):
        return ["%s.%s.%s" % (self.package, self.from_dataset, self.my_x_coord),
                "%s.%s.%s" % (self.package, self.from_dataset, self.my_y_coord)]

    def compute(self, dataset_pool):
        loc = dataset_pool.get_dataset(self.to_dataset)
        self.add_and_solve_dependencies(["%s.%s" % (self.to_dataset, self.dataset_x_coord), 
                                         "%s.%s" % (self.to_dataset, self.dataset_y_coord)], 
                                        dataset_pool=dataset_pool)
        pgcoords = column_stack( (loc.get_attribute(self.dataset_x_coord), 
                                  loc.get_attribute(self.dataset_y_coord)) )
        ds = self.get_dataset()
        coords = column_stack( (ds.get_attribute(self.my_x_coord), 
                                ds.get_attribute(self.my_y_coord)) )
        kd_tree = KDTree(pgcoords, 10)
        distances, indices = kd_tree.query(coords)
        return distances

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

