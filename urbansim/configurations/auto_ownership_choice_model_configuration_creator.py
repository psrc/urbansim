# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration


class AutoOwnershipChoiceModelConfigurationCreator(object):
    _model_name = 'auto_ownership_choice_model'        
        
    def __init__(self,        
                 debuglevel = 0,
                 agent_set = 'household',
                 records_per_chunk = 500,
                 estimation_procedure = 'opus_core.bhhh_mnl_estimation',
                 choice_attribute_name = 'cars',
                 choice_set = [0, 1, 2, 3],
                 coefficients_table = 'auto_ownership_choice_model_coefficients',
                 specification_table = 'auto_ownership_choice_model_specification'):
        
        self.debuglevel = debuglevel
        self.agent_set = agent_set
        self.records_per_chunk = records_per_chunk
        self.estimation_procedure = estimation_procedure
        self.choice_attribute_name = choice_attribute_name
        self.choice_set = choice_set
        
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'procedure': "'%s'" % self.estimation_procedure,
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.%s' % self._model_name: 'AutoOwnershipChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'%s'" % self.choice_attribute_name,
                    'choice_set': list(self.choice_set),
                    },
                'name': 'AutoOwnershipChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s)' % _specification
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


class TestAutoOwnershipChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
            
    def test_defaults(self):
        creator = AutoOwnershipChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'data_objects': 'datasets',
                    'debuglevel': 0,
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.auto_ownership_choice_model': 'AutoOwnershipChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'cars'",
                    # Hack to get around Traits returning non-list objects for Trait Lists:
                    'choice_set': [0, 1, 2, 3], 
                    },
                'name': 'AutoOwnershipChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'auto_ownership_choice_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'auto_ownership_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'auto_ownership_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
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
        creator = AutoOwnershipChoiceModelConfigurationCreator(
            debuglevel = 9999,
            agent_set = 'agent_set',
            records_per_chunk = 8888,
            estimation_procedure = 'package.procedure',
            choice_attribute_name = 'choice_attribute_name',
            choice_set = [7,7,7,7],
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'data_objects': 'datasets',
                    'debuglevel': 9999,
                    'procedure': "'package.procedure'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.auto_ownership_choice_model': 'AutoOwnershipChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_attribute_name': "'choice_attribute_name'",
                    # Hack to get around Traits returning non-list objects for Trait Lists:
                    'choice_set': [7,7,7,7],
                    },
                'name': 'AutoOwnershipChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification)'
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