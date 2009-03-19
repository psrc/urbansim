# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import sys
from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator
from opus_core.equation_specification import EquationSpecification, load_specification_from_dictionary
from opus_core.storage_factory import StorageFactory
from urbansim.estimation.estimator import Estimator
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

    movers_location_id = agent_set.get_attribute(location_set.get_id_name()[0])[movers_index]
    movers_by_location = location_set.sum_over_ids(movers_location_id, ones(movers_index.size))
    location_set.add_attribute(movers_by_location, "movers")

    #submarket_ids = location_set.get_attribute("submarket_id")
    ## number of movers in each submarket
    #agent_set.compute_variables(['submarket_id=household.disaggregate(building.submarket_id)'])
    #movers_submarket_id = agent_set.get_attribute("submarket_id")[movers_index]
    #movers_by_submarket = submarkets.sum_over_ids(movers_submarket_id, ones(movers_index.size))
    #submarkets.add_primary_attribute(movers_by_submarket, "movers")
    ## number of residential_units and vacant_units in each submarket
    submarkets.compute_variables([
        "movers=submarket.aggregate(building.movers)",        
        "residential_units=submarket.aggregate(building.residential_units)",
        "vacant_units=submarket.aggregate(urbansim_parcel.building.vacant_residential_units)",
        ##lambda = (T - S)/(T - S - V) - V/M, where S is the secondary residence units and it is missing here
        "lambda_value=safe_array_divide( submarket.residential_units, submarket.residential_units - submarket.vacant_units) - safe_array_divide(submarket.vacant_units, submarket.movers)",
        ## supply = lambda * movers + vacant_units
        "supply=clip_to_zero(submarket.lambda_value * submarket.movers + submarket.vacant_units)"
    ])
    
    #lambda_value = safe_array_divide( submarkets.get_attribute("residential_units"), 
                                      #submarkets.get_attribute("residential_units") - submarkets.get_attribute("vacant_units") ) \
                 #- safe_array_divide( submarkets.get_attribute("vacant_units"), movers_by_submarket)
    
    #submarkets.add_primary_attribute(lambda_value, "lambda_value")
    #submarkets.compute_variables("supply=submarket.lambda_value * submarket.movers + submarket.vacant_units")    

    location_set.compute_variables("supply=clip_to_zero(building.disaggregate(submarket.lambda_value) * building.movers + building.vacant_residential_units)")
    

