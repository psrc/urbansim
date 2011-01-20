# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.model import Model
from opus_core.misc import ncumsum, unique
from numpy.random import random
from numpy import searchsorted, where, ones, allclose
from opus_core.sampling_toolbox import normalize
                
class MonteCarloAssignmentModel(Model):
    """Assign individuals from one geography (dataset1) to another (dataset2) with
    probablity equal to fractions of dataset1 in dataset2 through a Monte Carlo process.
    
    For Example, assign individual households from blockgroup to zone by the fractions
    of blockgroup in zones.  See unittest below for details.
    """
    
    model_name = "Monte Carlo Assignment Model"
    model_short_name = "MCAM"

    def run(self, individual_dataset, fraction_dataset, id_name1='blockgroup_id', 
            id_name2='zone_id', fraction_attribute_name='fraction'):
        
        """
        """
        assert id_name1 in individual_dataset.get_known_attribute_names()
        if id_name2 not in individual_dataset.get_known_attribute_names():           
            individual_dataset.add_primary_attribute(-1*ones(individual_dataset.size(), dtype=fraction_dataset.get_attribute(id_name2).dtype), 
                                                     id_name2)
        fraction_id1 = fraction_dataset.get_attribute(id_name1)
        individual_id1 = individual_dataset.get_attribute(id_name1)
        unique_ids = unique(fraction_id1)
        
        for id1 in unique_ids:
            individual_of_id1 = where(individual_id1==id1)[0]
            n = individual_of_id1.size
            logger.log_status("Processing %s %s: %s individuals" % (id_name1, id1, n) )
            if n > 0:
                fractions = fraction_dataset.get_attribute(fraction_attribute_name)[fraction_id1==id1]
                id2 = fraction_dataset.get_attribute(id_name2)[fraction_id1==id1]
                ## ignore households in geography with sum of fractions less than 1.0e-6
                if fractions.sum() < 1.0e-2:
                    continue
                if not allclose(fractions.sum(), 1.0, rtol=1.e-2):
                    fractions = normalize(fractions)
                fractions_cumsum = ncumsum(fractions)
                R = random(n)
                index = searchsorted(fractions_cumsum, R)
                individual_dataset.modify_attribute(id_name2, id2[index], index=individual_of_id1)
                
        #individual_dataset.flush_dataset()

            
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, allclose, sort
import tempfile, os, shutil
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.tests.stochastic_test_case import StochasticTestCase

class MonteCarloAssignmentModelTest(StochasticTestCase):
    def setUp(self):
        household_data = {
            'household_id':  array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'blockgroup_id': array([1, 1, 1, 1, 2, 2, 2, 2, 2, 3]),
        }
        fraction_data = {
            'fraction_id':                array([1,    2,    3,   4,   5,   6,   6]), #unused, but necessary to use dataset_pool to get data
            'blockgroup_id':              array([1,    1,    1,   2,   2,   2,   3]),
            'zone_id':                    array([1,    2,    3,   3,   4,   5,   6]),
            'fraction':                   array([0.25, 0.25, 0.5, 0.2, 0.4, 0.4, 1.0])
            }
        blockgroup_data = {
            #unused by the model, for result verification only
            'blockgroup_id':              array([1,    2,   3]),
            }
        zone_data = {
            #unused by the model, for result verification only
            'zone_id':                    array([1,    2,    3,   4,  5,  6]),
            }

        self.tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')

        SimulationState().set_cache_directory(self.tmp_dir)
        attribute_cache = AttributeCache()
        self.dataset_pool = SessionConfiguration(new_instance=True,
                                                 package_order=['urbansim', 'opus_core'],
                                                 in_storage=attribute_cache).get_dataset_pool()        

        #storage = StorageFactory().get_storage('flt_storage', storage_location=self.tmp_dir)
        attribute_cache.write_table(table_name = 'households', table_data = household_data)
        attribute_cache.write_table(table_name = 'fractions', table_data = fraction_data)
        attribute_cache.write_table(table_name = 'blockgroups', table_data = blockgroup_data)
        attribute_cache.write_table(table_name = 'zones', table_data = zone_data)
        
        #self.dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim', 'opus_core'])
        self.household = self.dataset_pool.get_dataset('household')
        self.fraction = self.dataset_pool.get_dataset('fraction')
        self.blockgroup = self.dataset_pool.get_dataset('blockgroup')
        self.zone = self.dataset_pool.get_dataset('zone')        

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        
    def test_aggregate(self):
        model = MonteCarloAssignmentModel()
        def run_model():
            model.run(self.household, self.fraction, id_name1='blockgroup_id', 
                  id_name2='zone_id', fraction_attribute_name='fraction')
            hhs_by_zone = self.zone.compute_variables('zone.number_of_agents(household)')
            return hhs_by_zone
        
        #print expected_results      
        expected_results = array([1, 1, 3, 2, 2, 1])
        iterations = 10
        self.run_stochastic_test(__file__, run_model, expected_results, 
                                 iterations, significance_level=0.05, 
                                 transformation=None)
    def test_individual(self):
        model = MonteCarloAssignmentModel()
        def run_model():
            model.run(self.household, self.fraction, id_name1='blockgroup_id', 
                  id_name2='zone_id', fraction_attribute_name='fraction')
            zone_id = self.household.get_attribute('zone_id')
            return zone_id

        iterations = 10
        expected_results1 = array([3, 3, 3, 3,  4, 4, 4, 4, 4,  6])  #highest prob locations
        self.run_stochastic_test(__file__, run_model, expected_results1, 
                                 iterations, significance_level=0.05, 
                                 transformation=None)
        
        #expected_results2 = array([6, 5, 5, 4, 4, 3, 3, 3, 2, 1])
        #self.run_stochastic_test(__file__, run_model, expected_results2, 
                                 #iterations, significance_level=0.05, 
                                 #transformation=None)

        #unexpected_results = array([3, 3, 3, 4,  1, 4, 4, 4, 4,  6])
        #self.run_stochastic_test(__file__, run_model, unexpected_results, 
                                 #iterations, significance_level=0.05, 
                                 #transformation=None, expected_to_fail=True)
        
    def test_post_checks(self):
        model = MonteCarloAssignmentModel()
        model.run(self.household, self.fraction, id_name1='blockgroup_id', 
              id_name2='zone_id', fraction_attribute_name='fraction')
        
        self.assertTrue('zone_id' in self.household.get_known_attribute_names())
        hhs_by_bg = self.blockgroup.compute_variables('blockgroup.number_of_agents(household)')
        self.assertTrue(all(hhs_by_bg==array([4, 5, 1])))
        
if __name__=="__main__":
    opus_unittest.main()
