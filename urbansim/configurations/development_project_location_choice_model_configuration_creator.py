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
from opus_core.misc import get_string_or_None

class DevelopmentProjectLocationChoiceModelConfigurationCreator(HasStrictTraits):
    # Set in constructor
    project_type = Str()
    coefficients_table = Str()
    specification_table = Str()
    
    input_agent_set = Str()

    _model_name = None
    
    # Default values
    records_per_chunk = Int(300)
    debuglevel = Trait('debuglevel', Str, Int)
    location_set = Str('gridcell')
    events_for_estimation_table = Str('development_event_history')
    submodel_string = Trait('size_category', None, Str)

    def __init__(self, project_type, *args, **kwargs):
        """Construct attributes that depend upon project_type's value"""        
        # Hack around HasStrictTraits's restriction against assignment to non-Traits attributes
        self.__dict__['_model_name'] = '%s_development_location_choice_model' % project_type
        
        # Set defaults, which may be overridden by the kwarg values.
        self.input_agent_set = "dptm_results['%s']" % project_type
        self.coefficients_table = '%s_coefficients' % self._model_name
        self.specification_table = '%s_specification' % self._model_name
        
        # Let HasStrictTraits handle the assignment, etc. of the named arguments, above
        # kwargs['project_type'] = project_type # doesn't work for some users
        self.project_type = project_type
        
        HasStrictTraits.__init__(self, *args, **kwargs)
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _projects = 'projects'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': _projects,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                'urbansim.models.development_project_location_choice_model_creator': 'DevelopmentProjectLocationChoiceModelCreator'
                },
            'init': {
                'arguments': {
                    'location_set': self.location_set,
                    'model_configuration': "model_configuration['development_project_types']['%s']" % self.project_type,
                    'project_type': "'%s'" % self.project_type,
                    'submodel_string': get_string_or_None(self.submodel_string),
                    },
                'name': 'DevelopmentProjectLocationChoiceModelCreator().get_model'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'base_year': "resources['base_year']",
                    'categories': "model_configuration['development_project_types']['%s']['categories']" % self.project_type,
                    'events_for_estimation_storage': 'base_cache_storage',
                    'events_for_estimation_table': "'%s'" % self.events_for_estimation_table,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _projects)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table, 
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients)
                },
            'run': {
                'arguments': {
                    'agent_set': self.input_agent_set,
                    'chunk_specification': "{'records_per_chunk':%s}" % self.records_per_chunk,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification
                    }
                }
            })


from opus_core.tests import opus_unittest 


class TestDevelopmentProjectLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentProjectLocationChoiceModelConfigurationCreator(
            project_type = 'project_type',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'projects',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.development_project_location_choice_model_creator': 'DevelopmentProjectLocationChoiceModelCreator'
                },
            'init': {
                'arguments': {
                    'location_set': 'gridcell',
                    'model_configuration': "model_configuration['development_project_types']['project_type']",
                    'project_type': "'project_type'",
                    'submodel_string': "'size_category'"
                    },
                'name': 'DevelopmentProjectLocationChoiceModelCreator().get_model'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'base_year': "resources['base_year']",
                    'categories': "model_configuration['development_project_types']['project_type']['categories']",
                    'events_for_estimation_storage': 'base_cache_storage',
                    'events_for_estimation_table': "'development_event_history'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, projects)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'project_type_development_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': "dptm_results['project_type']",
                    'chunk_specification': "{'records_per_chunk':300}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentProjectLocationChoiceModelConfigurationCreator(
            project_type = 'project_type',
            input_agent_set = 'input_agent_set',
            records_per_chunk = 9999,
            debuglevel = 7777,
            location_set = 'location_set',
            events_for_estimation_table = 'events_for_estimation_table',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            submodel_string = None
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'projects',
                    'data_objects': 'datasets',
                    'debuglevel': 7777,
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'urbansim.models.development_project_location_choice_model_creator': 'DevelopmentProjectLocationChoiceModelCreator'
                },
            'init': {
                'arguments': {
                    'location_set': 'location_set',
                    'model_configuration': "model_configuration['development_project_types']['project_type']",
                    'project_type': "'project_type'",
                    'submodel_string': None
                    },
                'name': 'DevelopmentProjectLocationChoiceModelCreator().get_model'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'base_year': "resources['base_year']",
                    'categories': "model_configuration['development_project_types']['project_type']['categories']",
                    'events_for_estimation_storage': 'base_cache_storage',
                    'events_for_estimation_table': "'events_for_estimation_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, projects)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'coefficients_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'input_agent_set',
                    'chunk_specification': "{'records_per_chunk':9999}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 7777,
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()