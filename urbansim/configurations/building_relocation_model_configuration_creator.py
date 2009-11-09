# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class BuildingRelocationModelConfigurationCreator(object):
    
    _model_name = 'agent_relocation_model'
    
    def __init__(self,
                agent_set = 'building',
                location_id_name = 'gridcell.get_id_name()[0]',
                output_index = 'brm_index'):
        self.agent_set = agent_set
        self.location_id_name = location_id_name
        self.output_index = output_index
        
    def execute(self):
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'AgentRelocationModel'
                },
            'init': {
                'arguments': {
                    'location_id_name': self.location_id_name,
                    },
                'name': 'AgentRelocationModel'
                },
            'run': {
                'arguments': {'agent_set': self.agent_set},
                'output': self.output_index,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestBuildingRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = BuildingRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.agent_relocation_model': 'AgentRelocationModel'
                },
            'init': {
                'arguments': {
                    'location_id_name': 'gridcell.get_id_name()[0]',
                    },
                'name': 'AgentRelocationModel'
                },
            'run': {
                'arguments': {'agent_set': 'building'},
                'output': 'brm_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = BuildingRelocationModelConfigurationCreator(
            agent_set = 'agent_set',
            location_id_name = 'location_id_name',
            output_index = 'output_index',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.agent_relocation_model': 'AgentRelocationModel'
                },
            'init': {
                'arguments': {
                    'location_id_name': 'location_id_name',
                    },
                'name': 'AgentRelocationModel'
                },
            'run': {
                'arguments': {'agent_set': 'agent_set'},
                'output': 'output_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()