# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None
from opus_core.resources import Resources

class HouseholdLocationChoiceModelConfigurationCreator(object):
    _model_name = 'household_location_choice_model'

    def __init__(self,
                agent_set = 'household',
                debuglevel = 'debuglevel',
                coefficients_table = 'household_location_choice_model_coefficients',
                specification_table = 'household_location_choice_model_specification',
                location_set = 'gridcell',
                location_id_name = None,
                location_filter = None, # filter variable for locations to be chosen into the set of alternatives
                submodel_string = None, # agent's attribute determining sub-models
                sampler = 'opus_core.samplers.weighted_sampler', # module for sampling alternatives
                choices = 'urbansim.lottery_choices', # module for making choices
                capacity_string = 'vacant_residential_units', # attribute of location set that determines capacity and weights for sampling in simulation
                estimation_weight_string = 'residential_units', # attribute of location set that determines weights for sampling in estimation
                simulation_weight_string = None, # if this is None, weights are proportional to the capacity 
                sample_size_locations = 30, # how many locations should be sampled into the set of alternatives
                portion_to_unplace = 1/12.0, # portion of households to be unplaced before estimation
                nchunks = 12, # in how many chunks should the simulation run
                records_per_chunk = None, # how many records should be in 1 chunk (if not None, it has priority over 'nchunks')
                agents_for_estimation_table_name = 'households_for_estimation',
                number_of_units_string = 'residential_units', # attribute of location set that determines total number of units
                number_of_agents_string = 'number_of_households', # attribute of location set that determines number of households in each unit
                lottery_max_iterations = 3, # parameter for 'urbansim.lottery_choices' module - how many times households can re-decide for a location if the capacity is exceeded 
                maximum_runs = 3, # maximum number of iterations of the outer loop that compares values of 'number_of_units_string' with values of 'number_of_agents_string'
                estimation_procedure = 'opus_core.bhhh_mnl_estimation',
                estimation_size_agents = None, # Portion of households for estimation to be used for estimation (should be > 0 and <= 1)
                agent_filter_for_estimation = None, # filter variable for agents to be used for estimation
                variable_package = 'urbansim', # in what package are the variables above defined 
                run_config = {}, # additional arguments passed to simulation modules
                estimate_config = {}, # additional arguments passed to estimation modules
                join_agents_for_estimation_with_all_agents = True, # should the dataset of households for estimation be (internally) attached to the houeholds dataset.
                                                                    # If it is False, it is expected, that households for estimation are contained in the households table (the same household_id)
                unplace_agents_for_estimation = True, # should households for estimation be unplaced before estimation  (after capturing their locations for the estimation procedure)
                input_index = 'hrm_index' # internal connector between the household relocation model and HLCM
                ):
        self.agent_set = agent_set
        self.debuglevel = debuglevel
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        self.location_set = location_set
        self.location_id_name = location_id_name
        self.submodel_string = submodel_string
        self.sampler = sampler
        self.choices = choices
        self.capacity_string = capacity_string
        self.estimation_weight_string = estimation_weight_string
        self.simulation_weight_string = simulation_weight_string
        self.sample_size_locations = sample_size_locations
        self.portion_to_unplace = portion_to_unplace
        self.agents_for_estimation_table_name = agents_for_estimation_table_name
        self.number_of_units_string = number_of_units_string
        self.number_of_agents_string = number_of_agents_string
        self.lottery_max_iterations = lottery_max_iterations
        self.maximum_runs = maximum_runs
        self.estimation_procedure = estimation_procedure
        self.estimation_size_agents = estimation_size_agents
        self.variable_package = variable_package
        self.input_index = input_index
        self.location_filter = location_filter
        self.agent_filter_for_estimation = agent_filter_for_estimation
        self.join_agents_for_estimation_with_all_agents = join_agents_for_estimation_with_all_agents
        if unplace_agents_for_estimation:
            self.index_to_unplace = self.input_index
        else:
            self.index_to_unplace = None
        if records_per_chunk is not None:
            self.chunk_specification = "{'records_per_chunk':%s}" % records_per_chunk
        else:
            self.chunk_specification = "{'nchunks':%s}" % nchunks

        self.run_config = "Resources({'lottery_max_iterations': %s, " % self.lottery_max_iterations
        for key, value in run_config.iteritems():
            self.run_config += "'%s': %s," % (key, value)
        self.run_config += '})'
        
        self.estimate_config = 'Resources({'
        for key, value in estimate_config.iteritems():
            self.estimate_config += "'%s': %s," % (key, value)
        self.estimate_config += '})'
        
    def execute(self):
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'index'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': _index,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.%s' % self._model_name: 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': get_string_or_None(self.sampler),
                    'choices': "'%s'" % self.choices,
                    'estimation': "'%s'" % self.estimation_procedure,
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    'capacity_string': get_string_or_None(self.capacity_string),
                    'estimation_weight_string': get_string_or_None(self.estimation_weight_string),
                    'simulation_weight_string': get_string_or_None(self.simulation_weight_string),
                    'number_of_units_string': get_string_or_None(self.number_of_units_string),
                    'number_of_agents_string': get_string_or_None(self.number_of_agents_string),
                    'location_id_string': get_string_or_None(self.location_id_name),
                    'submodel_string': get_string_or_None(self.submodel_string),
                    'estimation_size_agents': self.estimation_size_agents,
                    'filter': get_string_or_None(self.location_filter),
                    'run_config': self.run_config,
                    'estimate_config': self.estimate_config,
                    "variable_package": "'%s'" % self.variable_package
                    },
                'name': 'HouseholdLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'%s'" % self.agents_for_estimation_table_name,
                    'data_objects': 'datasets',
                    'index_to_unplace': self.index_to_unplace,
                    'join_datasets': '%s' % self.join_agents_for_estimation_with_all_agents,
                    'portion_to_unplace': self.portion_to_unplace,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    'filter': get_string_or_None(self.agent_filter_for_estimation)
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _index)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients)
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': self.input_index,
                    'chunk_specification': self.chunk_specification,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    'maximum_runs': self.maximum_runs
                    }
                }
            })


