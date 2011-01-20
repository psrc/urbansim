# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from urbansim.configurations.distribute_unplaced_jobs_model_configuration_creator import DistributeUnplacedJobsModelConfigurationCreator

class RegionalDistributeUnplacedJobsModelConfigurationCreator(DistributeUnplacedJobsModelConfigurationCreator):

    _model_name = 'regional_distribute_unplaced_jobs_model'
    
    def execute(self):
        conf = DistributeUnplacedJobsModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalDistributeUnplacedJobsModel'}
        conf['init']['name'] = 'RegionalDistributeUnplacedJobsModel'
        return conf

from opus_core.tests import opus_unittest 


class TestDistributeUnplacedJobsModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalDistributeUnplacedJobsModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_distribute_unplaced_jobs_model': 'RegionalDistributeUnplacedJobsModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'dataset_pool': 'dataset_pool',
                              'filter':None},
                'name': 'RegionalDistributeUnplacedJobsModel',
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'data_objects': 'datasets',
                    'location_set': 'gridcell',
                    'agents_filter':None
                    }
                },
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
            
if __name__ == '__main__':
    opus_unittest.main()