# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.configuration import Configuration
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from urbansim.model_coordinators.model_system import ModelSystem
#from opus_core.choice_model import ChoiceModel
from opus_core.configurations.xml_configuration import XMLConfiguration
from urbansim.estimation.estimation_runner import EstimationRunner
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import probsample_noreplace
from numpy.random import randint
from numpy import where, arange
import cPickle

class options(object):
    meta_models = [['residential_building_type_choice_model', 
                    'tenure_choice_model', 
                    'auto_ownership_choice_model', 
                    'household_location_choice_model',
                    'worker1_workplace_choice_model'],
                   ]
    market_share = [['market_share=building_type.aggregate(building.residential_units)',
                     '',
                     'market_share=car.number_of_agents(household)',
                     'market_share=district.aggregate(district_traffic_flow.share)',
                     'market_share=district.aggregate(district_traffic_flow.share)'
                    ] 
                    ]
    choice_type = [['CLASSIFICATION', 'CLASSIFICATION', 'CLASSIFICATION', 'CLASSIFICATION', 'CLASSIFICATION']]
    #CLASSIFICATION = 1
    #RATING = 2
    #REGRESSION = 3
    xml_configuration = '/home/lmwang/opus/src/inprocess/lmwang/psrc_parcel_test.xml'
    scenario_name = 'psrc_baseline_test'
    year = 2000
    agent_set = 'household'
    sample_size = 5000 #for regularization
    agents_index = None
    agents_filter = 'psrc_parcel.household.customized_run_filter'
    pickle_filename = 'em_data.pickle'
    seed = 100
    nchunks = 1 ##TODO

