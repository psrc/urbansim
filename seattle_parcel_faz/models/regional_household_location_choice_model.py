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

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique_values
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel

class RegionalHouseholdLocationChoiceModel(HouseholdLocationChoiceModel):
    """Run the urbansim HLCM separately for each large area."""
    
    model_name = "Regional Household Location Choice Model" 
#    regional_id_name = "faz_id"

    def __init__(self, location_set,
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities",
            estimation = "opus_core.bhhh_mnl_estimation",
            capacity_string = "vacant_residential_units",
            estimation_weight_string = "residential_units", 
            number_of_agents_string = "number_of_households",
            number_of_units_string = "residential_units",            
            sample_proportion_locations = None, 
            sample_size_locations = 30, 
            estimation_size_agents = 1.0, 
            compute_capacity_flag = True, 
            filter=None,
            submodel_string = None, location_id_string = None,
            demand_string = None, # if not None, the aggregate demand for locations will be stored in this attribute
            run_config = None, estimate_config=None, debuglevel=0, dataset_pool=None,
            variable_package="urbansim",
            regional_id_name="faz_id"):
        self.regional_id_name = regional_id_name
        run_config = merge_resources_if_not_None(run_config, [ 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("compute_capacity_flag", compute_capacity_flag),
                    ("capacity_string", capacity_string),
                    ("number_of_agents_string", number_of_agents_string),
                    ("number_of_units_string", number_of_units_string),
                    ("demand_string", demand_string)                                                          
                                          ])
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents),
                    ("weights_for_estimation_string", estimation_weight_string)])         
    
        AgentLocationChoiceModel.__init__(self, location_set,
                                        model_name=self.model_name, 
                                        short_name=self.model_short_name, 
                                        sampler=sampler, 
                                        utilities=utilities, 
                                        probabilities=probabilities, 
                                        choices=choices, 
                                        filter=filter, 
                                        submodel_string=submodel_string,  
                                        location_id_string=location_id_string,
                                        run_config=run_config, 
                                        estimate_config=estimate_config, 
                                        debuglevel=debuglevel, dataset_pool=dataset_pool,
                                        variable_package=variable_package)
    
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        regions = agent_set.get_attribute(self.regional_id_name)
        self.choice_set.compute_variables(["urbansim_parcel.%s.%s" % (self.choice_set.get_dataset_name(), self.regional_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_region = where(regions[agents_index] > 0)[0]
        if valid_region.size > 0:
            unique_regions = unique_values(regions[agents_index][valid_region])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_region]] = True
            for area in unique_regions:
                new_index = where(logical_and(cond_array, regions == area))[0]
                self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.regional_id_name, area)
                logger.log_status("HLCM for area %s" % area)
                HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=new_index, **kwargs)
        no_region = where(regions[agents_index] <= 0)[0]
        if no_region.size > 0: # run the HLCM for housseholds that don't have assigned region
            self.filter = None
            logger.log_status("HLCM for households with no area assigned")
            choices = HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=agents_index[no_region], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = self.choice_set.get_id_index(choices[where_valid_choice])
            chosen_regions = self.choice_set.get_attribute_by_index(self.regional_id_name, choices_index)
            agent_set.modify_attribute(name=self.regional_id_name, data=chosen_regions, 
                                       index=no_region[where_valid_choice])

from opus_core.tests import opus_unittest
from numpy import array, ma, arange, where, zeros, concatenate
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory

class Test(StochasticTestCase):
    def skip_test_place_agents_to_correct_areas(self):
        """10 gridcells - 5 in area 1, 5 in area 2, with equal cost, no capacity restrictions
        100 households - 70 live in area 1, 30 live in area 2.
        We set the coefficient value for cost -0.001. 
        """
        storage = StorageFactory().get_storage('dict_storage')

        nhhs = 100
        ngcs = 10
        ngcs_attr = ngcs/2
        hh_grid_ids = array(nhhs*[-1])
        lareas = array(ngcs_attr*[1] + ngcs_attr*[2])
        hh_lareas = array(70*[1] + 30*[2])
        
        household_data = {
            'household_id': arange(nhhs)+1,
            'grid_id': hh_grid_ids,
            'faz_id': hh_lareas
            }

        gridcell_data = {
            'grid_id': arange(ngcs)+1,
            'cost':array(ngcs*[100]),
            'faz_id': lareas            
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
            households = HouseholdDataset(in_storage=storage, in_table_name='households')
            hlcm = RegionalHouseholdLocationChoiceModel(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 4)
            hlcm.run(specification, coefficients, agent_set=households, debuglevel=1)

            # get results
            gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                resources=Resources({"household":households}))
            result_area1 = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr)+1)
            result_area2 = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr+1, ngcs+1))
            gridcells.delete_one_attribute("number_of_households")
            result = concatenate((result_area1, result_area2))
            return result

        expected_results = array(ngcs_attr*[nhhs*0.7/float(ngcs_attr)] + ngcs_attr*[nhhs*0.3/float(ngcs_attr)])

        self.run_stochastic_test(__file__, run_model, expected_results, 10)

        # check the exact sum 
        hlcm = RegionalHouseholdLocationChoiceModel(location_set=gridcells, compute_capacity_flag=False,
                    choices = "opus_core.random_choices_from_index", sample_size_locations = 4)
        hlcm.run(specification, coefficients, agent_set=households, debuglevel=1)
        gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                resources=Resources({"household":households}))
        result_area1 = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr)+1).sum()
        result_area2 = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr+1, ngcs+1)).sum()
        results =  array([result_area1, result_area2])

        expected_results = array([70, 30])
        self.assertEqual(ma.allequal(expected_results, results), True, "Error, should_be: %s, but result: %s" % (
                                                                                             expected_results, results))
        
if __name__=="__main__":
    opus_unittest.main()