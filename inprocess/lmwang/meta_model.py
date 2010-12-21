# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
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
from numpy.random import randint
from numpy import where
import cPickle

class options(object):
    meta_models = [['large_area_choice_model', 'residential_building_type_choice_model', 'auto_ownership_choice_model'],
                   ['household_location_choice_model']
                   ]
    market_share = [['market_share=large_area.aggregate(building.residential_units)',
                     'market_share=building_type.aggregate(building.residential_units)',
                     'market_share=car.number_of_agents(household)'
                     ],
                     ['']
                    ]
    #CLASSIFICATION = 1
    #RATING = 2
    #REGRESSION = 3
    choice_type = [['CLASSIFICATION', 'CLASSIFICATION', 'CLASSIFICATION'], ['CLASSIFICATION']]
    xml_configuration = '/workspace/opus/project_configs/psrc_parcel_test.xml'
    scenario_name = 'psrc_baseline_test'
    year = 2000
    agent_set = 'household'
    sample_size = 5000 #for regularization
    agents_index = None
    pickle_filename = 'em_data.pickle'
    seed = None
    nchunks = 1 ##TODO

if __name__ == '__main__':
    xmlconfig = XMLConfiguration(options.xml_configuration)
    ## training data (start_estimation)
    training_data = []
    for h, hierarchy in enumerate(options.meta_models):
        model_data = []
        for i, model_name in enumerate(hierarchy):
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
            agents_size = estimator.get_agent_set().size()
            m = estimator.get_model()
            model_system = estimator.model_system
            
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
            
            variable_names = m.model_interaction.get_variable_names(submodel)
            outputvar = model_system.run_year_namespace['outputvar']
            results_name = outputvar.strip('()').split(',')[1].strip()
            estimation_results = model_system.run_year_namespace[results_name]
            
            model_data.append({"data":data, 
                               'index_chosen':index_chosen,
                               'variable_names':variable_names,
                               'estimation_results':estimation_results,
                               'model_name':model_name,
                               'choice_type':options.choice_type[h][i]
                               })

            if options.market_share[h][i]:
                ms_expression = options.market_share[h][i]
                ms_variablename = VariableName(ms_expression)
        
                dataset_name = ms_variablename.get_dataset_name()
                dataset_pool=model_system.run_year_namespace["dataset_pool"]
                ds = model_system.run_year_namespace[dataset_name] or model_system.run_year_namespace['datasets'][dataset_name]
                id_name = ds.get_id_name()[0]
                ds.compute_variables([ms_variablename], dataset_pool=dataset_pool)
                ms = ds.get_multiple_attributes([id_name, ms_variablename.get_alias()])
                
                market_ids = m.choice_set.compute_one_variable_with_unknown_package( id_name, dataset_pool=dataset_pool)
                market_ids_2d = market_ids[m.model_interaction.get_choice_index()]
                model_data[i].update({'market_id':market_ids_2d, 'market_share':ms})

        training_data.append(model_data)
        
    config = xmlconfig.get_run_configuration(options.scenario_name)
    if not options.agents_index:            
        options.agents_index = randint(0, agents_size, size=options.sample_size).tolist()

    ## regularization data
    population_data = []
    for h, hierarchy in enumerate(options.meta_models):
        model_data = []
        for i, model_name in enumerate(hierarchy):
            
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
            submodels = m.model_interaction.get_submodels()
            assert len(submodels) == 1
            submodel = submodels[0]
            
            data = m.get_all_data(submodel)
            model_data.append({'data':data, 
                               'model_name':model_name,
                               'choice_type':options.choice_type[h][i]
                              })
            
            if options.market_share[h][i]:
                ms_expression = options.market_share[h][i]
                ms_variablename = VariableName(ms_expression)
        
                dataset_name = ms_variablename.get_dataset_name()
                dataset_pool=model_system.run_year_namespace["dataset_pool"]
                ds = model_system.run_year_namespace[dataset_name] or model_system.run_year_namespace['datasets'][dataset_name]
                id_name = ds.get_id_name()[0]
                ds.compute_variables([ms_variablename], dataset_pool=dataset_pool)
                ms = ds.get_multiple_attributes([id_name, ms_variablename.get_alias()])
                
                market_ids = m.choice_set.compute_one_variable_with_unknown_package( id_name, dataset_pool=dataset_pool)
                market_ids_2d = market_ids[m.model_interaction.get_choice_index()]
                model_data[i].update({'market_id':market_ids_2d, 'market_share':ms})
                            
        population_data.append(model_data)
    
    ## pickle file   
    pickle_file = open(options.pickle_filename, 'w+b')
    cPickle.dump({'training_data': training_data,
                  'population_data': population_data,
                  'choice_type': options.choice_type
                 }, file=pickle_file)
    pickle_file.close()