from opus_core.tests import opus_unittest 


class TestHouseholdLocationChoiceModelConfiguration(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HouseholdLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.household_location_choice_model': 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'estimation': "'opus_core.bhhh_mnl_estimation'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_residential_units'",
                    'estimation_weight_string': "'residential_units'",
                    'simulation_weight_string': None,
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'location_id_string': None,
                    'submodel_string': None,
                    'estimation_size_agents': None,
                    'filter': None,
                    'run_config': "Resources({'lottery_max_iterations': 3, })",
                    'estimate_config': "Resources({})",
                    'variable_package': "'urbansim'"
                    },
                'name': 'HouseholdLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'households_for_estimation'",
                    'data_objects': 'datasets',
                    'index_to_unplace': 'hrm_index',
                    'join_datasets': 'True',
                    'portion_to_unplace': 1/12.0,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'",
                    'filter': None
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'household_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'hrm_index',
                    'chunk_specification': "{'nchunks':12}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification',
                    'maximum_runs': 3
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = HouseholdLocationChoiceModelConfigurationCreator(
            agent_set = 'agent_set',
            debuglevel = 999,
            sampler = None,
            choices = 'package.choices',
            estimation_procedure = 'opus_core.my_estimation_procedure',
            location_set = 'location_set',
            sample_size_locations = 2000,
            portion_to_unplace = 888.8,
            nchunks = 12345,
            agents_for_estimation_table_name = 'agents_for_estimation_table_name',
            lottery_max_iterations = 20,
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            input_index = 'input_index',
            maximum_runs=10,
            location_id_name='building_id',
            estimation_size_agents = 0.5,
            run_config = {'aaaa': "'bbbb'"},
            estimate_config = {'xx': 45}
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 999,
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.household_location_choice_model': 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': None, 
                    'choices': "'package.choices'",
                    'estimation': "'opus_core.my_estimation_procedure'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'sample_size_locations': 2000,
                    'capacity_string': "'vacant_residential_units'",
                    'estimation_weight_string': "'residential_units'",
                    'simulation_weight_string': None,
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'location_id_string': "'building_id'",
                    'submodel_string': None,
                    'estimation_size_agents': 0.5,
                    'filter': None,
                    'run_config': "Resources({'lottery_max_iterations': 20, 'aaaa': 'bbbb',})",
                    'estimate_config': "Resources({'xx': 45,})",
                    'variable_package': "'urbansim'"
                    },
                'name': 'HouseholdLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'agents_for_estimation_table_name'", ###
                    'data_objects': 'datasets',
                    'index_to_unplace': 'input_index', 
                    'join_datasets': 'True',
                    'portion_to_unplace': 888.8,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
                    'filter': None
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'coefficients_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'input_index',
                    'chunk_specification': "{'nchunks':12345}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 999,
                    'specification': 'specification',
                    'maximum_runs': 10
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()