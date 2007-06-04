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

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait

from opus_core.configuration import Configuration


class GovernmentalEmploymentLocationChoiceModelConfigurationCreator(HasStrictTraits):
    agent_set = Str('job')
    location_set = Str('gridcell')
    debuglevel = Trait('debuglevel', Str, Int)
    
    input_index = Str('erm_index')
    
    _model_name = 'home_based_employment_location_choice_model'
    
    def execute(self):        
        return Configuration({
            'import': {'urbansim.models.scaling_jobs_model': 'ScalingJobsModel'},
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'ScalingJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': self.input_index,
                    'data_objects': 'datasets',
                    'location_set': self.location_set,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestGovernmentalEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = GovernmentalEmploymentLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'import': {'urbansim.models.scaling_jobs_model': 'ScalingJobsModel'},
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'ScalingJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'erm_index',
                    'data_objects': 'datasets',
                    'location_set': 'gridcell',
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = GovernmentalEmploymentLocationChoiceModelConfigurationCreator(
            agent_set = 'agent_set',
            location_set = 'location_set',
            debuglevel = 9999,
            input_index = 'input_index',
            )
        
        expected = Configuration({
            'import': {'urbansim.models.scaling_jobs_model': 'ScalingJobsModel'},
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'ScalingJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'input_index',
                    'data_objects': 'datasets',
                    'location_set': 'location_set',
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()