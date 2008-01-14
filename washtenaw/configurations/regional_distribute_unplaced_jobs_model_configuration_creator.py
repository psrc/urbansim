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