if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    from psrc_parcel.household.aliases import aliases
    aliases += ["customized_est_filter= (household.household_id > 6000000) * " + \
                "numpy.logical_or(household.tenure==1, household.tenure==3) * " + \
                #numpy.setmember1d(household.tenure, (1,3)) * \ ## buggy
                "(( (psrc_parcel.household.building_type_id==4) + (psrc_parcel.household.building_type_id==11) + (psrc_parcel.household.building_type_id==12) + (psrc_parcel.household.building_type_id==19)) >= 1) * " + \
                #numpy.setmember1d(psrc_parcel.household.building_type_id, (4, 11, 12, 19)) * \ ##ideally the above line can be replaced with this, but this is buggy
                "(household.aggregate((person.worker1==1)*(urbansim_parcel.person.is_non_home_based_worker_with_job)))",
               "customized_run_filter= household.aggregate(urbansim_parcel.person.is_non_home_based_worker)>=1"
               ]
    xmlconfig = XMLConfiguration(options.xml_configuration)
    ## training data (start_estimation)
    training_data = []
    for h, hierarchy in enumerate(options.meta_models):
        model_data = []
        for i, model_name in enumerate(hierarchy):
            logger.start_block('%s' % model_name)
            estimator = EstimationRunner(model=model_name, 
                                         specification_module=None, 
                                         xml_configuration=xmlconfig, 
                                         model_group=None,
                                         configuration=None,
                                         save_estimation_results=True)
            #estimator = EstimationRunner(model=model_name,
                                         #xml_configuration=xmlconfig,
                                         #save_estimation_results=False)
            
            estimator.estimate()
            m = estimator.get_model()
            model_system = estimator.model_system
            dataset_pool=model_system.run_year_namespace["dataset_pool"]

            submodels = m.model_interaction.get_submodels()
            assert len(submodels) == 1
            submodel = submodels[0]
            
            #m.get_all_data(submodel).shape
            #data = m.get_all_data(submodel)
            mi = m.model_interaction
            data = mi.interaction_dataset.create_logit_data(mi.submodel_coefficients[submodel],
                                                            index=m.observations_mapping[submodel])

            is_chosen = m.model_interaction.get_chosen_choice()
            index_chosen = where(is_chosen)[1]
            assert index_chosen.size == data.shape[0]
            
            sampling_prob = mi.interaction_dataset['__sampling_probability'] \
                          if '__sampling_probability' in mi.interaction_dataset.get_known_attribute_names() \
                          else None            
            variable_names = m.model_interaction.get_variable_names(submodel)
            outputvar = model_system.run_year_namespace['outputvar']
            results_name = outputvar.strip('()').split(',')[1].strip()
            estimation_results = model_system.run_year_namespace[results_name]
            
            model_data.append({"data":data, 
                               'index_chosen':index_chosen,
                               'sampling_probability': sampling_prob,
                               'variable_names':variable_names,
                               'estimation_results':estimation_results,
                               'model_name':model_name,
                               'choice_type':options.choice_type[h][i]
                               })

            if options.market_share[h][i]:
                ms_expression = options.market_share[h][i]
                ms_variablename = VariableName(ms_expression)
        
                dataset_name = ms_variablename.get_dataset_name()
                ds = model_system.run_year_namespace[dataset_name] or model_system.run_year_namespace['datasets'][dataset_name]
                id_name = ds.get_id_name()[0]
                ds.compute_variables([ms_variablename], dataset_pool=dataset_pool)
                ms = ds.get_multiple_attributes([id_name, ms_variablename.get_alias()])
                
                market_ids = m.choice_set.compute_one_variable_with_unknown_package( id_name, dataset_pool=dataset_pool)
                market_ids_2d = market_ids[m.model_interaction.get_choice_index()]
                model_data[i].update({'market_id':market_ids_2d, 'market_share':ms})

            logger.end_block()
        training_data.append(model_data)
        
    config = xmlconfig.get_run_configuration(options.scenario_name)
    if not options.agents_index:
        agent_set = dataset_pool.get_dataset(options.agent_set)
        agents_size = agent_set.size()
        if options.agents_filter:
            is_valid = agent_set.compute_variables(options.agents_filter)
            options.agents_index = probsample_noreplace(arange(agents_size),
                                                        options.sample_size,
                                                        prob_array=is_valid
                                                       ).tolist()
        else:
            options.agents_index = randint(0, agents_size, size=options.sample_size).tolist()

    ## regularization data
    population_data = []
    for h, hierarchy in enumerate(options.meta_models):
        model_data = []
        for i, model_name in enumerate(hierarchy):
            logger.start_block('%s' % model_name)

            config['models_configuration'][model_name]['controller']['run']['arguments']['agents_index'] = options.agents_index
            config['models'] = [{model_name:["run"]}]
            config['years'] = [options.year, options.year]
            config['seed'] = options.seed
            config["datasets_to_cache_after_each_model"]=[]
            config['flush_variables'] = False
            
            config = Resources(config)       
            cache_directory = config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy
            simulation_state = SimulationState(new_instance=True, base_cache_dir=cache_directory)
            config['cache_directory'] = cache_directory
            
            SessionConfiguration(new_instance=True,
                                 package_order=config['dataset_pool_configuration'].package_order,
                                 in_storage=AttributeCache())
            
            model_system = ModelSystem()
            model_system.run(config, write_datasets_to_cache_at_end_of_year=False)
            
            m = model_system.run_year_namespace["model"]
            mi = m.model_interaction
            submodels = m.model_interaction.get_submodels()
            assert len(submodels) == 1
            submodel = submodels[0]
            
            data = m.get_all_data(submodel)
            sampling_prob = mi.interaction_dataset['__sampling_probability'] \
              if '__sampling_probability' in mi.interaction_dataset.get_known_attribute_names() \
              else None
            model_data.append({'data':data, 
                               'model_name':model_name,
                               'sampling_probability': sampling_prob,
                               'choice_type':options.choice_type[h][i]
                              })
            
            if options.market_share[h][i]:
                ms_expression = options.market_share[h][i]
                ms_variablename = VariableName(ms_expression)
        
                dataset_name = ms_variablename.get_dataset_name()
                dataset_pool=model_system.run_year_namespace["dataset_pool"]
                from numpy import zeros
                ## handle district_traffic_flow as a special case
                if dataset_name == 'district_traffic_flow':
                    id_name = 'district_id'  #fake id_name
                    ds = dataset_pool.get_dataset('district_traffic_flow')
                    ms = zeros( (ds['from_district_id'].max()+1, ds['to_district_id'].max()+1), 
                                dtype=ds['share'].dtype)
                    ms[ds['from_district_id'], ds['to_district_id']] = ds['share']
                else:
                    ds = model_system.run_year_namespace[dataset_name] \
                       or model_system.run_year_namespace['datasets'][dataset_name]
                    id_name = ds.get_id_name()[0]
                    ds.compute_variables([ms_variablename], dataset_pool=dataset_pool)
                    ms = ds.get_multiple_attributes([id_name, ms_variablename.get_alias()])
                
                market_ids = m.choice_set.compute_one_variable_with_unknown_package( id_name, dataset_pool=dataset_pool)
                market_ids_2d = market_ids[m.model_interaction.get_choice_index()]
                model_data[i].update({'market_id':market_ids_2d, 'market_share':ms})
                            
            logger.end_block()

        population_data.append(model_data)
    
    ## pickle file   
    pickle_file = open(options.pickle_filename, 'w+b')
    cPickle.dump({'training_data': training_data,
                  'population_data': population_data,
                  'choice_type': options.choice_type
                 }, file=pickle_file)
    pickle_file.close()
