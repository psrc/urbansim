# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset import Dataset
from numpy import maximum, zeros, float32, ones, where, arange, logical_and, logical_or, bool8
from numpy import reshape, repeat, alltrue
from numpy import ma
from opus_core.misc import DebugPrinter
from opus_core.misc import remove_elements_with_matched_prefix_from_list, remove_all

class GridcellDataset(UrbansimDataset):
    """Set of gridcells."""

    id_name_default = "grid_id"
    in_table_name_default = "gridcells"
    out_table_name_default = "gridcells"
    dataset_name = "gridcell"
    _coordinate_system = ('relative_x', 'relative_y')

    def __init__(self, *args, **kwargs):

        UrbansimDataset.__init__(self, *args, **kwargs)
        self.development_capacity = None

    def get_development_constrained_capacity(self,
            constraints,
            dataset_pool,
            index = None,
            recompute_flag = False,
            maximum_commercial_development_capacity = 4000000, ### TODO: Remove this default value and require this parameter.
            maximum_industrial_development_capacity = 1200000, ### TODO: Remove this default value and require this parameter.
            maximum_residential_development_capacity = 2800, ### TODO: Remove this default value and require this parameter.
            ):
        """
        Truncate the development capacity to the range
        min <= development capacity <= max, as defined by the given constraints.
        """
        if (self.development_capacity <> None) and (not recompute_flag):
            if (index <> None) and (index.size == self.development_capacity["index"].size) and \
                    alltrue(self.development_capacity["index"] == index):
                return self.development_capacity
        constraints.load_dataset_if_not_loaded()
        attributes = remove_elements_with_matched_prefix_from_list(
            constraints.get_attribute_names(), ["min", "max"])
        attributes = remove_all(attributes, constraints.get_id_name()[0])
        attributes_with_prefix = map(lambda attr: "urbansim.gridcell." +
                                        attr, attributes)
        self.compute_variables(attributes_with_prefix, dataset_pool=dataset_pool)
        if index == None:
            index = arange(self.size())
        development_constraints_array = ones((constraints.size(),index.size), dtype=bool8)
        for attr in attributes:
            values = self.get_attribute_by_index(attr, index)
            constr = reshape(constraints.get_attribute(attr), (constraints.size(),1))
            constr = repeat(constr, index.size, axis=1)
            tmp = logical_or(constr == values, constr < 0)
            development_constraints_array = logical_and(development_constraints_array, tmp)

        self.development_capacity = {
            "commercial":zeros((index.size,2)),
            "residential":zeros((index.size,2)), 
            "industrial":zeros((index.size,2)),
            "index": index,
        }

        #reasonable maxima
        self.development_capacity["commercial"][:,1] = maximum_commercial_development_capacity
        self.development_capacity["industrial"][:,1] = maximum_industrial_development_capacity
        self.development_capacity["residential"][:,1] = maximum_residential_development_capacity
        for iconstr in range(constraints.size()):
            w = where(development_constraints_array[iconstr,:])[0]
            if w.size > 0:
                self.development_capacity["commercial"][w,0] = \
                    maximum(self.development_capacity["commercial"][w,0], \
                        constraints.get_attribute_by_index("min_commercial_sqft", iconstr))
                self.development_capacity["commercial"][w,1] = \
                    ma.minimum(self.development_capacity["commercial"][w,1], \
                        constraints.get_attribute_by_index("max_commercial_sqft", iconstr))
                self.development_capacity["industrial"][w,0] = \
                    maximum(self.development_capacity["industrial"][w,0], \
                        constraints.get_attribute_by_index("min_industrial_sqft", iconstr))
                self.development_capacity["industrial"][w,1] = \
                    ma.minimum(self.development_capacity["industrial"][w,1], \
                        constraints.get_attribute_by_index("max_industrial_sqft", iconstr))
                self.development_capacity["residential"][w,0] = \
                    maximum(self.development_capacity["residential"][w,0], \
                        constraints.get_attribute_by_index("min_units", iconstr))
                self.development_capacity["residential"][w,1] = \
                    ma.minimum(self.development_capacity["residential"][w,1], \
                        constraints.get_attribute_by_index("max_units", iconstr))

        return self.development_capacity