def get_households_for_estimation(agent_set, in_storage, 
                                  agents_for_estimation_table_name, 
                                  exclude_condition=None,
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

    exclude_ids = []
    if exclude_condition is not None:
        exclude_ids = agent_set.get_id_attribute()[where(agent_set.compute_variables(exclude_condition))]
        
    for id in exclude_ids:
        minus = agent_set.get_id_index(id)
        if minus in index:            
            index = index[index != minus]
        
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
    #residential_building_type[building_type_name=='condo_residential'] = 82
    residential_building_type[building_type_name=='multi_family_residential'] = 83
    building_types.add_primary_attribute(residential_building_type, 'residential_building_type_id')
    buildings.compute_variables(['residential_building_type_id=building.disaggregate(building_type.residential_building_type_id)'])

class HLCMEstimator(Estimator):

    def estimate(self, spec_var=None, spec_py=None,
                 movers_index = None,
                 submodel_string = "", 
                 alt_sample_size=None,
                 sampler = "opus_core.samplers.weighted_sampler",
                 weight_string = "supply",
                 aggregate_demand = False,
                 submarket_definition = ('zone', 'building_type_id'),
                 sample_size_from_each_stratum = 50
                 ):        
        """

        """
        
        t1 = time()        
        SimulationState().set_current_time(2000)

        dataset_pool=SessionConfiguration().get_dataset_pool()
        
        buildings = dataset_pool.get_dataset("building")
        agent_set = dataset_pool.get_dataset('household')
        #buildings.load_dataset()

        submarket_geography = dataset_pool.get_dataset(submarket_definition[0])
        intermediates = '[]'
        if submarket_geography.dataset_name == 'zone':
            intermediates = '[parcel]'
        elif submarket_geography.dataset_name == 'faz':
            intermediates = '[zone, parcel]'
        elif submarket_geography.dataset_name == 'large_area':
            intermediates = '[faz, zone, parcel]'
        
        submarket_id_expression = 'building.disaggregate(%s.%s, intermediates=%s) * 100' % \
                                                (submarket_geography.dataset_name, submarket_geography.get_id_name()[0],
                                                 intermediates)
        submarket_variables = ['%s=numpy.ceil(submarket.submarket_id / 100)' % submarket_geography.get_id_name()[0]]

        if submarket_definition[1] == 'residential_building_type_id':
            set_residential_building_types(dataset_pool.get_dataset("building_type"), dataset_pool.get_dataset("building"))
        if submarket_definition[1] != '':
            submarket_id_expression = submarket_id_expression + ' + building.%s'  % submarket_definition[1] 
            submarket_variables.append(submarket_definition[1] + '=submarket.submarket_id % 100' ) 
            
        submarkets = define_submarket(buildings, 
                                      submarket_id_expression,
                                      #"urbansim_parcel.building.zone_id*100 + building.residential_building_type_id",
                                      #"building.disaggregate(faz.large_area_id, intermediates=[zone, parcel]) * 100 + building.residential_building_type_id",
                                      compute_variables=submarket_variables + [
                                          "residential_units=submarket.aggregate(building.residential_units)",
                                          "number_of_buildings_with_non_zero_units=submarket.aggregate(building.residential_units > 0 )",
                                          "number_of_surveyed_households=submarket.aggregate(household.household_id > 5000000, intermediates=[building])",                                                     
                                                     ],
                                      #filter = 'numpy.logical_and(submarket.number_of_surveyed_households > 0, submarket.residential_units>0)',
                                      #filter = 'submarket.supply > 0',
                                      #"psrc_parcel.building.large_area_id*100 + building.residential_building_type_id",
                                      #compute_variables=['residential_building_type_id=submarket.submarket_id % 100',
                                                         #'large_area_id=numpy.ceil(submarket.submarket_id / 100)']
                                      #"psrc_parcel.building.large_area_id",
                                      #compute_variables=[#'residential_building_type_id=submarket.submarket_id % 100',
                                                         #'large_area_id=numpy.ceil(submarket.submarket_id)']

                                  )

        dataset_pool.add_datasets_if_not_included({'submarket':submarkets})        
        compute_lambda_and_supply(buildings, agent_set, movers_index, submarkets)

        submarket_filter = 'submarket.supply > 0'
        if submarket_filter is not None:
            from numpy import logical_not
            submarkets.remove_elements(index= where( logical_not(submarkets.compute_variables(submarket_filter)) )[0])
            submarkets.touch_attribute(submarkets.get_id_name()[0])
            buildings.touch_attribute(submarkets.get_id_name()[0])
            
        if self.save_estimation_results:
            out_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                storage_location=self.out_con)
        
        if spec_py is not None:
            reload(spec_py)
            spec_var = spec_py.specification
        
        if spec_var is not None:
            self.specification = load_specification_from_dictionary(spec_var)
        else:
            in_storage = StorageFactory().build_storage_for_dataset(type='sql_storage', 
                                                                    storage_location=self.in_con)
            self.specification = EquationSpecification(in_storage=in_storage)
            self.specification.load(in_table_name="household_location_choice_model_specification")
        
        self.model_name = "household_location_choice_model"

        agent_set, agents_index_for_estimation = get_households_for_estimation(agent_set,
                                                                               AttributeCache(),
                                                                               "households_for_estimation",
                                                                               exclude_condition="household.disaggregate(submarket.submarket_id, intermediates=[building])<=0",
                                                                           )
        agent_set.compute_variables("submarket_id=household.disaggregate(building.submarket_id)")
        agent_sample_rate = agents_index_for_estimation.size / float(movers_index.size)
        dataset_pool.add_datasets_if_not_included({'sample_rate': agent_sample_rate })

        if aggregate_demand:
            location_set = buildings
            aggregate_dataset = 'submarket'
            #weight_string = 'inv_submarket_supply = 1.0 / (building.disaggregate(submarket.number_of_agents(building))).astype(float32) * (building.disaggregate(submarket.submarket_id) > 0)'
            #weight_string = 'submarket_supply = (building.disaggregate(submarket.supply) > 0).astype(int32)'
            #weight_string = 'submarket_supply = building.disaggregate(submarket.supply) * (building.disaggregate(submarket.submarket_id) > 0).astype(float32)'
        else:
            location_set = submarkets
            aggregate_dataset = None
            #weight_string = 'supply'

        model = HouseholdLocationChoiceModelCreator().get_model(location_set=location_set,
                                                                #location_set=submarkets,  
                                                                #filter = 'building.disaggregate(submarket.submarket_id) > 0',
                                                                #filter = 'numpy.logical_and(submarket.number_of_surveyed_households > 0, submarket.residential_units>0)',
                                                                #filter = 'building.disaggregate(numpy.logical_and(submarket.number_of_buildings_with_non_zero_units > 5000, submarket.number_of_surveyed_households > 0))',
                                                                submodel_string=submodel_string,
                                                                sampler = sampler,
                                                                #estimation_size_agents = agent_sample_rate * 100/20,    
                                                                # proportion of the agent set that should be used for the estimation
                                                                sample_size_locations = alt_sample_size,
                                                                #sample_proportion_locations = 1.0/1000,
                                                                # choice set size (includes current location)
                                                                compute_capacity_flag = True,
                                                                probabilities = "opus_core.mnl_probabilities",
                                                                choices = "urbansim.lottery_choices",
                                                                #run_config = Resources({"capacity_string":"supply"}), 
                                                                estimate_config = Resources({"capacity_string":"supply",
                                                                                             "weights_for_estimation_string":weight_string,
                                                                                             "aggregate_to_dataset":aggregate_dataset,
                                                                                             "stratum": "building.disaggregate(submarket.submarket_id)",
                                                                                             "sample_size_from_each_stratum": sample_size_from_each_stratum,
                                                                                             #"index2":where(submarkets.compute_variables('submarket.number_of_surveyed_households > 0'))[0],
                                                                                             #"sample_rate": 1.0/5000,
                                                                                             #"sample_size_from_chosen_stratum": 0,
                                                                                             "include_chosen_choice": True
                                                                                             }))

        
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
    from my_estimation_config import my_configuration
    from optparse import OptionParser
    
    parser = OptionParser(usage="python %prog [options]", description="")
    parser.add_option("--aggregate-demand", dest="aggregate_demand", default = False,
                      action="store_true", help="")
    parser.add_option("--alt-sample-size", dest="alt_sample_size", default = 1000,
                      action="store", help="")
    parser.add_option("--sampler", dest="sampler", default = "weighted_sampler",
                      action="store", help="")
    parser.add_option("--weight-string", dest="weight_string", default="supply",
                      action="store", help="")
    parser.add_option("--submarket-geography", dest="submarket_geography",
                      default='large_area', action="store", help="")
    parser.add_option("--submarket-attribute", dest="submarket_attribute",
                      default='residential_building_type_id',
                      action="store", help="")
    parser.add_option("--sample-size-from-each-stratum", dest="sample_size_from_each_stratum",
                      default=50, action="store", help="")
    
    (options, args) = parser.parse_args()

    #try:aggregate_demand = bool(int(sys.argv[1]))
    #except:aggregate_demand = False
    
    if options.aggregate_demand:
        import hlcm_specification
    else:
        import hlcm_specification_submarket as hlcm_specification        

    alt_sample_size = options.alt_sample_size
    #try:alt_sample_size = int(sys.argv[2])
    #except:alt_sample_size = 1000 #None #1027 #1112

    sampler = None
    if options.sampler is not None:
        sampler = "opus_core.samplers.%s" % options.sampler
    
    aggregate_lookup = {True:'aggregate demand', False:'aggregate choice set'}
    
    date_time_str=strftime("%Y_%m_%d__%H_%M", localtime())
    #agent_sample_rate_str = '' #"__ASR_" + str(agent_sample_rate)
    #alt_sample_size_str = "_ALT_" + str(alt_sample_size)
    logger.enable_memory_logging()

    if options.sampler == 'weighted_sampler':
        file_name_pattern = date_time_str + "_alt_size_%s_%s_%s" % ( alt_sample_size, options.sampler, 
                                                                    '_'.join(aggregate_lookup[options.aggregate_demand].split(' ')) )
        logger.enable_file_logging( file_name_pattern + '__run.txt')
        info_file = file_name_pattern + "__info.txt"
        logger.log_status("Constrained Estimation with alternatvie sample size %s from %s for %s" % \
                          (alt_sample_size, options.sampler, aggregate_lookup[options.aggregate_demand]))
    elif options.sampler == 'stratified_sampler':
        file_name_pattern = date_time_str + "_alt_size_%s_per_stratum_%s_%s" % ( options.sample_size_from_each_stratum, 
                                                                                options.sampler, 
                                                                                '_'.join(aggregate_lookup[options.aggregate_demand].split(' ')) )
        logger.enable_file_logging( file_name_pattern + '__run.txt')
        info_file = file_name_pattern + "__info.txt"
        logger.log_status("Constrained Estimation with alt sample size %s per stratum from %s for %s" % \
                          (options.sample_size_from_each_stratum, options.sampler, aggregate_lookup[options.aggregate_demand]))
    
    if options.sampler is None:
        file_name_pattern = date_time_str + "_all_choice_%s" % '_'.join(aggregate_lookup[options.aggregate_demand].split(' '))
        logger.enable_file_logging( file_name_pattern + '__run.txt')
        info_file = file_name_pattern + "__info.txt"
        logger.log_status("Constrained Estimation with alternatives of full choice set for %s" % \
                          aggregate_lookup[options.aggregate_demand])
    else:
        logger.log_status("weight_string: " + options.weight_string )
        
    logger.log_status("submarket defined by %s x %s " % (options.submarket_geography, options.submarket_attribute) )

    estimator = HLCMEstimator(config=my_configuration,
                              save_estimation_results=False)
    estimator.simulation_state.set_current_time(2000)
    
    attribute_cache = AttributeCache()
    sc = SessionConfiguration()
    CLOSE = 0.005   #criterion for convergence
    sc.put_data({'CLOSE':CLOSE, 'info_file':info_file})
    
    seed(71) # was: seed(71,110)

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
                       submarket_definition=(options.submarket_geography, options.submarket_attribute),
                       alt_sample_size=alt_sample_size,
                       sampler=sampler,
                       weight_string = options.weight_string,
                       aggregate_demand=options.aggregate_demand,
                       sample_size_from_each_stratum = int(options.sample_size_from_each_stratum),
                   )

