#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import sys
from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from urbansim.estimation.estimator import Estimator, load_specification_from_variable
from opus_core.resources import Resources
from opus_core.logger import logger
from numpy.random import seed
from opus_core.misc import unique_values, safe_array_divide
from numpy import arange, where, array, float32, concatenate, ones, zeros
from time import time, localtime, strftime
from opus_core.datasets.dataset import Dataset
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from household_location_choice_model_with_price_adj import define_submarket

def compute_lambda_and_supply(location_set, agent_set, movers_index, submarkets):
    submarket_ids = location_set.get_attribute("submarket_id")
    ## number of movers in each submarket
    agent_set.compute_variables(['submarket_id=household.disaggregate(building.submarket_id)'])
    movers_submarket_id = agent_set.get_attribute("submarket_id")[movers_index]
    movers_by_submarket = submarkets.sum_over_ids(movers_submarket_id, ones(movers_index.size))
    ## number of total_units and vacant_units in each submarket
    submarkets.compute_variables(["total_units=submarket.aggregate(building.residential_units)",
                                 "vacant_units=submarket.aggregate(urbansim_parcel.building.vacant_residential_units)"])
    submarkets.add_primary_attribute(movers_by_submarket, "movers")
    
    ##lambda = (T - S)/(T - S - V) - V/M, where S is the secondary residence units and it is missing here
    lambda_value = safe_array_divide( submarkets.get_attribute("total_units"), 
                                      submarkets.get_attribute("total_units") - submarkets.get_attribute("vacant_units") ) \
                 - safe_array_divide( submarkets.get_attribute("vacant_units"), movers_by_submarket)
    
    submarkets.add_primary_attribute(lambda_value, "lambda_value")

    ## supply = lambda * movers + vacant_units
    movers_building_id = agent_set.get_attribute("building_id")[movers_index]
    movers_by_building = location_set.sum_over_ids(movers_building_id, ones(movers_index.size))
    location_set.add_attribute(movers_by_building, "movers")
    location_set.compute_variables("supply=(building.disaggregate(submarket.lambda_value)) * building.movers + building.vacant_residential_units")
    

def get_households_for_estimation(agent_set, in_storage, 
                                  agents_for_estimation_table_name, 
                                  join_datasets=True):
    estimation_set = Dataset(in_storage = in_storage,
                             in_table_name=agents_for_estimation_table_name,
                             id_name=agent_set.get_id_name(), 
                             dataset_name=agent_set.get_dataset_name())
    agent_set.unload_primary_attributes()
    agent_set.load_dataset(attributes='*')
    estimation_set.load_dataset(attributes=agent_set.get_primary_attribute_names())
    if join_datasets:
        agent_set.join_by_rows(estimation_set, 
                               require_all_attributes=False,
                               change_ids_if_not_unique=True)
        index = arange(agent_set.size()-estimation_set.size(),agent_set.size())
    else:
        index = agent_set.get_id_index(estimation_set.get_id_attribute())
        
    return (agent_set, index)

def set_residential_building_types(building_types, buildings):
    """
    residential_building_type_id:
    81 - sfr (sfh + mobile home)
    82 - condo
    83 - mfr (multi-family apt)
    84 - others
    """
    #building_types = dataset_pool.get_dataset('building_type')
    residential_building_type = 84 + zeros(building_types.size(), dtype='int32')  # 84 by default
    building_type_name = building_types.get_attribute('building_type_name')
    residential_building_type[building_type_name=='single_family_residential'] = 81
    residential_building_type[building_type_name=='condo_residential'] = 82
    residential_building_type[building_type_name=='multi_family_residential'] = 83
    building_types.add_primary_attribute(residential_building_type, 'residential_building_type_id')
    buildings.compute_variables(['residential_building_type_id=building.disaggregate(building_type.residential_building_type_id)'])

