#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import arange, bool8, Float, logical_and, logical_or
from numpy import reshape, repeat, ones, zeros, where
from numpy import ma
from opus_core.misc import remove_elements_with_matched_prefix_from_list, remove_all

class ParcelDataset(UrbansimDataset):

    id_name_default = "parcel_id"
    in_table_name_default = "parcels"
    out_table_name_default = "parcels"
    dataset_name = "parcel"

    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        self.development_constraints = None

    def get_development_constraints(self,
            constraints,
            dataset_pool,
            index = None,
            recompute_flag = False,
            variable_package_name="psrc_parcel.parcel"
            ):
        """
        calculate the min and max development capacity given by constraints.
        """
        if (self.development_constraints <> None) and (not recompute_flag):
            if (index <> None) and alltrue(self.development_constraints["index"] == index):
                return self.development_constraints
        constraints.load_dataset_if_not_loaded()
        attributes = set(constraints.get_attribute_names()) - \
                   set([constraints.get_id_name()[0], "building_type_id", "min_constraint", "max_constraint"])
        attributes_with_prefix = map(lambda attr: "%s.%s" % (variable_package_name, attr),
                                        attributes)
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

        self.development_constraints = {"index": index}
        building_types = dataset_pool.get_dataset("building_type")
        type_ids = constraints.get_attribute("building_type_id")
        #initialize results, set max to the max value found in constraints for each type
        for type_id in building_types.get_id_attribute():
            self.development_constraints.update({type_id:zeros((index.size,2), dtype=Float)})
            w_this_type = where(type_ids == type_id)
            type_constraint_max = constraints.get_attribute("max_constraint")[w_this_type].max()
            self.development_constraints[type_id][:, 1] = type_constraint_max

        for iconstr in range(constraints.size()):
            type_id = type_ids[iconstr]
            w = where(development_constraints_array[iconstr,:])[0]
            if w.size > 0:
                self.development_constraints[type_id][w,0] = \
                    ma.maximum(self.development_constraints[type_id][w,0],
                        constraints.get_attribute_by_index("min_constraint", iconstr))
                self.development_constraints[type_id][w,1] = \
                    ma.minimum(self.development_constraints[type_id][w,1],
                        constraints.get_attribute_by_index("max_constraint", iconstr))

        return self.development_constraints

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_get_development_constraints(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage._write_dataset(
            'building_types',
            {
                "building_type_id":array([1, 2]),
                'density_name':   array(['units_per_acre','far']),
                'constraint_name':array(['units_per_acre','far']),
            }
        )

        storage._write_dataset(
            'development_constraints',
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'building_type_id': array([1, 1, 2, 2]),
                'min_constraint': array([0,  0,   2,  0]),
                'max_constraint': array([3, 0.2, 10, 100]),
            }
        )
        storage._write_dataset(
            'parcels',
            {
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   0,    1]),
            }
        )

        dataset_pool = DatasetPool(package_order=['psrc_parcel','urbansim'],
                                   storage=storage)

        parcels = dataset_pool.get_dataset('parcel')
        constraints = dataset_pool.get_dataset('development_constraint')

        values = parcels.get_development_constraints(constraints, dataset_pool)

        should_be = {1:array([[0,0.2],
                              [0, 3],
                              [0,0.2]]
                              ),
                     2:array([[2,10],
                              [0,100],
                              [2,10]])
                          }
        for key, should_be_value in should_be.iteritems():
            self.assert_(key in values)
            self.assert_(ma.allclose(values[key], should_be_value),
                         msg = "Error in parcel get_development_constraints")


if __name__=='__main__':
    opus_unittest.main()