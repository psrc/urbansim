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
    large_area_id_name = "large_area_id"
    
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        large_areas = agent_set.compute_variables(["washtenaw.%s.%s" % (agent_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        self.choice_set.compute_variables(["washtenaw.%s.%s" % (self.choice_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_large_area = where(large_areas[agents_index] > 0)[0]
        if valid_large_area.size > 0:
            unique_large_areas = unique_values(large_areas[agents_index][valid_large_area])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_large_area]] = True
            for area in unique_large_areas:
                new_index = where(logical_and(cond_array, large_areas == area))[0]
                self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.large_area_id_name, area)
                logger.log_status("HLCM for area %s" % area)
                HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=new_index, **kwargs)
        no_large_area = where(large_areas[agents_index] <= 0)[0]
        if no_large_area.size > 0: # run the HLCM for housseholds that don't have assigned large_area
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=agents_index[no_large_area], **kwargs)
        if "large_area_id" in agent_set.get_known_attribute_names():
            agent_set.delete_one_attribute("large_area_id") # next time it must be recomputed (HTM sets it as primary attribute) 

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
    def test_place_agents_to_correct_areas(self):
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
            'large_area_id': hh_lareas
            }

        gridcell_data = {
            'grid_id': arange(ngcs)+1,
            'cost':array(ngcs*[100]),
            'large_area_id': lareas            
            }

        storage._write_dataset(out_table_name='households', values=household_data)
        storage._write_dataset(out_table_name='gridcells', values=gridcell_data)

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