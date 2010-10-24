# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from numpy import array, concatenate, sqrt, float32, logical_and
from opus_core.ndimage import standard_deviation
from matplotlib.pylab import plot, show
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.control_total_dataset import ControlTotalDataset
from urbansim.models.household_transition_model import HouseholdTransitionModel
from urbansim.datasets.household_characteristic_dataset import HouseholdCharacteristicDataset

def run_ALCM(niter):
    nhhs = 100
    ngcs = 10
    ngcs_attr = ngcs/2
    ngcs_noattr = ngcs - ngcs_attr
    hh_grid_ids = array(nhhs*[-1])
    
    storage = StorageFactory().get_storage('dict_storage')

    households_table_name = 'households'        
    storage.write_table(
        table_name = households_table_name,
        table_data = {
            'household_id': arange(nhhs)+1, 
            'grid_id': hh_grid_ids
            }
        )
        
    gridcells_table_name = 'gridcells'        
    storage.write_table(
        table_name = gridcells_table_name,
        table_data = {
            'grid_id': arange(ngcs)+1, 
            'cost':array(ngcs_attr*[100]+ngcs_noattr*[1000])
            }
        )

    households = HouseholdDataset(in_storage=storage, in_table_name=households_table_name)
    gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)
    
    # create coefficients and specification
    coefficients = Coefficients(names=('costcoef', ), values=(-0.001,))
    specification = EquationSpecification(variables=('gridcell.cost', ), coefficients=('costcoef', ))
    logger.be_quiet()
    result = zeros((niter,ngcs))
    for iter in range(niter):
        hlcm = HouseholdLocationChoiceModelCreator().get_model(location_set=gridcells, compute_capacity_flag=False, 
                choices = 'opus_core.random_choices_from_index', 
                sampler=None,
                #sample_size_locations = 30
                )
        hlcm.run(specification, coefficients, agent_set=households, debuglevel=1,
                  chunk_specification={'nchunks':1})
        
        # get results
        gridcells.compute_variables(['urbansim.gridcell.number_of_households'],
            resources=Resources({'household':households}))
        result_more_attractive = gridcells.get_attribute_by_id('number_of_households', arange(ngcs_attr)+1)
        result_less_attractive = gridcells.get_attribute_by_id('number_of_households', arange(ngcs_attr+1, ngcs+1))
        households.set_values_of_one_attribute(attribute='grid_id', values=hh_grid_ids)
        gridcells.delete_one_attribute('number_of_households')
        result[iter,:] = concatenate((result_more_attractive, result_less_attractive))
        #print result #, result_more_attractive.sum(), result_less_attractive.sum()
    return result

def run_HTM(niter):
        nhhs = 5000
        ngroups = 4
        nhhsg = int(nhhs/ngroups)
        nhhslg = nhhs-(ngroups-1)*nhhsg
        should_nhhs = nhhs-2000

        storage = StorageFactory().get_storage('dict_storage')

        hc_set_table_name = 'hc_set'        
        storage.write_table(
            table_name = hc_set_table_name,
            table_data = {
                'characteristic': array(4*['income']+4*['age_of_head']), 
                'min':array([0,1001,5001, 10001, 0, 31, 41, 61]), 
                'max':array([1000, 5000, 10000,-1, 30, 40, 60, -1])
                },
            )
            
        hct_set_table_name = 'hct_set'        
        storage.write_table(
            table_name = hct_set_table_name,
            table_data = {
                'year':array([2000]), 
                'total_number_of_households':array([should_nhhs])
                },
            )
            
        households_table_name = 'households'        
        storage.write_table(
            table_name = households_table_name,
            table_data = {
                'age_of_head': array(nhhsg/2*[18]+(nhhsg-nhhsg/2)*[35] +
                    nhhsg/2*[30] + (nhhsg-nhhsg/2)*[40] +
                    nhhsg/2*[38] + (nhhsg-nhhsg/2)*[65] + 
                    nhhslg/2*[50] + (nhhslg-nhhslg/2)*[80]
                    ),
                'income': array(nhhsg*[500] + nhhsg*[2000] + 
                    nhhsg*[7000] + nhhslg*[15000]
                    ),
                'household_id':arange(nhhs)+1
                },
            )

        hc_set = HouseholdCharacteristicDataset(in_storage=storage, in_table_name=hc_set_table_name)
        hct_set = ControlTotalDataset(
            in_storage = storage, 
            in_table_name = hct_set_table_name, 
            what = 'household', 
            id_name = ['year']
            )
          
        logger.be_quiet()
        result = zeros((niter,4))
        for iter in range(niter):
            households = HouseholdDataset(in_storage=storage, in_table_name=households_table_name)

            model = HouseholdTransitionModel()
            model.run(year=2000, household_set=households, control_totals=hct_set, characteristics=hc_set)
            income = households.get_attribute('income')
            age = households.get_attribute('age_of_head')
            idx1 = where(income <= 1000)[0]
            idx2 = where(logical_and(income <= 5000, income > 1000))[0]
            idx3 = where(logical_and(income <= 10000, income > 5000))[0]
            idx4 = where(income > 10000)[0]
            result[iter,:] = array([age[idx1].mean(), age[idx2].mean(), age[idx3].mean(), age[idx4].mean()])

        return result
    
if __name__=='__main__':
    from numpy import ma, arange, where, zeros
    from opus_core.resources import Resources
    from urbansim.datasets.gridcell_dataset import GridcellDataset
    from urbansim.datasets.household_dataset import HouseholdDataset
    from urbansim.datasets.job_dataset import JobDataset
    from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
    from opus_core.coefficients import Coefficients
    from opus_core.equation_specification import EquationSpecification
    from opus_core.tests.stochastic_test_case import StochasticTestCase
    from opus_core.logger import logger

    niter=100

    #result = run_ALCM(niter)
    result = run_HTM(niter)
    ngcs = result.shape[1]
    var = zeros(ngcs, dtype=float32)
    vart = zeros(ngcs, dtype=float32)
    means = zeros(ngcs, dtype=float32)
    meanst = zeros(ngcs, dtype=float32)
    for ig in range(ngcs):
        var[ig] = standard_deviation(result[:,ig])**2.0
        means[ig] = result[:,ig].mean()
        vart[ig] = standard_deviation(sqrt(result[:,ig]))**2.0
        meanst[ig] = sqrt(result[:,ig]).mean()
    print means
    print var
    print sqrt(var)
    plot(means,var, 'ro')
    show()
    print meanst
    print vart
    plot(meanst,vart, 'ro')
    show()