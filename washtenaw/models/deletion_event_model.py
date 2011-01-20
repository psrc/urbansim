# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, where, resize
from opus_core.model import Model
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.logger import logger

class DeletionEventModel(Model):
    """ Removes jobs and households from their locations according to the deletion_events table.
    """
    model_name = "Deletion Event Model"
          
    def run(self, location_set, deletion_event_set, current_year, dataset_pool=None):
        """ The deletion_event_set is expected to have attributes:
                grid_id, scheduled_year, number_of_jobs, number_of_households
            The method finds jobs/househods located in the given locations (grid_id),
            then samples the given amount for this year and unplaces them.
            If the value for number_of_jobs/number_of_households is -2, the model removes 
            all jobs/households from the location.
        """
        if not deletion_event_set or (deletion_event_set.size() == 0): 
            logger.log_status("No jobs/households to be deleted.")
            return

        idx_of_events_this_year = deletion_event_set.get_attribute("scheduled_year") == current_year
        if idx_of_events_this_year.sum() == 0:
            logger.log_status("No jobs/households to be deleted.")
            return
        
        self.dataset_pool = self.create_dataset_pool(dataset_pool)
        
        location_id_name = location_set.get_id_name()[0]
        location_ids_in_event_set = deletion_event_set.get_attribute_by_index(location_id_name, 
                                                                              idx_of_events_this_year)
        
        agents_dict = {"number_of_jobs": "job", "number_of_households": "household"}
        # load attributes and datasets needed
        delete_agents = {"job": False, "household": False}
        agent_sets = {}
        for attribute_name, dataset_name in agents_dict.iteritems():
            if attribute_name in deletion_event_set.get_known_attribute_names():
                values = deletion_event_set.get_attribute_by_index(attribute_name, idx_of_events_this_year)
                if values.sum() > 0:
                    agent_sets[dataset_name] = self.dataset_pool.get_dataset(dataset_name)
                    if location_id_name not in agent_sets[dataset_name].get_known_attribute_names():
                        # compute agents locations
                        agent_sets[dataset_name].compute_one_variable_with_unknown_package(location_id_name, 
                                                                                           self.dataset_pool)
                    delete_agents[dataset_name] = True
                    
        for attribute_name, dataset_name in agents_dict.iteritems():
            if not delete_agents[dataset_name]:
                continue
            # iterate over locations
            for location_id in location_ids_in_event_set:
                number_of_agents = eval("deletion_event_set.get_data_element_by_id((location_id, current_year)).%s" % attribute_name)
                agent_ids = agent_sets[dataset_name].get_attribute(location_id_name)
                agent_index = where(agent_ids == location_id)[0]
                if (number_of_agents == -2) or (agent_index.size <= number_of_agents): # unplace all agents
                    unplace_index = agent_index
                else: # sample agents
                    unplace_index = sample_noreplace(agent_index, number_of_agents)
                agent_sets[dataset_name].modify_attribute(name=location_id_name, 
                                                      data=resize(array([-1], dtype=agent_ids.dtype), unplace_index.size),
                                                      index = unplace_index)
                            
from opus_core.tests import opus_unittest
from numpy import ma, arange
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from washtenaw.datasets.deletion_event_dataset import DeletionEventDataset
        
class DeletionEventsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        self.storage.write_table(table_name='gridcells',
            table_data = {
                'grid_id': arange(10) + 1
                }
            )
        # There are 10 jobs in each gridcell 
        self.storage.write_table(table_name='jobs',
            table_data = {
                'job_id': arange(100) + 1,
                'grid_id': array(10*[arange(10)+1]).ravel()
                }
            )
    def _add_households_to_storage(self):
        # There are 10 households in gridcell 1 and 30 households in gridcell 3
        self.storage.write_table(table_name = 'households',
            table_data = {
                'household_id': arange(50) + 1,
                'grid_id': array(10*[1] + 30*[3] + 10*[-1])
                }
            )
      
    def tearDown(self):
        del self.storage
        
    def _create_simple_deletion_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name = 'events', 
               table_data = {
                "scheduled_year": array([2000, 2000, 2001, 2001]),
                "grid_id": array([10, 5, 3, 5]),
                "number_of_jobs": array([20, 5, 0, 3])
                }
            )
        return DeletionEventDataset(in_storage=storage, in_table_name='events')
        
    def _create_full_deletion_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name = 'events', 
               table_data = {
                "scheduled_year": array([2000, 2000, 2001, 2001, 2001]),
                "grid_id": array([1, 5, 3, 5, 2]),
                "number_of_jobs": array([3, 5, 0, 3, -2]),
                "number_of_households": array([7, 5, 25, 0, 0])
                }
            )
        return DeletionEventDataset(in_storage=storage, in_table_name='events')
    
    def test_deletion_of_jobs(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["washtenaw","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_simple_deletion_event_set()

        DeletionEventModel().run(gridcell_set, event_set, 2000, dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should remove 5 jobs from gridcell 5 and all jobs from gridcell 10
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,5,10,10,10,10,0]))) 

        DeletionEventModel().run(gridcell_set, event_set, 2001, dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should remove another 3 jobs from gridcell 5
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,2,10,10,10,10,0])))
        
    def test_deletion_of_jobs_and_households(self):
        self._add_households_to_storage()
        dataset_pool = DatasetPool(storage=self.storage, package_order=["washtenaw","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_full_deletion_event_set()

        DeletionEventModel().run(gridcell_set, event_set, 2000, dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should remove 3 jobs from gridcell 1 and 5 jobs from gridcell 5
        self.assert_(ma.allclose(number_of_jobs, array( [7,10,10,10,5,10,10,10,10,10])))
        # the model should remove 7 households from gridcell 1
        self.assert_(ma.allclose(number_of_households, array( [3,0,30,0,0,0,0,0,0,0]))) 

        DeletionEventModel().run(gridcell_set, event_set, 2001, dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should remove another 3 jobs from gridcell 5 and all jobs from gridcell 2
        self.assert_(ma.allclose(number_of_jobs, array( [7,0,10,10,2,10,10,10,10,10]))) 
        # the model should remove 25 households from gridcell 3
        self.assert_(ma.allclose(number_of_households, array( [3,0,5,0,0,0,0,0,0,0])))
        
if __name__=="__main__":
    opus_unittest.main()