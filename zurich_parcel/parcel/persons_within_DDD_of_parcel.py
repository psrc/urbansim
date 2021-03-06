# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros
from numpy import array
from scipy.spatial import KDTree
from numpy import column_stack
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState

import cPickle as pickle
import os.path

class persons_within_DDD_of_parcel(Variable):
    """total number of persons within radius DDD of parcel"""
    _return_type = "int32"

    def __init__(self, radius):
        self.radius = radius
        self.cache_file_name = os.path.join(SimulationState().get_cache_directory(), 'persons_%s.pkl' % radius)
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                "urbansim_parcel.household.parcel_id",
                "urbansim_parcel.household.persons"
                ]

    def compute(self, dataset_pool):
        with logger.block(name="compute variable persons_within_DDD_of_parcel with DDD=%s" % self.radius, verbose=False):
            results = None
            with logger.block(name="trying to read cache file %s" % self.cache_file_name, verbose=False):
                try:
                    results = self._load_results()
                except IOError:
                    logger.log_warning("Cache file could not be loaded")
    
            with logger.block(name="initialize datasets", verbose=False):
                parcels = self.get_dataset()
                arr = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('household'), attribute_name="persons")
    
            if not results:
                with logger.block(name="initialize coords", verbose=False):
                    coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        
                with logger.block(name="build KDTree", verbose=False):
                    kd_tree = KDTree(coords, 100)
        
                with logger.block(name="compute"):
                    results = kd_tree.query_ball_tree(kd_tree, self.radius)
    
                with logger.block(name="cache"):
                    if not SimulationState().cache_directory_exists():
                        logger.log_warning("Cache does not exist and is created.")
                        SimulationState().create_cache_directory()
                    self._cache_results(results)
                    
            with logger.block(name="sum results", verbose=False):
                return_values = array(map(lambda l: arr[l].sum(), results))
            
        return return_values

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

    def _cache_results(self, results): 
        filename = self.cache_file_name
        my_file = open(filename, 'w')
        pickle.dump(results, my_file)
        my_file.close()

    def _load_results(self):
        filename = self.cache_file_name
        my_file = open(filename, 'r')
        return pickle.load(my_file)

        

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['zurich_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id": array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    3 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'household':
            {
                "household_id":array([1,2,3,4,5,6,7]),
                "persons":array([3,5,2,2,2,1,3]),
                "building_id":array([1,2,3,4,5,6,7]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([15, 18, 14])

        instance_name = 'zurich_parcel.parcel.persons_within_1_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
