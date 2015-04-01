# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, where, resize, logical_and, zeros, arange, ones
from opus_core.model import Model
from opus_core.sampling_toolbox import sample_noreplace, sample_replace
from opus_core.logger import logger

class AgentEventModel(Model):
    """ Removes, adds agents (jobs, households) from/to their locations according to the {agent}_events table
        (e.g. jobs_events).
    """
    model_name = "Agent Event Model"
          
    def run(self, location_set, agent_event_set, agent_set, current_year, disaggregate_to=None, 
            location_characteristics=[], dataset_pool=None):
        """ The agent_event_set is expected to have attributes:
                grid_id, scheduled_year, total_number, is_percentage, change_type, (optionally other agent characteristics)
            'grid_id' is not a mandatory name, but it must match to the id name of the location_set.
            Thus, the model works on any geography level. If it's a aggregated geography and there is a need to 
            disaggregate the agents into lower geography, set the dataset to be disaggregated to in the 
            'disaggregate_to' argument (e.g. location_set=zone, disaggregate_to=building).
            'is_percentage' (bool) determines if the 'total_number' is a percentage of existing agents (True) or 
            an absolute number (False).
            'change_type' can have values 'D' (delete), 'A' (add) and determines the type
            of change for the agents. If this column is missing, the model considers 'D' as default
            for all entries in the agent_event_set.
            If the change of type is 'D', 
            the method finds agents from the agent_set (jobs, households) located in the given locations 
            (e.g. grid_id), then samples the given amount for the current_year and unplaces them.
            If other characteristics columns are contained in the agent_event_set, their names
            must match column names in the agent_set (e.g. 'sector_id' for jobs).
            In such a case the deletion is done among agents that match the given characteristics.
            If the change of type is 'A', the agent_event_set can contain attributes of the location set.
            It determines agents used for sampling missing characteristics of the added agents, for example
            values of income or persons. Values of these characteristics can be -1 if no restriction 
            for the sampling is desired. Such location attributes must be passed in the argument 
            'location_characteristics'. 
        """        
        if not agent_event_set or (agent_event_set.size() == 0): 
            logger.log_status("No %s agents for event processing." % agent_set.get_dataset_name())
            return

        idx_of_events_this_year = agent_event_set.get_attribute("scheduled_year") == current_year
        if idx_of_events_this_year.sum() == 0:
            logger.log_status("No %s agents for this year event processing." % agent_set.get_dataset_name())
            return
        
        self.dataset_pool = self.create_dataset_pool(dataset_pool)
        
        location_id_name = location_set.get_id_name()[0]
        location_ids_in_event_set = agent_event_set.get_attribute_by_index(location_id_name, 
                                                                           idx_of_events_this_year)
        
        other_characteristics = agent_event_set.get_known_attribute_names()
        for name in agent_event_set.get_id_name() + [location_id_name, 
                    "scheduled_year", "total_number", "is_percentage", "change_type"] + location_characteristics:
            if name in other_characteristics:
                other_characteristics.remove(name)
        
        totals = agent_event_set.get_attribute_by_index("total_number", idx_of_events_this_year)
        if "change_type" not in agent_event_set.get_known_attribute_names():
            types_of_change = array(idx_of_events_this_year.sum()*['D'])
        else:
            types_of_change = agent_event_set.get_attribute_by_index("change_type", 
                                                                           idx_of_events_this_year)
        if "is_percentage" not in agent_event_set.get_known_attribute_names():
            is_percentage = zeros(idx_of_events_this_year.sum(), dtype='bool8')
        else:
            is_percentage = agent_event_set.get_attribute_by_index("is_percentage", 
                                                                           idx_of_events_this_year)
        
        # pre-load other characteristics
        for name in other_characteristics:
            agent_event_set.get_attribute(name)
            
        if location_id_name not in agent_set.get_known_attribute_names():
            # compute agents locations
            agent_set.compute_one_variable_with_unknown_package(location_id_name, self.dataset_pool)
                    
        # iterate over rows in the event set
        for ilocation_id in range(location_ids_in_event_set.size):
            agent_ids = agent_set.get_attribute(location_id_name)
            location_id = location_ids_in_event_set[ilocation_id]
            change_type = types_of_change[ilocation_id]

            agents_to_consider = agent_ids == location_id
            for characteristics in other_characteristics:
                characteristics_value = agent_event_set[characteristics][idx_of_events_this_year][ilocation_id]
                agents_to_consider = logical_and(agents_to_consider, 
                                                 agent_set.get_attribute(characteristics) == characteristics_value)
            number_of_agents = totals[ilocation_id]
            agent_index = where(agents_to_consider)[0]  
            if  is_percentage[ilocation_id]: # number_of_agents means percentage; convert to absolute number
                number_of_agents = agent_index.size*number_of_agents/100.0
            number_of_agents = int(number_of_agents)
            if change_type == 'D':
                if number_of_agents > 0:
                    if agent_index.size <= number_of_agents: # unplace all agents
                        unplace_index = agent_index
                    else: # sample agents
                        unplace_index = sample_noreplace(agent_index, number_of_agents)
                    agent_set.modify_attribute(name=location_id_name, 
                                           data=resize(array([-1], dtype=agent_ids.dtype), unplace_index.size),
                                           index = unplace_index)
                    logger.log_status('%s agents deleted from location %s' % (number_of_agents, location_id))
            elif change_type == 'A':
                if number_of_agents <= 0:
                    continue
                data = {agent_set.get_id_name()[0]: arange(1, number_of_agents+1, 1) + agent_set.get_id_attribute().max()}
                if disaggregate_to is not None:
                    if location_id_name not in disaggregate_to.get_known_attribute_names():
                        disaggregate_to.compute_one_variable_with_unknown_package(location_id_name, self.dataset_pool)
                    disaggr_idx = where(disaggregate_to[location_id_name] == location_id)[0]
                    if disaggr_idx.size <= 0:
                        logger.log_warning('No %s locations found for %s=%s. %s agents not created.' % (
                                disaggregate_to.get_dataset_name(), location_id_name, location_id, number_of_agents))
                        continue
                    # sample disaggregated locations
                    disaggr_sidx = sample_replace(disaggr_idx, number_of_agents)
                    data[disaggregate_to.get_id_name()[0]] = disaggregate_to.get_id_attribute()[disaggr_sidx]
                else:
                    data[location_id_name] = array([location_id] * number_of_agents)
                
                for characteristics in other_characteristics:
                    characteristics_value = agent_event_set[characteristics][idx_of_events_this_year][ilocation_id]
                    data[characteristics] = array([characteristics_value] * number_of_agents)
                
                # determine agents with the desire characteristics to impute missing characteristics to the new agents
                loc_indicator = ones(agent_set.size(), dtype='bool8')
                for locchar in location_characteristics:
                    if agent_event_set[locchar][idx_of_events_this_year][ilocation_id] == -1:
                        continue
                    var = agent_set.compute_one_variable_with_unknown_package(locchar, self.dataset_pool)
                    loc_indicator = logical_and(loc_indicator, var == agent_event_set[locchar][idx_of_events_this_year][ilocation_id])
                if loc_indicator.sum() == 0:
                    loc_indicator[:] = True
                clone_attr_index = sample_replace(where(loc_indicator)[0], number_of_agents)
                # impute remaining attributes
                for attr in agent_set.get_primary_attribute_names():
                    if attr not in data.keys():
                        data[attr] = agent_set[attr][clone_attr_index]
                
                agent_set.add_elements(data, require_all_attributes=False)
                if location_id_name not in agent_set.get_known_attribute_names():
                    # re-compute agents locations, because the add_elements method deleted all computed attributes
                    agent_set.compute_one_variable_with_unknown_package(location_id_name, self.dataset_pool)
                logger.log_status('%s agents added to location %s' % (number_of_agents, location_id))
                    
                            
