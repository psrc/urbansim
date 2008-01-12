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

from opus_core.misc import get_string_or_None
from opus_core.configuration import Configuration


class DistributeUnplacedJobsModelConfigurationCreator(object):
    _model_name = 'distribute_unplaced_jobs_model'
    
    def __init__(self,
                debuglevel = 'debuglevel',
                agent_set = 'job',
                location_set = 'gridcell',
                agents_filter = None,
                filter = None):
        self.debuglevel = debuglevel
        self.agent_set = agent_set
        self.location_set = location_set
        self.agents_filter = agents_filter
        self.filter = filter
    
    def execute(self):        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'DistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel,
                              'filter': get_string_or_None(self.filter),
                              'dataset_pool': 'dataset_pool'},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'data_objects': 'datasets',
                    'location_set': self.location_set,
                    'agents_filter': get_string_or_None(self.agents_filter),
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
                'arguments': {'debuglevel': 'debuglevel',
                              'filter': None,
                              'dataset_pool': 'dataset_pool'},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'data_objects': 'datasets',
                    'location_set': 'gridcell',
                    'agents_filter': None
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
            agents_filter='job.sector_id==10'
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999,
                              'filter': None,
                              'dataset_pool': 'dataset_pool'},
                'name': 'DistributeUnplacedJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'data_objects': 'datasets',
                    'location_set': 'location_set',
                    'agents_filter': "'job.sector_id==10'"
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()