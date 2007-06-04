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

from numpy import array

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait

from opus_core.configuration import Configuration


class DevelopmentEventTransitionModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    
    input_projects = Str('dptm_results')
    output_events = Str('development_events')
    
    _model_name = 'development_event_transition_model'
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _types = 'all_project_types'
        _units = 'all_project_units'
        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': self.input_projects,
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_types, _units)
                },
            'run': {
                'arguments': {
                    'debuglevel': self.debuglevel,
                    'projects': self.input_projects,
                    'types': _types,
                    'units': _units,
                    'year': 'year'
                    },
                'output': self.output_events,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDevelopmentEventTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentEventTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': 'dptm_results',
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(all_project_types, all_project_units)'
                },
            'run': {
                'arguments': {
                    'debuglevel': 'debuglevel',
                    'projects': 'dptm_results',
                    'types': 'all_project_types',
                    'units': 'all_project_units',
                    'year': 'year'
                    },
                'output': 'development_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentEventTransitionModelConfigurationCreator(
            debuglevel = 9999,
            output_events = 'output_events',
            input_projects = 'input_projects',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': 'input_projects',
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(all_project_types, all_project_units)'
                },
            'run': {
                'arguments': {
                    'debuglevel': 9999,
                    'projects': 'input_projects',
                    'types': 'all_project_types',
                    'units': 'all_project_units',
                    'year': 'year'
                    },
                'output': 'output_events',
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()