from opus_core.tests import opus_unittest
from numpy import ma, arange, in1d
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from psrc_parcel.datasets.jobs_event_dataset import JobsEventDataset
from psrc_parcel.datasets.households_event_dataset import HouseholdsEventDataset
        
class AgentEventsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = StorageFactory().get_storage('dict_storage')
        self.storage.write_table(table_name='gridcells',
            table_data = {
                'grid_id': arange(10) + 1,
                'zone_id': array([1,1]+8*[2])
                }
            )
        # There are 10 jobs in each gridcell
        # All gridcells have 4 jobs of sector 1, 3 jobs of sector 4, 3 jobs of sector 2
        self.storage.write_table(table_name='jobs',
            table_data = {
                'job_id': arange(100) + 1,
                'grid_id': array(10*[arange(10)+1]).ravel(),
                'sector_id': array(40*[1] + 30*[4] + 30*[2])
                }
            )
        # There are 10 households in gridcell 1 and 30 households in gridcell 3
        self.storage.write_table(table_name='households',
            table_data = {
                'household_id': arange(50) + 1,
                'grid_id': array(10*[1] + 30*[3] + 10*[-1]),
                'persons': array(5*[1] + 5*[2] + 40*[3])
                }
            )
      
    def tearDown(self):
        del self.storage
        
    def _create_simple_job_deletion_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                "jobs_event_id": arange(1,5),
                "scheduled_year": array([2000, 2000, 2001, 2001]),
                "grid_id": array([10, 5, 3, 5]),
                "total_number": array([20, 5, 0, 3])
                }
            )
        return JobsEventDataset(in_storage=storage, in_table_name='events')

    def _create_simple_job_addition_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                "jobs_event_id": arange(1,5),
                "scheduled_year": array([2000, 2000, 2001, 2001]),
                "grid_id": array([10, 5, 3, 5]),
                "total_number": array([20, 5, 0, 3]),
                "change_type": array(['A', 'A', 'A', 'A']),
                
                }
            )
        return JobsEventDataset(in_storage=storage, in_table_name='events')
        
    def _create_household_deletion_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                "households_event_id": arange(1,7),
                "scheduled_year": array([2000, 2000, 2001, 2001, 2001, 2001]),
                "grid_id": array([1, 5, 3, 5, 2, 1]),
                "total_number": array([6, 5, 25, 0, 0, 50]),
                "is_percentage": array([0,0, 0,  0, 0,  1], dtype="bool8"),
                }
            )
        return HouseholdsEventDataset(in_storage=storage, in_table_name='events')

    def _create_household_addition_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                "households_event_id": arange(1,7),
                "scheduled_year": array([2000, 2000, 2001, 2001, 2001, 2001]),
                "grid_id":      array([1, 5, 3, 5, 2, 1]),
                "total_number": array([6, 5, 25, 0, 0, 50]),
                "is_percentage": array([0,0, 0,  0, 0,  1], dtype="bool8"),
                "change_type":array(['A','A','A','A','A','A'])
                }
            )
        return HouseholdsEventDataset(in_storage=storage, in_table_name='events')
    
    def _create_household_addition_event_set_with_location(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='events', 
                            table_data = {
                                "households_event_id": arange(1,7),
                                "scheduled_year": array([2000, 2000, 2001, 2001, 2001, 2001]),
                                "grid_id":      array([1, 5, 3, 5, 2, 1]),
                                "total_number": array([6, 5, 25, 0, 0, 50]),
                                "is_percentage": array([0,0, 0,  0, 0,  1], dtype="bool8"),
                                "change_type":array(['A','A','A','A','A','A']),
                                "zone_id": array([1, 1, -1, -1, -1, -1])
                            }
                            )
        return HouseholdsEventDataset(in_storage=storage, in_table_name='events')    
        
    def _create_job_deletion_event_set_with_characteristics(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                 "jobs_event_id": arange(1,7),
                "scheduled_year": array([2000, 2000, 2001, 2001, 2001, 2001]),
                "grid_id":          array([1,    5,    3,   5,     2,    1]),
                "total_number": array([2,    5,  70,  2,    100,    1]),
                "is_percentage": array([0,   0,   1,  0,     1,     0], dtype="bool8"),
                "sector_id":        array([1,    1,    2,   2,     2,    1])
                }
            )
        return JobsEventDataset(in_storage=storage, in_table_name='events')

    def _create_job_addition_event_set_with_characteristics(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='events', 
               table_data = {
                "jobs_event_id": arange(1,7),
                "scheduled_year": array([2000, 2000, 2001, 2001, 2001, 2001]),
                "grid_id":          array([1,    5,    3,   5,     2,    1]),
                "total_number": array([2,    5,  70,  2,    100,    1]),
                "is_percentage": array([0,   0,   1,  0,     1,     0], dtype="bool8"),
                "sector_id":        array([1,    1,    2,   2,     2,    1]),
                "change_type":array(['A','A','A','A','A','A'])                
                }
            )
        return JobsEventDataset(in_storage=storage, in_table_name='events')
    
    def test_deletion_of_jobs(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_simple_job_deletion_event_set()
        jobs = dataset_pool.get_dataset("job")
        AgentEventModel().run(gridcell_set, event_set, jobs, 2000, dataset_pool=dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should remove 5 jobs from gridcell 5 and all jobs from gridcell 10
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,5,10,10,10,10,0]))) 

        AgentEventModel().run(gridcell_set, event_set, jobs, 2001, dataset_pool=dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should remove another 3 jobs from gridcell 5
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,2,10,10,10,10,0])))

    def test_addition_of_jobs(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_simple_job_addition_event_set()
        jobs = dataset_pool.get_dataset("job")
        AgentEventModel().run(gridcell_set, event_set, jobs, 2000, dataset_pool=dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should add 5 jobs to gridcell 5 and 20 jobs to gridcell 10
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,15,10,10,10,10,30]))) 

        AgentEventModel().run(gridcell_set, event_set, jobs, 2001, dataset_pool=dataset_pool)
        number_of_jobs = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs", dataset_pool=dataset_pool)
        # the model should add another 3 jobs to gridcell 5
        self.assert_(ma.allclose(number_of_jobs, array( [10,10,10,10,18,10,10,10,10,30])))
        
    def test_deletion_of_households(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_household_deletion_event_set()
        households = dataset_pool.get_dataset("household")
        AgentEventModel().run(gridcell_set, event_set, households, 2000, dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should remove 6 households from gridcell 1
        self.assert_(ma.allclose(number_of_households, array( [4,0,30,0,0,0,0,0,0,0]))) 

        AgentEventModel().run(gridcell_set, event_set, households, 2001, dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should remove 50% from gridcell 1 (2) and 25 households from gridcell 3
        self.assert_(ma.allclose(number_of_households, array( [2,0,5,0,0,0,0,0,0,0])))

    def test_addition_of_households(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_household_addition_event_set()
        households = dataset_pool.get_dataset("household")
        AgentEventModel().run(gridcell_set, event_set, households, 2000, dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should add 6 households to gridcell 1, 
        self.assert_(ma.allclose(number_of_households, array( [16,0,30,0,5,0,0,0,0,0]))) 

        AgentEventModel().run(gridcell_set, event_set, households, 2001, dataset_pool=dataset_pool)
        number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                              dataset_pool=dataset_pool)
        # the model should add 50% from gridcell 1 (8) and 25 households to gridcell 3
        self.assert_(ma.allclose(number_of_households, array( [24,0,55,0,5,0,0,0,0,0])))
        
    def test_addition_of_households_with_location(self):
            dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
            gridcell_set = dataset_pool.get_dataset('gridcell')
            event_set = self._create_household_addition_event_set_with_location()
            households = dataset_pool.get_dataset("household")
            AgentEventModel().run(gridcell_set, event_set, households, 2000, 
                                  location_characteristics=['zone_id'], dataset_pool=dataset_pool)
            
            # the model should add 6 households to gridcell 1 and 5 to gridcell 5, i.e. 11 new households
            # all new households should have persons either 1 or 2, but not 3
            self.assert_(in1d(households['persons'][50:61], array([1,2])).all())
     
            AgentEventModel().run(gridcell_set, event_set, households, 2001, 
                                  location_characteristics=['zone_id'], dataset_pool=dataset_pool)
            number_of_households = gridcell_set.compute_variables("urbansim.gridcell.number_of_households", 
                                                                  dataset_pool=dataset_pool)
            # the model should add 50% from gridcell 1 (8) and 25 households to gridcell 3, i.e. 33 new HHs
            # new households should have persons 1,2,3
            self.assert_(in1d(households['persons'][61:94], array([1,2,3])).all())    
        
    def test_deletion_of_jobs_with_one_characteristics(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_job_deletion_event_set_with_characteristics()
        jobs = dataset_pool.get_dataset("job")
        AgentEventModel().run(gridcell_set, event_set, jobs, 2000, dataset_pool=dataset_pool)
        number_of_jobs_of_sector_1 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_1", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_2 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_2", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_4 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_4", 
                                                                    dataset_pool=dataset_pool)
        # the model should remove 2 jobs of sector 1 from gridcell 1, 
        #                         5 jobs of sector 1 from gridcell 5
        self.assert_(ma.allclose(number_of_jobs_of_sector_1, array( [2,4,4,4,0,4,4,4,4,4]))) 
        # other sectors don't change
        self.assert_(ma.allclose(number_of_jobs_of_sector_2, array( 10 * [3]))) 
        self.assert_(ma.allclose(number_of_jobs_of_sector_4, array( 10 * [3]))) 

        AgentEventModel().run(gridcell_set, event_set, jobs, 2001, dataset_pool=dataset_pool)
        number_of_jobs_of_sector_1 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_1", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_2 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_2", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_4 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_4", 
                                                                    dataset_pool=dataset_pool)
        # the model should remove 2 jobs of sector 2 from gridcell 5, 
        #                         1 job of sector 1 from gridcell 1,
        #                       all jobs of sector 2 from gridcell 2
        #                        70% jobs of sector 2 from gridcell 3
        self.assert_(ma.allclose(number_of_jobs_of_sector_1, array( [1,4,4,4,0,4,4,4,4,4]))) 
        self.assert_(ma.allclose(number_of_jobs_of_sector_2, array( [3, 0, 1, 3, 1, 3, 3, 3, 3, 3]))) 
        # sector 4 does not change

    def test_addition_of_jobs_with_one_characteristics(self):
        dataset_pool = DatasetPool(storage=self.storage, package_order=["psrc_parcel","urbansim", "opus_core"])
        gridcell_set = dataset_pool.get_dataset('gridcell')
        event_set = self._create_job_addition_event_set_with_characteristics()
        jobs = dataset_pool.get_dataset("job")
        AgentEventModel().run(gridcell_set, event_set, jobs, 2000, dataset_pool=dataset_pool)
        number_of_jobs_of_sector_1 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_1", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_2 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_2", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_4 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_4", 
                                                                    dataset_pool=dataset_pool)

        # the model should add 2 jobs of sector 1 to gridcell 1, 
        #                      5 jobs of sector 1 to gridcell 5
        self.assert_(ma.allclose(number_of_jobs_of_sector_1, array( [6,4,4,4,9,4,4,4,4,4]))) 
        # other sectors don't change
        self.assert_(ma.allclose(number_of_jobs_of_sector_2, array( 10 * [3]))) 
        self.assert_(ma.allclose(number_of_jobs_of_sector_4, array( 10 * [3]))) 

        AgentEventModel().run(gridcell_set, event_set, jobs, 2001, dataset_pool=dataset_pool)
        number_of_jobs_of_sector_1 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_1", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_2 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_2", 
                                                                    dataset_pool=dataset_pool)
        number_of_jobs_of_sector_4 = gridcell_set.compute_variables("urbansim.gridcell.number_of_jobs_of_sector_4", 
                                                                    dataset_pool=dataset_pool)
        # the model should add 2 jobs of sector 2 to gridcell 5, 
        #                      1 job of sector 1 to gridcell 1,
        #                      4 jobs of sector 2 to gridcell 2
        #                      70% jobs of sector 2 to gridcell 3
        self.assert_(ma.allclose(number_of_jobs_of_sector_1, array( [7, 4, 4, 4, 9, 4, 4, 4, 4, 4]))) 
        self.assert_(ma.allclose(number_of_jobs_of_sector_2, array( [3, 6, 5, 3, 5, 3, 3, 3, 3, 3]))) 
        # sector 4 does not change
        self.assert_(ma.allclose(number_of_jobs_of_sector_4, array( 10 * [3])))
                
if __name__=="__main__":
    opus_unittest.main()