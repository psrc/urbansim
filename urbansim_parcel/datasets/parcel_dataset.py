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
from opus_core.misc import unique_values
from numpy import arange, logical_and, logical_or, alltrue
from numpy import reshape, repeat, ones, zeros, where
from numpy import maximum, minimum
from opus_core.logger import logger
from opus_core.variables.variable_name import VariableName

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
            variable_package_name="urbansim_parcel.parcel"
            ):
        """
        calculate the min and max development capacity given by constraints.
        modelled from the method of gridcell
        """
        if (self.development_constraints <> None) and (not recompute_flag):
            if (index <> None) and alltrue(self.development_constraints["index"] == index):
                return self.development_constraints
        constraints.load_dataset_if_not_loaded()
        attributes = set(constraints.get_attribute_names()) - \
                   set([constraints.get_id_name()[0], "generic_land_use_type_id", "constraint_type", "minimum", "maximum"])
        attributes_with_prefix = map(lambda attr: "%s.%s" % (variable_package_name, attr),
                                        attributes)
        self.compute_variables(attributes_with_prefix, dataset_pool=dataset_pool)
        attributes = map(lambda attr: VariableName(attr), attributes)
        
        if index == None:
            index = arange(self.size())

        self.development_constraints = {"index": index}
#        building_types = dataset_pool.get_dataset("building_type")
        type_ids = constraints.get_attribute("generic_land_use_type_id")
        constraint_types = constraints.get_attribute("constraint_type")
        constraint_minimum = constraints.get_attribute("minimum")
        constraint_maximum = constraints.get_attribute("maximum")
        #initialize results, set max to the max value found in constraints for each type
        for type_id in unique_values(type_ids):
            w_this_type = where(type_ids == type_id)
            self.development_constraints[type_id] = {}
            for constraint_type in unique_values(constraint_types[w_this_type]):
                self.development_constraints[type_id].update({ constraint_type : zeros((index.size,2), dtype="float32") })
                w_this_type_and_constraint_type = where( logical_and(type_ids == type_id, constraint_types == constraint_type ) )
                # initialize the maximum value, because minimum of maximum value below need to have this initial value to work
                type_constraint_max = constraint_maximum[w_this_type_and_constraint_type].max()
                self.development_constraints[type_id][constraint_type][:, 1] = type_constraint_max

        self.development_constraints_array = None
        self.large_constraint_array = False
        
        logger.start_block("Matching %s development constraints to %s parcels" % (constraints.size(), index.size))
        for iconstr in xrange(constraints.size()):
            type_id = type_ids[iconstr]
            constraint_type = constraint_types[iconstr]
            w = where(self._get_one_constraint(iconstr, constraints, index, attributes))[0]
            if w.size > 0: #has at least 1 match
                ##TODO: this may be problematic when given building type and constraint type of 
                ## a parcel doesn't match to any row of the constraints table, it'll use the max value
                ## of the building type and constraint type
                self.development_constraints[type_id][constraint_type][w,0] = \
                    maximum(self.development_constraints[type_id][constraint_type][w,0],
                        constraint_minimum[iconstr])
                self.development_constraints[type_id][constraint_type][w,1] = \
                    minimum(self.development_constraints[type_id][constraint_type][w,1],
                        constraint_maximum[iconstr])
        logger.end_block()
        del self.development_constraints_array
        return self.development_constraints

    def _get_one_constraint(self, iconstr, constraints, index, attributes):
        if self.development_constraints_array is None:
            try:
                self.development_constraints_array = ones((constraints.size(),index.size), dtype='bool8')
                for attr in attributes:
                    values = self.get_attribute_by_index(attr, index)
                    constr = reshape(constraints.get_attribute(attr), (constraints.size(),1))
                    constr = repeat(constr, index.size, axis=1)
                    tmp = logical_or(constr == values, constr < 0)
                    self.development_constraints_array = logical_and(self.development_constraints_array, tmp)
            except (MemoryError, ValueError):
                self.large_constraint_array=True
                self.development_constraints_array = ones(index.size, dtype='bool8')
                
        if not self.large_constraint_array:
            return self.development_constraints_array[iconstr,:]
        
        self.development_constraints_array[:] = True
        for attr in attributes:
            values = self.get_attribute(attr)[index]
            constr = constraints.get_attribute(attr)[iconstr]
            self.development_constraints_array = logical_and(self.development_constraints_array, 
                                                             logical_or(constr == values, constr < 0))
        return self.development_constraints_array
            
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_get_development_constraints(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='land_use_types',
            table_data={
                "land_use_type_id":array([1, 2]),
                'density_name':   array(['units_per_acre','far']),
                'constraint_name':array(['units_per_acre','far']),
            }
        )

        storage.write_table(
            table_name='development_constraints',
            table_data={
                'constraint_id': array([1,  2, 3, 4, 5, 6, 7]),
                'is_constrained': array([0, 0, 1, 1, 1, 0, 0]),
                'generic_land_use_type_id': array([1, 1, 1, 1, 2, 2, 2]),
                'constraint_type': array(["unit_per_acre","far","unit_per_acre", "far", "far", "unit_per_acre", "far"]),
                'minimum': array([0, 0,  0,  0,  2,  0, 0]),
                'maximum': array([3, 0, 0.2, 1,  10, 0.4, 100]),
            }
        )
        storage.write_table(
            table_name='parcels',
            table_data={
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   0,    1]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim_parcel','urbansim'],
                                   storage=storage)

        parcels = dataset_pool.get_dataset('parcel')
        constraints = dataset_pool.get_dataset('development_constraint')

        values = parcels.get_development_constraints(constraints, dataset_pool)

        should_be = { 1:{"unit_per_acre":array([[0,0.2],
                                                [0, 3],
                                                [0,0.2]]
                                              ),
                         "far":array([[0, 1],
                                     [0,  0],
                                     [0,  1]]
                                     ),                              
                           },
                      2:{"unit_per_acre":array([[0, 0.4],  #ideally [0, 0]
                                                [0, 0.4],
                                                [0, 0.4]]     #ideally [0, 0]
                                               ),
                         "far":array([[2,10],
                                     [0, 100],
                                     [2, 10]]
                                     )         
                          }
                     }
        
        for bt, ct in should_be.iteritems():
            for key, should_be_value in ct.iteritems():
                self.assert_(bt in values)
                self.assert_(key in values[bt])
                self.assert_(ma.allclose(values[bt][key], should_be_value),
                             msg = "Error in parcel get_development_constraints")

if __name__=='__main__':
    opus_unittest.main()