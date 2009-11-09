# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

if __name__=="__main__":
    from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
    from numpy import concatenate, logical_and
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
    from opus_core.storage_factory import StorageFactory
    from urbansim.datasets.control_total_dataset import ControlTotalDataset
    from urbansim.models.household_transition_model import HouseholdTransitionModel
    from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset
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
            hh_grid_ids = array(nhhs*[-1])
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
                result = concatenate((result_more_attractive, result_less_attractive))
                #print result #, result_more_attractive.sum(), result_less_attractive.sum()
                return result
                
            expected_results = array(ngcs_attr*[nhhs*0.71/float(ngcs_attr)] + ngcs_noattr*[nhhs*0.29/float(ngcs_noattr)])
            #print expected_results
            R = 1000
            #r = [2, 5, 10, 50, 100, 1000]
            r = [2, 5, 10, 15, 20]
            #r=[5]
            levels = [0.05,  0.01]
            #levels = [0.05]
            power = zeros((len(r), len(levels)))            
            for ir in range(len(r)):
                for il in range(len(levels)):
                    print "r=", r[ir],", level=",levels[il]
                    seed(1)
                    for iR in range(R):                   
                        try:
                            self.run_stochastic_test(__file__, run_model, expected_results, 
                                                     r[ir], significance_level=levels[il])
                        except:
                            power[ir,il]=power[ir,il]+1
                    print "Power: ",power[ir,il]/float(R)
            print power/float(R)
            
        def xtest_HTM_controlling_with_marginal_characteristics(self):
            nhhs = 5000
            ngroups = 4
            nhhsg = int(nhhs/ngroups)
            nhhslg = nhhs-(ngroups-1)*nhhsg
            should_nhhs = nhhs-2000
            #logger.be_quiet()
            household_data = {"age_of_head": array(nhhsg/2*[18]+(nhhsg-nhhsg/2)*[35] +
                                nhhsg/2*[30] + (nhhsg-nhhsg/2)*[40] + 
                                nhhsg/2*[38] + (nhhsg-nhhsg/2)*[65] + 
                                nhhslg/2*[50] + (nhhslg-nhhslg/2)*[80]),
                               "income": array(nhhsg*[500] + nhhsg*[2000] + 
                                       nhhsg*[7000] + nhhslg*[15000]),
                               "household_id":arange(nhhs)+1}
            household_characteristics_for_ht_data = {"characteristic": array(4*["income"]+4*["age_of_head"]), 
                                                      "min":array([0,1001,5001, 10001, 0, 31, 41, 61]), 
                                                      "max":array([1000, 5000, 10000,-1, 30, 40, 60, -1])}
            annual_household_control_totals_data = {"year":array([2000]),
                                                     "total_number_of_households":array([should_nhhs])}
            
            storage = StorageFactory().get_storage('dict_storage')
           
            storage.write_table(table_name = 'hc_set', table_data = household_characteristics_for_ht_data)
            hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

            storage.write_table(table_name = 'hct_set', table_data = annual_household_control_totals_data)
            hct_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hct_set')
            
            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='households')

            income = households.get_attribute("income")
            age = households.get_attribute("age_of_head")
            idx1 = where(income <= 1000)[0]
            idx2 = where(logical_and(income <= 5000, income > 1000))[0]
            idx3 = where(logical_and(income <= 10000, income > 5000))[0]
            idx4 = where(income > 10000)[0]
            expected_results = array([age[idx1].mean(), age[idx2].mean(), age[idx3].mean(), age[idx4].mean()]) 
                  
            def run_model():
                storage.write_table(table_name = 'households', table_data = household_data)
                households = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='households')

                model = HouseholdTransitionModel()
                model.run(year=2000, household_set=households, control_totals=hct_set, characteristics=hc_set)
                income = households.get_attribute("income")
                age = households.get_attribute("age_of_head")
                idx1 = where(income <= 1000)[0]
                idx2 = where(logical_and(income <= 5000, income > 1000))[0]
                idx3 = where(logical_and(income <= 10000, income > 5000))[0]
                idx4 = where(income > 10000)[0]
                results = array([age[idx1].mean(), age[idx2].mean(), age[idx3].mean(), age[idx4].mean()])
                print results
                return results
            print expected_results      
            R = 2
            #r = [2, 5, 10, 50, 100, 1000]
            #r = [2, 5, 10, 15, 20]
            r=[10]
            #levels = [0.05,  0.01]
            levels = [0.05, 0.01]
            power = zeros((len(r), len(levels)))            
            for ir in range(len(r)):
                for il in range(len(levels)):
                    print "r=", r[ir],", level=",levels[il]
                    seed(1)
                    for iR in range(R):                   
                        try:
                            self.run_stochastic_test(__file__, run_model, expected_results, 
                                                     r[ir], significance_level=levels[il], transformation=None)
                        except:
                            power[ir,il]=power[ir,il]+1
                    print "Power: ",power[ir,il]/float(R)
            print power/float(R)     
            
        def xtest_power_HTM_controlling_with_marginal_characteristics(self):
            nhhs = 5000
            ngroups = 4
            nhhsg = int(nhhs/ngroups)
            nhhslg = nhhs-(ngroups-1)*nhhsg
            should_nhhs = nhhs-2000
            logger.be_quiet()
            household_data = {"age_of_head": array(nhhsg/2*[18]+(nhhsg-nhhsg/2)*[35] +
                                nhhsg/2*[30] + (nhhsg-nhhsg/2)*[40] + 
                                nhhsg/2*[38] + (nhhsg-nhhsg/2)*[65] + 
                                nhhslg/2*[50] + (nhhslg-nhhslg/2)*[80]),
                               "income": array(nhhsg*[500] + nhhsg*[2000] + 
                                       nhhsg*[7000] + nhhslg*[15000]),
                               "household_id":arange(nhhs)+1}
            household_characteristics_for_ht_data = {"characteristic": array(4*["income"]+4*["age_of_head"]), 
                                                      "min":array([0,1001,5001, 10001, 0, 31, 41, 61]), 
                                                      "max":array([1000, 5000, 10000,-1, 30, 40, 60, -1])}
            annual_household_control_totals_data = {"year":array([2000]),
                                                     "total_number_of_households":array([should_nhhs])}
            
            storage = StorageFactory().get_storage('dict_storage')
           
            storage.write_table(table_name = 'hc_set', table_data = household_characteristics_for_ht_data)
            hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hc_set')

            storage.write_table(table_name = 'hct_set', table_data = annual_household_control_totals_data)
            hct_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='hct_set')
            
            storage.write_table(table_name = 'households', table_data = household_data)
            households = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='households')

            income = households.get_attribute("income")
            age = households.get_attribute("age_of_head")
            idx1 = where(income <= 1000)[0]
            idx2 = where(logical_and(income <= 5000, income > 1000))[0]
            idx3 = where(logical_and(income <= 10000, income > 5000))[0]
            idx4 = where(income > 10000)[0]
            expected_results = array([age[idx1].mean(), age[idx2].mean(), age[idx3].mean(), age[idx4].mean()]) 
                  
            def run_model():
                storage.write_table(table_name = 'households', table_data = household_data)
                households = HouseholdCharacteristicDataset(in_storage=storage, in_table_name='households')
            
                model = HouseholdTransitionModel()
                model.run(year=2000, household_set=households, control_totals=hct_set, characteristics=hc_set)
                income = households.get_attribute("income")
                age = households.get_attribute("age_of_head")
                idx1 = where(income <= 1000)[0]
                idx2 = where(logical_and(income <= 5000, income > 1000))[0]
                idx3 = where(logical_and(income <= 10000, income > 5000))[0]
                idx4 = where(income > 10000)[0]
                results = array([age[idx1].mean(), age[idx2].mean(), age[idx3].mean(), age[idx4].mean()])
                results[-1] = results[-1]+self.wrong_number
                #print results
                return results
            #print expected_results      
            R = 1000
            #r = [2, 5, 10, 50, 100, 1000]
            #r = [2, 5, 10, 15, 20]
            r=[2,5]
            levels = [0.05,  0.01]
            #levels = [0.05]
            #wrong_numbers = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
            wrong_numbers = [1]
            for wn in wrong_numbers:
                self.wrong_number = wn
                print "Wrong number = ", self.wrong_number
                power = zeros((len(r), len(levels)))            
                for ir in range(len(r)):
                    for il in range(len(levels)):
                        print "r=", r[ir],", level=",levels[il]
                        seed(1)
                        for iR in range(R):                  
                            try:
                                self.run_stochastic_test(__file__, run_model, expected_results, 
                                                         r[ir], significance_level=levels[il], transformation=None)
                            except:
                                power[ir,il]=power[ir,il]+1
                        print "Power: ",power[ir,il]/float(R)
                print power/float(R)                                                 
    opus_unittest.main()
