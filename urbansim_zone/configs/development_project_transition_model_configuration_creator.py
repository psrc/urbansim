# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array

from opus_core.configuration import Configuration


class DevelopmentProjectTransitionModelConfigurationCreator(object):
    
    _model_name = 'development_project_transition_model'
    
    def __init__(self,
            debuglevel = 'debuglevel',
            location_set = 'zone',
            history_table = 'development_event_history',
            vacancy_table = 'target_vacancy',
            output_results = 'dptm_results',
            vacancy_variables = None,
            total_units_variables = None):
        """vacancy_variables is a dictionary with keys equal to the project types and values equal to 
        the variable names that determine vacancies. If not given, default values are set by the model.
        total_units_variables is a dictionary with keys equal to the project types and values equal to 
        the variable names that determine total number of existing units. If not given, default values are set by the model.
        """
        self.debuglevel = debuglevel
        self.location_set = location_set
        self.history_table = history_table
        self.vacancy_table = vacancy_table
        self.output_results = output_results
        self.run_config = None
        if (vacancy_variables is not None) or (total_units_variables is not None):
            self.run_config = "{"
            if vacancy_variables is not None:
                for key, value in vacancy_variables.iteritems():
                    self.run_config += "'%s_vacant_variable': '%s'," % (key, value)
            if total_units_variables is not None:
                for key, value in total_units_variables.iteritems():
                    self.run_config += "'%s_total_units_variable': '%s'," % (key, value)
            self.run_config += "}"
        
    def execute(self):        
        return Configuration({
            'import': {
                'urbansim_zone.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': self.history_table,
                    'location_set': self.location_set,
                    'vacancy_table': self.vacancy_table,
                    'year': 'year',
                    'dataset_pool': 'dataset_pool',
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
                'urbansim_zone.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': 'development_event_history',
                    'location_set': 'zone',
                    'vacancy_table': 'target_vacancy',
                    'year': 'year',
                    'dataset_pool': 'dataset_pool',
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
            vacancy_variables = {'commercial': 'zone.my_commercial_vacant_var',
                                'industrial': 'zone.my_industrial_vacant_var'}
            )
        
        expected = Configuration({
            'import': {
                'urbansim_zone.models.development_project_transition_model': 'DevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'DevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': 'history_table',
                    'location_set': 'location_set',
                    'vacancy_table': 'vacancy_table',
                    'year': 'year',
                    'dataset_pool': 'dataset_pool', 
                    'resources': "{'industrial_vacant_variable': 'zone.my_industrial_vacant_var','commercial_vacant_variable': 'zone.my_commercial_vacant_var',}"
                    },
                'output': 'output_results'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()