class HLCMEstimator(Estimator):

    def estimate(self, spec_var=None, spec_py=None,
                 movers_index = None,
                 submodel_string = "workers", 
                 #agent_sample_rate=0.005, 
                 alt_sample_size=None,
                 #sampler = "opus_core.samplers.stratified_sampler"
                 sampler = "opus_core.samplers.weighted_sampler"
                 #sampler = None
                 ):        
        """

        """
        if alt_sample_size is None:
            sampler = None
        
        t1 = time()        
        SimulationState().get_current_time()
        SimulationState().set_current_time(2000)

        dataset_pool=SessionConfiguration().get_dataset_pool()
        
        location_set = dataset_pool.get_dataset("building")
        agent_set = dataset_pool.get_dataset('household')
        location_set.load_dataset()
        set_residential_building_types(dataset_pool.get_dataset("building_type"), dataset_pool.get_dataset("building"))
        submarkets = define_submarket(location_set, 
                                      "urbansim_parcel.building.zone_id*100 + building.residential_building_type_id",
                                      compute_variables=['residential_building_type_id=submarket.submarket_id % 100',
                                                         'zone_id=numpy.ceil(submarket.submarket_id / 100)'
                                                        ]
                                  )

        dataset_pool.add_datasets_if_not_included({'submarket':submarkets})
        
        compute_lambda_and_supply(location_set, agent_set, movers_index, submarkets)
        submarkets.compute_variables("supply=submarket.aggregate(building.supply)")
        
        #depts, lambda_value = compute_lambda(self.nbs)
        #supply, vacancy_rate = compute_supply_and_vacancy_rate(self.nbs, depts, lambda_value)
        #self.nbs.set_values_of_one_attribute("supply", supply)

        if self.save_estimation_results:
            out_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                storage_location=self.out_con)
        
        if spec_py is not None:
            reload(spec_py)
            spec_var = spec_py.specification
        
        if spec_var is not None:
            self.specification = load_specification_from_variable(spec_var)
        else:
            in_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                                                                    storage_location=self.in_con)
            self.specification = EquationSpecification(in_storage=in_storage)
            self.specification.load(in_table_name="household_location_choice_model_specification")
        
        seed(71) # was: seed(71,110)
        self.model_name = "household_location_choice_model"

        model = HouseholdLocationChoiceModelCreator().get_model(#location_set=location_set,
                                                                location_set=submarkets,  
                                                                submodel_string=submodel_string,
                                                                sampler = sampler,
                                                                #estimation_size_agents = agent_sample_rate * 100/20,    
                                                                # proportion of the agent set that should be used for the estimation
                                                                sample_size_locations = alt_sample_size,  
                                                                # choice set size (includes current location)
                                                                compute_capacity_flag = True,
                                                                probabilities = "opus_core.mnl_probabilities",
                                                                choices = "urbansim.lottery_choices",
                                                                run_config = Resources({"capacity_string":"supply"}), 
                                                                estimate_config = Resources({"capacity_string":"supply",
                                                                                             "compute_capacity_flag":True,
#                                                                                             "stratum": "building.submarket_id",
 #                                                                                            "sample_size_from_each_stratum": 1,
  #                                                                                           "sample_size_from_chosen_stratum": 0,
   #                                                                                          "include_chosen_choice": True
                                                                                             }))

        
        agent_set, agents_index_for_estimation = get_households_for_estimation(agent_set,
                                                                               AttributeCache(),
                                                                               "households_for_estimation")
        agent_set.compute_variables("submarket_id=household.disaggregate(building.submarket_id)")
        agent_sample_rate = agents_index_for_estimation.size / float(movers_index.size)
        dataset_pool.add_datasets_if_not_included({'sample_rate': agent_sample_rate })
        # was dataset_pool.add_datasets_if_not_included({'sample_rate':agent_sample_rate})        
        self.result = model.estimate(self.specification, 
                                     agent_set=agent_set, 
                                     agents_index=agents_index_for_estimation, 
                                     debuglevel=self.debuglevel,
                                     procedure="urbansim.constrain_estimation_bhhh_two_loops" ) #"urbansim.constrain_estimation_bhhh"

        #save estimation results
        if self.save_estimation_results:    
            self.save_results(out_storage)
            
        logger.log_status("Estimation done. " + str(time()-t1) + " s")

if __name__ == "__main__":
    try:import wingdbstub
    except:pass
    
    # run estimation with given specification
    #import hlcm_specification
    import hlcm_specification_submarket as hlcm_specification
    from my_estimation_config import my_configuration

    #try:agent_sample_rate = float(sys.argv[1])
    #except:agent_sample_rate = 0.005

    try:alt_sample_size = int(sys.argv[2])
    except:alt_sample_size = None
        
    date_time_str=strftime("%Y_%m_%d__%H_%M", localtime())
    agent_sample_rate_str = '' #"__ASR_" + str(agent_sample_rate)
    alt_sample_size_str = "_ALT_" + str(alt_sample_size)
    info_file = date_time_str + agent_sample_rate_str + alt_sample_size_str + "__info.txt"
    logger.enable_file_logging(date_time_str + agent_sample_rate_str + alt_sample_size_str + "__run.txt")
    logger.enable_memory_logging()
    #logger.log_status("Constrained Estimation with agent sample rate of %s and alternatvie sample size %s\n" % \
                      #(agent_sample_rate, alt_sample_size))

    estimator = HLCMEstimator(config=my_configuration,
                              save_estimation_results=False)
    estimator.simulation_state.set_current_time(2000)
    #ss = SimulationState()
    #ss.set_current_time(2000)    
    #ss.set_cache_directory(my_configuration['cache_directory'])

    #attribute_cache = AttributeCache()
    #sc = SessionConfiguration(#new_instance=True,
                         #package_order=my_configuration['dataset_pool_configuration'].package_order,
                         #package_order_exceptions=my_configuration['dataset_pool_configuration'].package_order_exceptions,
                         #in_storage=attribute_cache)
    
    attribute_cache = AttributeCache()
    sc = SessionConfiguration()
    CLOSE = 0.001   #criterion for convergence
    sc.put_data({'CLOSE':CLOSE, 'info_file':info_file})
    
    ## relocate movers
    from urbansim.models.household_relocation_model_creator import HouseholdRelocationModelCreator
    hrm = HouseholdRelocationModelCreator().get_model(probabilities='urbansim.household_relocation_probabilities',
                                                      location_id_name='building_id' )
    hrm_resources = hrm.prepare_for_run(rate_storage=attribute_cache,
                                        rate_table='annual_relocation_rates_for_households',
                                        what='households')
    hrm_index = hrm.run(agent_set=sc.get_dataset_from_pool('household'),
                        resources=hrm_resources)
    
    estimator.estimate(spec_py=hlcm_specification, 
                       movers_index=hrm_index, 
                       alt_sample_size=alt_sample_size)

