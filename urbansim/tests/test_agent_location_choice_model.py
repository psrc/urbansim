# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

### These unit tests were moved here from agent_location_choice_model to remove
### a circular dependency with household_location_choice_model_creator.
from opus_core.tests import opus_unittest
from numpy import array, ma, arange, where, zeros, concatenate
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.datasets.dataset import DatasetSubset
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.model_group import ModelGroup, ModelGroupMember
from opus_core.storage_factory import StorageFactory


class Test(StochasticTestCase):
    def test_do_nothing_if_no_agents(self):
        storage = StorageFactory().get_storage('dict_storage')

        households_table_name = 'households'
        storage.write_table(
            table_name = households_table_name,
            table_data = {
                "household_id": arange(10000)+1,
                "grid_id": array(10000*[-1])
                }
            )
        households = HouseholdDataset(in_storage=storage, in_table_name=households_table_name)

        gridcells_table_name = 'gridcells'
        storage.write_table(
            table_name = gridcells_table_name,
            table_data = {
                "grid_id": arange(100)+1,
                "cost":array(50*[100]+50*[1000])
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

        # create coefficients and specification
        coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
        specification = EquationSpecification(variables=("gridcell.cost", ), coefficients=("costcoef", ))

        # run the model
        hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
        hlcm.run(specification, coefficients, agent_set = households, agents_index=array([], dtype='int32'), debuglevel=1)

        # get results
        gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
            resources=Resources({"household":households}))
        result = gridcells.get_attribute("number_of_households")

        # check the individual gridcells
        self.assertEqual(ma.allclose(result, zeros((100,)) , rtol=0), True)

    def test_agents_go_to_attractive_locations(self):
        """10 gridcells - 5 with cost 100, 5 with cost 1000, no capacity restrictions
        100 households
        We set the coefficient value for cost -0.001. This leads to probability
        proportion 0.71 (less costly gridcells) to 0.29 (expensive gridcells)
        (derived from the logit formula)
        """
        storage = StorageFactory().get_storage('dict_storage')

        nhhs = 100
        ngcs = 10
        ngcs_attr = ngcs/2
        ngcs_noattr = ngcs - ngcs_attr
        hh_grid_ids = array(nhhs*[-1])

        household_data = {
            'household_id': arange(nhhs)+1,
            'grid_id': hh_grid_ids
            }

        gridcell_data = {
            'grid_id': arange(ngcs)+1,
            'cost':array(ngcs_attr*[100]+ngcs_noattr*[1000])
            }

        storage.write_table(table_name = 'households', table_data = household_data)
        storage.write_table(table_name = 'gridcells', table_data = gridcell_data)

        households = HouseholdDataset(in_storage=storage, in_table_name='households')
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        # create coefficients and specification
        coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
        specification = EquationSpecification(variables=("gridcell.cost", ), coefficients=("costcoef", ))

        # check the individual gridcells
        def run_model():
            hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 8)
            hlcm.run(specification, coefficients, agent_set=households, debuglevel=1)

            # get results
            gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                resources=Resources({"household":households}))
            result_more_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr)+1)
            result_less_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr+1, ngcs+1))
            households.set_values_of_one_attribute(attribute="grid_id", values=hh_grid_ids)
            gridcells.delete_one_attribute("number_of_households")
            result = concatenate((result_more_attractive, result_less_attractive))
            return result

        expected_results = array(ngcs_attr*[nhhs*0.71/float(ngcs_attr)] + ngcs_noattr*[nhhs*0.29/float(ngcs_noattr)])

        self.run_stochastic_test(__file__, run_model, expected_results, 10)

        def run_model_2():
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdDataset(in_storage=storage, in_table_name='households')

            storage.write_table(table_name = 'gridcells', table_data = gridcell_data)
            gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

            hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 8)
            hlcm.run(specification, coefficients, agent_set=households, debuglevel=1)

            # get results
            gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                resources=Resources({"household":households}))
            result_more_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr)+1)
            result_less_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr+1, ngcs+1))
            return array([result_more_attractive.sum(), result_less_attractive.sum()])

        expected_results = array([nhhs*0.71, nhhs*0.29])
        self.run_stochastic_test(__file__, run_model_2, expected_results, 10)

    def test_agents_do_not_go_to_inferior_locations(self):
        """100 gridcells - 99 with attractiveness 2000, 1 with attractiveness 1, no capacity restrictions
        10,000 households
        We set the coefficient value for attracitiveness to 1.
        """
        storage = StorageFactory().get_storage('dict_storage')

        #create households
        storage.write_table(table_name='households',
            table_data = {
                'household_id': arange(10000)+1,
                'grid_id': array(10000*[-1])
                }
            )
        households = HouseholdDataset(in_storage=storage, in_table_name='households')

        # create gridcells
        storage.write_table(table_name='gridcells',
            table_data = {
                'grid_id': arange(100)+1,
                'attractiveness':array(99*[2000]+[1])
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        # create coefficients and specification
        coefficients = Coefficients(names=("attractcoef", ), values=(1,))
        specification = EquationSpecification(variables=("gridcell.attractiveness", ), coefficients=("attractcoef", ))

        # run the model
        hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
        hlcm.run(specification, coefficients, agent_set = households, debuglevel=1)

        # get results
        gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
            resources=Resources({"household":households}))
        result = gridcells.get_attribute_by_id("number_of_households", 100)

        # nobody should choose gridcell 100
        self.assertEqual(result, 0, "Error: %s is not equal to 0" % (result,))

    def xtest_gracefully_handle_empty_choice_sets(self):
        storage = StorageFactory().get_storage('dict_storage')

        #create households
        storage.write_table(table_name='households',
            table_data = {
                'household_id': arange(10000)+1,
                'grid_id': array(100*list(range(100)))+1
                }
            )
        households = HouseholdDataset(in_storage=storage, in_table_name='households')

        # create gridcells
        storage.write_table(table_name='gridcells',
            table_data = {
                'grid_id': arange(100)+1,
                'residential_units':array(100*[100])
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        # create coefficients and specification
        coefficients = Coefficients(names=("dummy",), values=(0,))
        specification = EquationSpecification(variables=("gridcell.residential_units",), coefficients=("dummy",))

        # run the model
        hlcm = HouseholdLocationChoiceModelCreator().get_model( location_set=gridcells,
                choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
        hlcm.run(specification, coefficients, agent_set=households, debuglevel=1)

        # get results
        gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
            resources=Resources({"household":households}))
        result = gridcells.get_attribute_by_id("number_of_households", 100)

        # nobody should choose gridcell 100
        self.assertEqual(ma.allclose(result.sum(), 0 , rtol=0),
                         True, "Error: %s is not equal to 0" % (result.sum(),))

    def test_unplaced_agents_decrease_available_space(self):
        """Using the household location choice model, create a set of available spaces and
        2000 unplaced agents (along with 5000 placed agents). Run the model, and check that
        the unplaced agents were placed, and the number of available spaces has decreased"""
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='households',
            table_data = {
                'grid_id': array(2000*[0] + 5000*[1]),
                'household_id': arange(7000)+1
                }
            )

        storage.write_table(table_name='gridcells',
            table_data= {
                'residential_units':array(50*[10000]),
                'grid_id':  arange(50)+1
                }
            )

        households = HouseholdDataset(in_storage=storage, in_table_name='households')
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        coefficients = Coefficients(names=("dummy",), values=(0.1,))
        specification = EquationSpecification(variables=("gridcell.residential_units",), coefficients=("dummy",))

        """need to specify to the household location choice model exactly which households are moving,
        because by default it assumes all current households want to move, but in this test,
        the 5000 households already in gridcell #1 shouldn't move.
        here, we specify that only the unplaced households should be moved."""
        agents_index = where(households.get_attribute("grid_id") == 0)[0]

        hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells,
               choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
        hlcm.run(specification, coefficients, agent_set=households, agents_index=agents_index, debuglevel=1)

        gridcells.compute_variables(["urbansim.gridcell.vacant_residential_units"],
                                    resources=Resources({"household":households}))
        vacancies = gridcells.get_attribute("vacant_residential_units")

        """since there were 5000 households already in gridcell #1, and gridcell #1 has
        10000 residential units, there should be no more than 5000 vacant residential units
        in gridcell #1 after running this model"""
        self.assertEqual(vacancies[0] <= 5000,
                         True, "Error: %d" % (vacancies[0],))
        """there should be exactly 430000 vacant residential units after the model run,
        because there were originally 50 gridcells with 10000 residential units each,
        and a total of 7000 units are occupied after the run"""
        self.assertEqual(sum(vacancies) == 50 * 10000 - 7000,
                         True, "Error: %d" % (sum(vacancies)))


    def test_agents_placed_in_appropriate_types(self):
        """Create 1000 unplaced industrial jobs and 1 commercial job. Allocate 50 commercial
        gridcells with enough space for 10 commercial jobs per gridcell. After running the
        EmploymentLocationChoiceModel, the 1 commercial job should be placed,
        but the 100 industrial jobs should remain unplaced
        """
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='job_building_types',
            table_data = {
                'id':array([2,1]),
                'name': array(['commercial', 'industrial'])
                }
            )
        job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name='job_building_types')

        storage.write_table(table_name='jobs',
            table_data = {
                'job_id': arange(1001)+1,
                'grid_id': array([0]*1001),
                'building_type': array([1]*1000 + [2])
                }
            )
        jobs = JobDataset(in_storage=storage, in_table_name='jobs')

        storage.write_table(table_name='gridcells',
            table_data = {
                'grid_id': arange(50)+1,
                'commercial_sqft': array([1000]*50),
                'commercial_sqft_per_job': array([100]*50)
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

        coefficients = Coefficients(names=("dummy",), values=(0.1,))
        specification = EquationSpecification(variables=("gridcell.commercial_sqft",), coefficients=("dummy",))

        compute_resources = Resources({"job":jobs, "job_building_type": job_building_types})
        agents_index = where(jobs.get_attribute("grid_id") == 0)
        unplace_jobs = DatasetSubset(jobs, agents_index)
        agents_index = where(unplace_jobs.get_attribute("building_type") == 2)[0]
        gridcells.compute_variables(["urbansim.gridcell.number_of_commercial_jobs"],
                                    resources=compute_resources)
        commercial_jobs = gridcells.get_attribute("number_of_commercial_jobs")

        gridcells.compute_variables(["urbansim.gridcell.number_of_industrial_jobs"],
                                    resources=compute_resources)
        industrial_jobs = gridcells.get_attribute("number_of_industrial_jobs")
        model_group = ModelGroup(job_building_types, "name")
        elcm = EmploymentLocationChoiceModel(ModelGroupMember(model_group,"commercial"), location_set=gridcells,
               agents_grouping_attribute = "job.building_type",
               choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
        elcm.run(specification, coefficients, agent_set = jobs, agents_index=agents_index, debuglevel=1)

        gridcells.compute_variables(["urbansim.gridcell.number_of_commercial_jobs"],
                                    resources=compute_resources)
        commercial_jobs = gridcells.get_attribute("number_of_commercial_jobs")

        gridcells.compute_variables(["urbansim.gridcell.number_of_industrial_jobs"],
                                    resources=compute_resources)
        industrial_jobs = gridcells.get_attribute("number_of_industrial_jobs")

        self.assertEqual(commercial_jobs.sum() == 1,
                         True, "Error, there should only be a total of 1 commercial job")
        self.assertEqual(industrial_jobs.sum() == 0,
                         True, "Error, there should be no industrial jobs because there's no space for them")

    def test_agents_equally_distributed_across_attractive_locations(self):
        """Create 5000 unplaced households and 50 gridcells with equal attractiveness.
        Theoretically, after running the location_choice_model, there should be
        100 houesholds in each gridcell since they're equally attractive, but due to random
        sampling there will be a little deviance. The test also checks, if the aggregated probabilities,
        i.e. housing demand, are equally distributed.
        """
        nhhs = 5000

        household_data = {
            "household_id": arange(nhhs)+1,
            "grid_id": array(nhhs*[-1])
            }

        gridcell_data = {
            "grid_id": arange(50)+1,
            "cost":array(50*[1000])
            }

        coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
        specification = EquationSpecification(variables=("gridcell.cost", ), coefficients=("costcoef", ))

        def run_model1():
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdDataset(in_storage=storage, in_table_name='households')

            storage.write_table(table_name = 'gridcells', table_data = gridcell_data)
            gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

            hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
            hlcm.run(specification, coefficients, agent_set = households)

            gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                                        resources=Resources({"household":households}))
            return gridcells.get_attribute("number_of_households")

        expected_results = array(50*[nhhs/50])

        self.run_stochastic_test(__file__, run_model1, expected_results, 10)

        def run_model2():
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdDataset(in_storage=storage, in_table_name='households')

            storage.write_table(table_name = 'gridcells', table_data = gridcell_data)
            gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')

            hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 30)
            hlcm.run(specification, coefficients, agent_set = households,
                     run_config=Resources({"demand_string":"gridcell.housing_demand"}))
            return gridcells.get_attribute("housing_demand")

        #check aggregated demand
        expected_results = array(50*[nhhs/50])
        self.run_stochastic_test(__file__, run_model2, expected_results, 5)


if __name__=="__main__":
    opus_unittest.main()