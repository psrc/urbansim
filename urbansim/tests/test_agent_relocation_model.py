# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

### These unit tests were moved here from agent_relocation_model to remove
### a circular dependency with household_location_choice_model_creator.
from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from urbansim.models.household_relocation_model_creator import HouseholdRelocationModelCreator
from urbansim.models.employment_relocation_model_creator import EmploymentRelocationModelCreator
from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.resources import Resources
from numpy import array, arange, int8
from numpy import ma
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset

#from urbansim.datasets.rate_dataset import RateDataset
from urbansim.datasets.household_relocation_rate_dataset import HouseholdRelocationRateDataset
from urbansim.datasets.job_relocation_rate_dataset import JobRelocationRateDataset

from opus_core.storage_factory import StorageFactory


class Tests(StochasticTestCase):

    def setUp(self):
#           600 households of age <= 50 and income < 40,000
#           400 households of age > 50 and income < 40,000
#           200 households of age <= 50 and income >= 40,000
#           300 households of age > 50 and income >= 40,000
        self.household_data = {
            "household_id": arange(1500)+1,
            "grid_id": array(1500*[1]),
            "age_of_head": array(600*[40] + 400*[55] + 200*[25] + 300*[70]),
            "income": array(600*[35000] + 400*[20000] + 200*[50000] + 300*[75000])
            }    
        self.annual_relocation_rates_for_households_data = {
            "age_of_head_min": array([0,51,0,51]),
            "age_of_head_max": array([50,100,50,100]),
            "income_min": array([0,0,40000,40000]),
            "income_max": array([39999,39999,100000,100000]),
            "probability_of_relocating": array(4*[1.0])                   
            }
            
    def test_do_nothing_if_no_agents(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name = 'households', 
            table_data = {
                'household_id': array([], dtype='int32')
                }
            )
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='households')
        
        storage.write_table(table_name = 'rates', table_data =self.annual_relocation_rates_for_households_data)            
        hh_rateset = HouseholdRelocationRateDataset(in_storage=storage, in_table_name='rates')

        hrm_resources = Resources({"rate":hh_rateset})

        hrm = HouseholdRelocationModelCreator().get_model(debuglevel=2)
        hrm_relocation_results = hrm.run(hh_set,resources=hrm_resources)

        should_be = 0
        self.assertEqual(hrm_relocation_results.size, should_be, msg = "Error ")
        
    def test_return_unplaced_if_no_probabilities(self):
        """If no probabilities are passed, the model should only return indices of unplaced agents."""
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name = 'households',
            table_data = {
                'household_id': arange(1500)+1,
                'grid_id': array(1000*[1] + 500*[0]), # 500 households unplaced
                }
            )
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='households')
        
        arm = AgentRelocationModel(location_id_name="grid_id")
        result = arm.run(hh_set)
        
        should_be = arange(1000, 1500)
        
        self.assertEqual(ma.allequal(result, should_be), True, msg = "Error " )
        
    def test_hrm_all_households_relocate_with_100_percent_probability(self):
        """Creates four groups of households as defined in the setUp method, 
        and assigns their probability of relocate as 100% (1 because it is a ratio).
        Ensure that all 15,000 households decide to relocate.
        """        
        storage = StorageFactory().get_storage('dict_storage')
 
        storage.write_table(table_name = 'households', table_data =self.household_data)
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='households')
        
        storage.write_table(table_name = 'rates', table_data =self.annual_relocation_rates_for_households_data)
        hh_rateset = HouseholdRelocationRateDataset(in_storage=storage, in_table_name='rates')

        hrm_resources = Resources({"household_relocation_rate":hh_rateset})

        hrm = HouseholdRelocationModelCreator().get_model(debuglevel=1)
        hrm_relocation_results = hrm.run(hh_set,resources=hrm_resources)

        should_be = 1500
        self.assertEqual(hrm_relocation_results.size, should_be, msg = "Error ")

    def test_hrm_no_households_relocate_with_0_percent_probability(self):
        """Creates four groups of households as defined in the setUp method, 
        and assigns their probability of relocate as 0%.
        Ensure that all 15,000 households do not decide to relocate.
        """
        storage = StorageFactory().get_storage('dict_storage')
        
        annual_relocation_rates_for_households_data = self.annual_relocation_rates_for_households_data
        annual_relocation_rates_for_households_data['probability_of_relocating'] = array(4*[0.0])
        
        storage.write_table(table_name = 'households', table_data = self.household_data)
        storage.write_table(table_name = 'rates', table_data = annual_relocation_rates_for_households_data)
      
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='households')
        hh_rateset = HouseholdRelocationRateDataset(in_storage=storage, in_table_name='rates')

        hrm_resources = Resources({'household_relocation_rate':hh_rateset})

        hrm = HouseholdRelocationModelCreator().get_model(debuglevel=1)
        hrm_relocation_results = hrm.run(hh_set,resources=hrm_resources)

        should_be = 0
        self.assertEqual(hrm_relocation_results.size, should_be, msg = 'Error ')

    def test_hrm_proportion_households_relocate_with_varied_percent_probability(self):
        """Creates four groups of households as defined in the setUp method, 
        and assigns their probability of relocating as 0%, 10%, 50%, and 100% respectively.
        Ensure that the number of households that do decide to relocate is proportionate to their probabilites.
        """
        storage = StorageFactory().get_storage('dict_storage')

        annual_relocation_rates_for_households_data = self.annual_relocation_rates_for_households_data
        annual_relocation_rates_for_households_data['probability_of_relocating'] = array([0.0, 0.1,0.5,1.0])
        
        storage.write_table(table_name = 'households', table_data =self.household_data)
        storage.write_table(table_name = 'rates', table_data =annual_relocation_rates_for_households_data)
        
        hh_set = HouseholdDataset(in_storage=storage, in_table_name='households')
        hh_rateset = HouseholdRelocationRateDataset(in_storage=storage, in_table_name='rates')

        hrm_resources = Resources({'household_relocation_rate':hh_rateset})

        hrm = HouseholdRelocationModelCreator().get_model(debuglevel=1)
        
        def run_model():
            hrm_relocation_results = hrm.run(hh_set,resources=hrm_resources)

            """Because this model returns a list of indices of houses that have decided to relocate, which maps 
            nicely to the order in which they were created (by house_id) because of the way populate_table works, 
            we just need to assign ranges of house_id's corresponding to how many houses of that ,
            and then count how many houses returned in hrm_relocation_results are in each range.  
            """
            list_of_tallies = []
            for range_to_count in [range(0,600), range(600,1000), range(1000,1200), range(1200,1500)]:
                list_of_tallies.append(len(filter(lambda x: x in range_to_count, hrm_relocation_results)))
            return array(list_of_tallies)

        should_be = array([0, 40, 100, 300])
        self.run_stochastic_test(__file__, run_model, should_be, 10)

        #the 0% and 100% probability groups should be exactly equal to 0 and 3000 
        #because there is no randomness for those probabilities     
        list_of_tallies = run_model()
        self.assertEqual(ma.allequal([list_of_tallies[0], list_of_tallies[3]],
                                  [should_be[0], should_be[3]]), True, msg = "Error ")

    def test_erm_correct_distribution_of_jobs_relocate(self):
        # In addition to unplaced jobs choose 50% of jobs of sector 2 to relocate and
        # no job of sector 1. 
        # gridcell       has              expected
        # 1         100 sector 1 jobs    100 sector 1 jobs
        #           400 sector 2 jobs    about 200 sector 2 jobs 
        # 2         100 sector 1 jobs    100 sector 1 jobs
        #           200 sector 2 jobs    about 100 sector 2 jobs
        # 3         100 sector 1 jobs    100 sector 1 jobs
        #           100 sector 2 jobs    about 50 sector 2 jobs
        # unplaced   10 sector 1 jobs
        #            10 sector 2 jobs
        
        storage = StorageFactory().get_storage('dict_storage')
        
        # create jobs
        job_grid_ids = array(100*[1]+100*[2]+100*[3]+400*[1]+200*[2]+100*[3]+20*[-1])
        
        storage.write_table(table_name = 'jobs',
            table_data = {
                'job_id': arange(1020)+1,
                'sector_id': array(300*[1]+700*[2]+10*[1]+10*[2]),
                'grid_id': job_grid_ids,
                }
            )
        jobs = JobDataset(in_storage=storage, in_table_name='jobs')
        
        # create gridcells
        storage.write_table(table_name = 'gridcells',
            table_data = {
                'grid_id':arange(3)+1,
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')
        
        # create rate set with rate 0 for jobs of sector 1 and 0.5 for jobs of sector 2
        storage.write_table(table_name = 'rates',
            table_data = {
                'sector_id':array([1,2]), 
                'job_relocation_probability':array([0,0.5]),
                }
            )
        rates = JobRelocationRateDataset(in_storage=storage, in_table_name='rates')
        
        # run model
        model = EmploymentRelocationModelCreator().get_model(debuglevel=0)
        hrm_resources = Resources({"job_relocation_rate":rates})
                    
        # get results from one run
        movers_indices = model.run(jobs, resources = hrm_resources)
        jobs.compute_variables(["urbansim.job.is_in_employment_sector_1"])
        
        # unplace chosen jobs
        compute_resources = Resources({"job":jobs,'urbansim_constant':{"industrial_code":1,
                                                                       "commercial_code":2}})
        jobs.set_values_of_one_attribute(attribute="grid_id", values=-1, index = movers_indices)
        gridcells.compute_variables(["urbansim.gridcell.number_of_jobs_of_sector_1", 
                                     "urbansim.gridcell.number_of_jobs_of_sector_2"],
                                    resources = compute_resources)
            
        # only 100 jobs of sector 1 (unplaced jobs) should be selected
        result1 = jobs.get_attribute_by_index("is_in_employment_sector_1", movers_indices).astype(int8).sum()
        self.assertEqual(result1==10, True)
        
        # number of sector 1 jobs should not change
        result2 = gridcells.get_attribute("number_of_jobs_of_sector_1")
        self.assertEqual(ma.allclose(result2, array([100, 100, 100]), rtol=0), True)
        
        def run_model():
            jobs.modify_attribute(name="grid_id", data = job_grid_ids)
            indices = model.run(jobs, resources = hrm_resources)                
            jobs.modify_attribute(name="grid_id", data = -1, index = indices)
            gridcells.compute_variables(["urbansim.gridcell.number_of_jobs_of_sector_2"],
                                    resources = compute_resources)
            return gridcells.get_attribute("number_of_jobs_of_sector_2")
        
        # distribution of sector 2 jobs should be the same, the mean are halfs of the original values
        should_be = array([200, 100, 50])
        self.run_stochastic_test(__file__, run_model, should_be, 10)
        
    def test_erm_proportion_jobs_relocate_with_varied_percent_probability(self):
        """Create groups of jobs in different gridcells in different sectors, and ensure that
        proportion of jobs that decide to relocate matches % specified for each category
        """
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name = 'jobs',
             table_data = {
                'job_id': arange(1000)+1,
                'grid_id': array(500*[1] + 300*[2] + 200*[3]),
                'sector_id': array(100*[1] + 400*[2] + 100*[1] + 200*[2] + 100*[1] + 100*[2])
                }
            )
            
        storage.write_table(table_name = 'rates',
            table_data = {
                'sector_id':array([1,2]),
                'job_relocation_probability':array([0.5, 0.5])
                }
            )

        jobs_set = JobDataset(in_storage=storage, in_table_name='jobs')
        jobs_rateset = JobRelocationRateDataset(in_storage=storage, in_table_name='rates')

        erm_resources = Resources({"job_relocation_rate":jobs_rateset})

        erm = EmploymentRelocationModelCreator().get_model(debuglevel=1)
        def run_model():
            erm_relocation_results = erm.run(jobs_set,resources=erm_resources)

            list_of_tallies = []
            range_list = [range(0,75),     range(75, 100),  range(100, 400), range(400, 500), #gridcell 1
                          range(500,550), range(550, 600), range(600, 700), range(700, 800), #gridcell 2
                          range(800,825), range(825, 900), range(900, 925), range(925, 1000)] #gridcell 3
            for range_to_count in range_list:
                list_of_tallies.append(len(filter(lambda x: x in range_to_count, erm_relocation_results)))
            return array(list_of_tallies)

        #50% of each group is what we expect. i.e. 750 sector-1 non-home-based jobs were created in gridcell #1, 
        #and so we expect 375 of those jobs to decide to reloacte, since the probability has been set to 50%
        should_be = array([37, 12, 150, 50,
                           25, 25, 50,  50, 
                           12, 37, 12,  37])
        self.run_stochastic_test(__file__, run_model, should_be, 10)
        
        #sum up the number of relocated jobs in sector 1
        def run_model_sector_1():
            list_of_tallies = run_model()
            list_of_tallies_summed = filter(lambda i: not(i/2%2), range(len(list_of_tallies)))
            list_of_tallies_summed = sum(map(lambda x: list_of_tallies[x], list_of_tallies_summed))
            return list_of_tallies_summed
        
        should_be = array([37 + 12 + 25 + 25 + 12 + 37])
        self.run_stochastic_test(__file__, run_model_sector_1, should_be, 10)
        
        #sum up the number of relocated jobs in sector 2
        def run_model_sector_2():
            list_of_tallies = run_model()
            list_of_tallies_summed = filter(lambda i: i/2%2, range(len(list_of_tallies)))
            list_of_tallies_summed = sum(map(lambda x: list_of_tallies[x], list_of_tallies_summed))
            return list_of_tallies_summed
        should_be = array([150 + 50 + 50 + 50 + 12 + 37])
        self.run_stochastic_test(__file__, run_model_sector_2, should_be, 10)


if __name__=='__main__':
    opus_unittest.main()