# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class EmploymentTransitionModelConfigurationCreator(object):    
    _model_name = 'employment_transition_model'
    
    def __init__(self,
                debuglevel = 'debuglevel',
                job_set = 'job',
                job_building_types = 'job_building_type',
                location_id_name = 'grid_id'):
        self.debuglevel = debuglevel
        self.job_set = job_set
        self.job_building_types = job_building_types
        self.location_id_name = location_id_name
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _control_totals = 'control_totals'
        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'EmploymentTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel,
                              'location_id_name': "'%s'" % self.location_id_name,
                              },
                'name': 'EmploymentTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': _control_totals,
                },
            'run': {
                'arguments': {
                    'control_totals': _control_totals,
                    'job_building_types': self.job_building_types,
                    'job_set': self.job_set,
                    'year': 'year'
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestEmploymentTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = EmploymentTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.employment_transition_model': 'EmploymentTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel', 'location_id_name': "'grid_id'"},
                'name': 'EmploymentTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': 'control_totals'
                },
            'run': {
                'arguments': {
                    'control_totals': 'control_totals',
                    'job_building_types': 'job_building_type',
                    'job_set': 'job',
                    'year': 'year'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = EmploymentTransitionModelConfigurationCreator(
            debuglevel = 9999,
            job_set = 'job_set',
            job_building_types = 'job_building_types',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.employment_transition_model': 'EmploymentTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999, 'location_id_name': "'grid_id'"},
                'name': 'EmploymentTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': 'control_totals'
                },
            'run': {
                'arguments': {
                    'control_totals': 'control_totals',
                    'job_building_types': 'job_building_types',
                    'job_set': 'job_set',
                    'year': 'year'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()