# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from scipy.spatial import KDTree
from numpy import column_stack, arange, where

class abstract_nearest_element_of_SSS_dataset(Variable):
    """distance of a dataset centroid to nearest SSS dataset point.
    """
    _return_type = "int32"
    
    dataset_x_coord = "x_coord"
    dataset_y_coord = "y_coord"
    my_x_coord = "x_coord"
    my_y_coord = "y_coord"
    package = "urbansim"
    from_dataset = "gridcell"
    filter = None # expression to filter out the SSS dataset
    
    def __init__(self, to_dataset):
        self.to_dataset = to_dataset
        Variable.__init__(self)
    
    def dependencies(self):
        return ["%s.%s.%s" % (self.package, self.from_dataset, self.my_x_coord),
                "%s.%s.%s" % (self.package, self.from_dataset, self.my_y_coord)]
        
    def _compute(self, dataset_pool):
        loc = dataset_pool.get_dataset(self.to_dataset)
        xdep = "%s" % self.dataset_x_coord
        if VariableName(self.dataset_x_coord).get_dataset_name() is None:
            xdep = "%s.%s" % (self.to_dataset, xdep)
        ydep = "%s" % self.dataset_y_coord
        if VariableName(self.dataset_y_coord).get_dataset_name() is None:
            ydep = "%s.%s" % (self.to_dataset, ydep)
            
        self.add_and_solve_dependencies([xdep, ydep], 
                                        dataset_pool=dataset_pool)
        if self.filter is not None:
            self.add_and_solve_dependencies(["%s" % self.filter], dataset_pool=dataset_pool)
            index = where(loc[VariableName(self.filter).get_alias()])[0]
        else:
            index = arange(loc.size())
        pgcoords = column_stack( (loc.get_attribute(self.dataset_x_coord)[index], 
                                  loc.get_attribute(self.dataset_y_coord)[index]) )
        ds = self.get_dataset()
        coords = column_stack( (ds.get_attribute(self.my_x_coord), 
                                ds.get_attribute(self.my_y_coord)) )
        kd_tree = KDTree(pgcoords, 10)
        return kd_tree.query(coords), index

    def compute(self, dataset_pool):
        result =  self._compute(dataset_pool)
        return result[0][1]
    
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

