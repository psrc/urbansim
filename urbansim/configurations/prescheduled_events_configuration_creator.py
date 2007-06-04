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


class PrescheduledEventsConfigurationCreator(HasStrictTraits):
    _model_name = 'prescheduled_events'
    
    output_events = Str('development_events')
    
    def execute(self):
        return Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': self.output_events,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestPrescheduledEventsConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = PrescheduledEventsConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': 'development_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = PrescheduledEventsConfigurationCreator(
            output_events = 'output_events',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': 'output_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()