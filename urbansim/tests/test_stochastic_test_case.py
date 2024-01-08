# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import arange
from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from opus_core.coefficients import Coefficients
from opus_core.storage_factory import StorageFactory
from opus_core.equation_specification import EquationSpecification
from opus_core.tests.stochastic_test_case import StochasticTestCase

from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator


class Test(StochasticTestCase):   
    """
    We are using this class to explore how to test stochastic systems.
    """
    def test_stochastic_test_case(self):
        """100 gridcells - 50 with cost 100, 50 with cost 1000, no capacity restrictions
        10,000 households
        We set the coefficient value for cost -0.001. This leads to probability
        proportion 0.71 (less costly gridcells) to 0.29 (expensive gridcells)
        (derived from the logit formula)
        """
        storage = StorageFactory().get_storage('dict_storage')
        
        nhouseholds = 10000
        ngrids = 10
        
        #create households
        storage.write_table(table_name='households',
            table_data = {
                'household_id': arange(nhouseholds)+1, 
                'grid_id': array(nhouseholds*[-1])
                }
            ) 
        households = HouseholdDataset(in_storage=storage, in_table_name='households')
            
        # create gridcells
        storage.write_table(table_name = 'gridcells',
            table_data = {
                'grid_id': arange(ngrids)+1,
                'cost':array(int(ngrids/2)*[100] + int(ngrids/2)*[1000])
                }
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name='gridcells')
        
        # create coefficients and specification
        coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
        specification = EquationSpecification(variables=("gridcell.cost", ), coefficients=("costcoef", ))
        
        # run the model
        hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False, \
                choices = "opus_core.random_choices_from_index", sampler=None)
                #sample_size_locations = 30)
        
        # check the individual gridcells
        # This is a stochastic model, so it may legitimately fail occassionally.
        success = []
        def inner_loop():
            hlcm.run(specification, coefficients, agent_set = households, debuglevel=1,
                      chunk_specification={'nchunks':1})
            
            # get results
            gridcells.compute_variables(["urbansim.gridcell.number_of_households"], 
                resources=Resources({"household":households}))
            result_more_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngrids/2)+1)
            return result_more_attractive
            
        expected_results = array(int(ngrids/2)*[nhouseholds*0.71/(ngrids/2)])
        self.run_stochastic_test(__file__, inner_loop, expected_results, 10, type="pearson", transformation=None)

        # Make sure it fails when expected distribution is different from actual.
        expected_results = array(int(ngrids/2)*[nhouseholds*0.61/(ngrids/2)])
        try:
            self.run_stochastic_test(__file__, inner_loop, expected_results, 10, type="poisson", transformation=None)
        except AssertionError:
            pass
           

if __name__=="__main__":
    opus_unittest.main() 
