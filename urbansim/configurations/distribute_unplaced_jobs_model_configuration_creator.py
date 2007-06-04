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


class DistributeUnplacedJobsModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    agent_set = Str('job')
    location_set = Str('gridcell')
    
    _model_name = 'distribute_unplaced_jobs_model'
    
    def execute(self):        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'DistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'data_objects': 'datasets',
                    'location_set': self.location_set,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDistributeUnplacedJobsModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DistributeUnplacedJobsModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'data_objects': 'datasets',
                    'location_set': 'gridcell'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DistributeUnplacedJobsModelConfigurationCreator(
            debuglevel = 9999,
            agent_set = 'agent_set',
            location_set = 'location_set',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'data_objects': 'datasets',
                    'location_set': 'location_set'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()