# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

if __name__=="__main__":
    from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
    from numpy import concatenate
    from scipy.ndimage import standard_deviation
    from numpy.random import seed
    
    from opus_core.tests import opus_unittest
    from numpy import array, ma, arange, where, zeros
    from opus_core.resources import Resources
    from urbansim.datasets.gridcell_dataset import GridcellDataset
    from urbansim.datasets.household_dataset import HouseholdDataset
    from urbansim.datasets.job_dataset import JobDataset
    from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
    from opus_core.coefficients import Coefficients
    from opus_core.equation_specification import EquationSpecification
    from opus_core.tests.stochastic_test_case import StochasticTestCase
    from opus_core.logger import logger
    from opus_core.storage_factory import StorageFactory
    
        
    class Test(StochasticTestCase):
        def test_agents_go_to_attractive_locations(self):
            """100 gridcells - 50 with cost 100, 50 with cost 1000, no capacity restrictions
            10,000 households
            We set the coefficient value for cost -0.001. This leads to probability
            proportion 0.71 (less costly gridcells) to 0.29 (expensive gridcells)
            (derived from the logit formula)
            """
            nhhs = 1000
            ngcs = 50
            ngcs_attr = ngcs/2
            ngcs_noattr = ngcs - ngcs_attr
            #print ngcs_attr, ngcs_noattr
            hh_grid_ids = array([-1]*nhhs)
            household_data = {"household_id": arange(nhhs)+1, "grid_id": hh_grid_ids} 
            gridcell_data = {"grid_id": arange(ngcs)+1, "cost":array(ngcs_attr*[100]+ngcs_noattr*[1000])} 
            
            storage = StorageFactory().get_storage('dict_storage')
      
            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdDataset(in_storage=storage, in_table_name='households')
                   
            storage.write_table(table_name = 'gridcells', table_data = gridcell_data)
            gridcells = HouseholdDataset(in_storage=storage, in_table_name='gridcells')
                        
            # create coefficients and specification
            coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
            specification = EquationSpecification(variables=("gridcell.cost", ), coefficients=("costcoef", ))
            logger.be_quiet()
    
            # check the individual gridcells
            def run_model():
                hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False, 
                        choices = "opus_core.random_choices_from_index",
                        sampler=None,
                        #sample_size_locations = 30
                        )
                hlcm.run(specification, coefficients, agent_set=households, debuglevel=1,
                          chunk_specification={'nchunks':1})
                
                # get results
                gridcells.compute_variables(["urbansim.gridcell.number_of_households"],
                    resources=Resources({"household":households}))
                result_more_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr)+1)
                result_less_attractive = gridcells.get_attribute_by_id("number_of_households", arange(ngcs_attr+1, ngcs+1))
                households.set_values_of_one_attribute(attribute="grid_id", values=hh_grid_ids)
                gridcells.delete_one_attribute("number_of_households")
                result_less_attractive[0]=result_less_attractive[0] + self.wrong_number
                result = concatenate((result_more_attractive, result_less_attractive))
                #print standard_deviation(result[ngcs_attr:(ngcs-1)])
                return result
                
            expected_results = array(ngcs_attr*[nhhs*0.71/float(ngcs_attr)] + ngcs_noattr*[nhhs*0.29/float(ngcs_noattr)])
            #print expected_results
            R = 1000
            #r = [2, 5, 10, 50, 100, 1000]
            r = [2, 5, 10, 15, 20]
            #r=[20]
            levels = [0.05, 0.01]
            #levels = [0.01]
            #wrong_numbers = [8, 10, 12, 14, 16, 18, 21, 23]
            #wrong_numbers = [2, 4, 6, 8, 10, 12, 14, 16]
            #wrong_numbers = [3, 6, 9, 12, 15, 18]
            wrong_numbers = [12, 15, 18]
            for wn in wrong_numbers:
                self.wrong_number = wn
                print "Wrong number =", self.wrong_number
                power = zeros((len(r), len(levels)))            
                for ir in range(len(r)):
                    for il in range(len(levels)):
                        print "r =", r[ir],", level =",levels[il]
                        seed(1)
                        for iR in range(R):                   
                            try:
                                self.run_stochastic_test(__file__, run_model, expected_results, 
                                                         r[ir], significance_level=levels[il])
                            except:
                                power[ir,il]=power[ir,il]+1
                        print "Power:",power[ir,il]/float(R)
                print power/float(R)
    
    opus_unittest.main() 