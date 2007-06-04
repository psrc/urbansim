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


class EmploymentTransitionModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    job_set = Str('job')
    job_building_types = Str('job_building_type')
    
    _model_name = 'employment_transition_model'
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _control_totals = 'control_totals'
        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'EmploymentTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
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
                'arguments': {'debuglevel': 'debuglevel'},
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
                'arguments': {'debuglevel': 9999},
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