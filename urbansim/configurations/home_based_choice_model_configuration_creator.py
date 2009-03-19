# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration


class HomeBasedChoiceModelConfigurationCreator(object):
    _model_name = 'home_based_choice_model'

    def __init__(self,
                agent_set = 'person',
                debuglevel = 0,
                coefficients_table = 'home_based_choice_model_coefficients',
                specification_table = 'home_based_choice_model_specification',
                records_per_chunk = 500,
                agents_for_estimation_table = 'persons_for_estimation',
                estimation_procedure = 'opus_core.bhhh_mnl_estimation',
                choice_attribute_name = 'work_nonhome_based',
                choice_set = [0, 1],
                filter = 'None'):
        self.agent_set = agent_set
        self.debuglevel = debuglevel
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        self.records_per_chunk = records_per_chunk
        self.agents_for_estimation_table = agents_for_estimation_table
        self.estimation_procedure = estimation_procedure
        self.choice_attribute_name = choice_attribute_name
        self.choice_set = choice_set
        self.filter = filter
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'agents_index'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': _index,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'procedure': "'%s'" % self.estimation_procedure,
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.%s' % self._model_name: 'HomeBasedChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'%s'" % self.choice_attribute_name,
                    'choice_set': list(self.choice_set),
                    },
                'name': 'HomeBasedChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'%s'" % self.agents_for_estimation_table,
                    'filter': self.filter,
                    'join_datasets': 'True',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
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
                    'chunk_specification': "{'records_per_chunk':%s}" % self.records_per_chunk,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'specification': _specification,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestHomeBasedChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HomeBasedChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_index': 'agents_index',
                    'data_objects': 'datasets',
                    'debuglevel': 0,
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.home_based_choice_model': 'HomeBasedChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'work_nonhome_based'",
                    # Hack to get around Traits returning non-list objects for Trait Lists:
                    'choice_set': [0, 1],
                    },
                'name': 'HomeBasedChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'persons_for_estimation'",
                    'filter': 'None',
                    'join_datasets': 'True',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'home_based_choice_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, agents_index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'home_based_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'home_based_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'person',
                    'chunk_specification': "{'records_per_chunk':500}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = HomeBasedChoiceModelConfigurationCreator(
            debuglevel = 9999,
            records_per_chunk = 8888,
            agent_set = 'agent_set',
            estimation_procedure = 'package.estimation_procedure',
            choice_attribute_name = 'choice_attribute_name',
            choice_set = [9, 9],
            agents_for_estimation_table = 'agents_for_estimation_table',
            filter = 'filter',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            )
            
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'agents_index',
                    'data_objects': 'datasets',
                    'debuglevel': 9999,
                    'procedure': "'package.estimation_procedure'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.home_based_choice_model': 'HomeBasedChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'choice_attribute_name'",
                    # Hack to get around Traits returning non-list objects for Trait Lists:
                    'choice_set': [9, 9],
                    },
                'name': 'HomeBasedChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'agents_for_estimation_table'",
                    'filter': 'filter',
                    'join_datasets': 'True',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, agents_index)'
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
                    'chunk_specification': "{'records_per_chunk':8888}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()