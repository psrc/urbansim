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

from opus_core.configuration import Configuration


class DevelopmentProjectTransitionModelConfigurationCreator(object):
    
    _model_name = 'development_project_transition_model'
    
    def __init__(self,
            debuglevel = 4,
            location_set = 'gridcell',
            history_table = 'development_event_history',
            vacancy_table = 'target_vacancy',
            output_results = 'dptm_results',
            vacancy_variables = None):
        self.debuglevel = debuglevel
        self.location_set = location_set
        self.history_table = history_table
        self.vacancy_table = vacancy_table
        self.output_results = output_results
        self.run_config = None
        if vacancy_variables is not None:
            self.run_config = "{"
            for key, value in vacancy_variables.iteritems():
                self.run_config += "'%s_vacant_variable': '%s'," % (key, value)
            self.run_config += "}"
        
    def execute(self):        
        return Configuration({
            'import': {
                'urbansim.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': self.history_table,
                    'location_set': self.location_set,
                    'model_configuration': 'model_configuration',
                    'resources': 'model_resources',
                    'vacancy_table': self.vacancy_table,
                    'year': 'year',
                    'resources': self.run_config
                    },
                'output': self.output_results,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDevelopmentProjectTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentProjectTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 4},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': 'development_event_history',
                    'location_set': 'gridcell',
                    'model_configuration': 'model_configuration',
                    'resources': 'model_resources',
                    'vacancy_table': 'target_vacancy',
                    'year': 'year',
                    'resources': None
                    },
                'output': 'dptm_results'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentProjectTransitionModelConfigurationCreator(
            debuglevel = 9999,
            location_set = 'location_set',
            history_table = 'history_table',
            vacancy_table = 'vacancy_table',
            output_results = 'output_results',
            vacancy_variables = {'commercial': 'gridcell.my_commercial_vacant_var',
                                'industrial': 'gridcell.my_industrial_vacant_var'}
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': 'history_table',
                    'location_set': 'location_set',
                    'model_configuration': 'model_configuration',
                    'resources': 'model_resources',
                    'vacancy_table': 'vacancy_table',
                    'year': 'year',
                    'resources': "{'industrial_vacant_variable': 'gridcell.my_industrial_vacant_var','commercial_vacant_variable': 'gridcell.my_commercial_vacant_var',}"
                    },
                'output': 'output_results'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()