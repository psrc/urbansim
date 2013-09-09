# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import array, zeros, exp
from scipy.spatial import KDTree
from numpy import column_stack
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState

import cPickle as pickle
import os.path

class jobs_within_DDD_of_parcel_weighted(Variable):
    """total number of jobs within radius DDD of parcel weighted by negative exponential euclidian distance function"""
    _return_type = "float64"

    def __init__(self, radius):
        self.radius = radius
        self.cache_file_name = os.path.join(SimulationState().get_cache_directory(), 'jobs_%s.pkl' % radius)
        self.cache_distances_file_name = os.path.join(SimulationState().get_cache_directory(), 'distances_%s.pkl' % radius)
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                "urbansim_parcel.job.parcel_id"
                ]

    def compute(self, dataset_pool):
        with logger.block(name="compute variable jobs_within_DDD_of_parcel_weighted with DDD=%s" % self.radius, verbose=False):
            results = None
            distances = None
            with logger.block(name="trying to read cache files", verbose=False):
                try:
                    results = self._load_results()
                except IOError:
                    logger.log_warning("Cache file %s could not be loaded" % self.cache_file_name)
                try:
                    distances = self._load_distances()
                except IOError:
                    logger.log_warning("Cache file %s could not be loaded" % self.cache_distances_file_name)
    
            with logger.block(name="initialize datasets", verbose=False):
                parcels = self.get_dataset()
                arr = parcels.sum_dataset_over_ids(dataset_pool.get_dataset('job'), constant=1)
    
            if not results or not distances:
                with logger.block(name="initialize coords", verbose=False):
                    coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        
                with logger.block(name="build KDTree", verbose=False):
                    kd_tree = KDTree(coords, 100)
        
                with logger.block(name="compute neighbourhoods and euclidean distances"):
                    results = kd_tree.query_ball_tree(kd_tree, self.radius)
                    distances = kd_tree.sparse_distance_matrix(kd_tree, self.radius)
    
                with logger.block(name="cache neighbourhoods"):
                    if not SimulationState().cache_directory_exists():
                        logger.log_warning("Cache does not exist and is created.")
                        SimulationState().create_cache_directory()
                    self._cache_results(results)
                    self._cache_distances(distances)
                    
            with logger.block(name="Sum weighted jobs in neighbourhood", verbose=False):
#                return_values = array(map(lambda l: arr[l].sum(), results))
                return_values = array(self.euclidean_accessibility_for_parcel(results, distances, arr))
            
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

    def _cache_distances(self, distances): 
        filename = self.cache_distances_file_name
        my_file = open(filename, 'w')
        pickle.dump(distances, my_file)
        my_file.close()

    def _load_distances(self):
        filename = self.cache_distances_file_name
        my_file = open(filename, 'r')
        return pickle.load(my_file)
    
    def euclidean_accessibility_for_parcel(self, neighbourhoods, impedances, jobs):
        weighted_sums = []
        i=0
        for n in neighbourhoods:
            weighted_sum = 0.0
            for e in n:
                weighted_sum = weighted_sum + exp(-impedances[i,e])*jobs[e]
            weighted_sums.append(weighted_sum)
            i+=1
        return weighted_sums

        

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
                "parcel_id":        array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    4 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'job':
            {
                "job_id":array([1,2,3,4,5,6,7]),
                "building_id":array([1,2,3,4,5,6,7]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([3.47151776, 4.87109417, 1.54134113])

        instance_name = 'zurich_parcel.parcel.jobs_within_2_of_parcel_weighted'
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
