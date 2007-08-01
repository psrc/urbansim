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

from enthought.traits.api import HasStrictTraits, Str

from opus_core.configuration import Configuration


class DeletionEventModelConfigurationCreator(HasStrictTraits):
    location_set = Str('gridcell')
    deletion_event_set = Str('deletion_event')
    
    _model_name = 'deletion_event_model'
    
    def execute(self):        
        return Configuration({
            'import': {
                'washtenaw.models.%s' % self._model_name: 'DeletionEventModel'
                },
            'init': {'name': 'DeletionEventModel'},
            'run': {
                'arguments': {
                    'location_set': self.location_set,
                    'deletion_event_set': self.deletion_event_set,
                    'current_year': 'year',
                    'dataset_pool': 'dataset_pool'
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDeletionEventModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DeletionEventModelConfigurationCreator()
        
        expected = Configuration({
           'import': {
                'washtenaw.models.deletion_event_model': 'DeletionEventModel'
                },
            'init': {'name': 'DeletionEventModel'},
            'run': {
                'arguments': {
                    'location_set': 'gridcell',
                    'deletion_event_set': 'deletion_event',
                    'current_year': 'year',
                    'dataset_pool': 'dataset_pool'
                    }
                }
            })
        result = creator.execute()
        self.assertDictsEqual(result, expected)           
            
if __name__ == '__main__':
    opus_unittest.main()