# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.misc import unique_values
from numpy import arange, logical_and, logical_or
from numpy import reshape, repeat, ones, zeros, where, alltrue
from numpy import ma

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
                   set([constraints.get_id_name()[0], "generic_building_type_id", "constraint_type", "minimum", "maximum"])
        attributes_with_prefix = map(lambda attr: "%s.%s" % (variable_package_name, attr),
                                        attributes)
        self.compute_variables(attributes_with_prefix, dataset_pool=dataset_pool)
        if index == None:
            index = arange(self.size())
        # constraints are specified for each generic_building_type, 
        development_constraints_array = ones((constraints.size(),index.size), dtype='bool8')
        for attr in attributes:
            values = self.get_attribute_by_index(attr, index)
            constr = reshape(constraints.get_attribute(attr), (constraints.size(),1))
            constr = repeat(constr, index.size, axis=1)
            tmp = logical_or(constr == values, constr < 0)
            development_constraints_array = logical_and(development_constraints_array, tmp)

        self.development_constraints = {"index": index}
#        building_types = dataset_pool.get_dataset("building_type")
        type_ids = constraints.get_attribute("generic_building_type_id")
        constraint_types = constraints.get_attribute("constraint_type")
        #initialize results, set max to the max value found in constraints for each type
        for type_id in unique_values(type_ids):
            w_this_type = where(type_ids == type_id)
            self.development_constraints[type_id] = {}
            for constraint_type in unique_values(constraint_types[w_this_type]):
                self.development_constraints[type_id].update({ constraint_type : zeros((index.size,2), dtype="float32") })
                w_this_type_and_constraint_type = where( logical_and(type_ids == type_id, constraint_types == constraint_type ) )
                # initialize the maximum value, because minimum of maximum value below need to have this initial value to work
                type_constraint_max = constraints.get_attribute("maximum")[w_this_type_and_constraint_type].max()
                self.development_constraints[type_id][constraint_type][:, 1] = type_constraint_max

        for iconstr in range(constraints.size()):
            type_id = type_ids[iconstr]
            constraint_type = constraint_types[iconstr]
            w = where(development_constraints_array[iconstr,:])[0]
            if w.size > 0: #has at least 1 match
                ##TODO: this may be problematic when given building type and constraint type of 
                ## a parcel doesn't match to any row of the constraints table, it'll use the max value
                ## of the building type and constraint type
                self.development_constraints[type_id][constraint_type][w,0] = \
                    ma.maximum(self.development_constraints[type_id][constraint_type][w,0],
                        constraints.get_attribute_by_index("minimum", iconstr))
                self.development_constraints[type_id][constraint_type][w,1] = \
                    ma.minimum(self.development_constraints[type_id][constraint_type][w,1],
                        constraints.get_attribute_by_index("maximum", iconstr))

        return self.development_constraints

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_get_development_constraints(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='building_types',
            table_data={
                "building_type_id":array([1, 2]),
                'density_name':   array(['units_per_acre','far']),
                'constraint_name':array(['units_per_acre','far']),
            }
        )

        storage.write_table(
            table_name='development_constraints',
            table_data={
                'constraint_id': array([1,  2, 3, 4, 5, 6, 7]),
                'is_constrained': array([0, 0, 1, 1, 1, 0, 0]),
                'generic_building_type_id': array([1, 1, 1, 1, 2, 2, 2]),
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

        dataset_pool = DatasetPool(package_order=['pag_parcel','urbansim'],
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