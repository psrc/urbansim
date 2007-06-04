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


class BuildingLocationChoiceModelConfigurationCreator(HasStrictTraits):
    records_per_chunk = Int(500)
    debuglevel = Trait('debuglevel', Str, Int)
    agent_set = Str('building')
    location_set = Str('gridcell')
    sample_size_locations = Int(30)
    attribute_to_group_by = Str('building_type.name')
    
    coefficients_table = Str('development_location_choice_model_coefficients')
    specification_table = Str('development_location_choice_model_specification')

    input_index = Str('brm_index')

    _model_name = 'building_location_choice_model'
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'bindex'
        
        try:
            attribute_to_group_by_dataset_name, attribute_to_group_by_attribute_name = self.attribute_to_group_by.split('.')
        except:
            raise Exception("Attribute to group by must be of the form "
                "'dataset_name.attribute_name', where dataset_name is the name "
                "of the dataset containing the attribute to group by "
                "(attribute_name). Received '%s'." % self.attribute_to_group_by)
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': _index,
                    'data_objects': 'datasets',
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients,
                },
            'group_by_attribute': (attribute_to_group_by_dataset_name, attribute_to_group_by_attribute_name),
            'import': {
                'urbansim.models.%s' % self._model_name: 'BuildingLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    },
                'name': 'BuildingLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'building_categories': ### TODO: Construct this list from the development_project_type_configuration info
                        """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'dataset_pool': 'dataset_pool',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _index)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients),
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': self.input_index,
                    'chunk_specification': "{'records_per_chunk':%s}" % self.records_per_chunk,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestBuildingLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = BuildingLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'building',
                    'agents_index': 'bindex',
                    'data_objects': 'datasets',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'group_by_attribute': ('building_type', 'name'),
            'import': {
                'urbansim.models.building_location_choice_model': 'BuildingLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_set': 'gridcell',
                    'sample_size_locations': 30
                    },
                'name': 'BuildingLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'building',
                    'building_categories': """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'dataset_pool': 'dataset_pool',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'development_location_choice_model_specification'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, bindex)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'development_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'development_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'building',
                    'agents_index': 'brm_index',
                    'chunk_specification': "{'records_per_chunk':500}",
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
        creator = BuildingLocationChoiceModelConfigurationCreator(
            records_per_chunk = 9999,
            debuglevel = 8888,
            agent_set = 'agent_set',
            location_set = 'location_set',
            sample_size_locations = 7777,
            attribute_to_group_by = 'dataset.attribute_name',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            input_index = 'input_index',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'bindex',
                    'data_objects': 'datasets',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'group_by_attribute': ('dataset', 'attribute_name'),
            'import': {
                'urbansim.models.building_location_choice_model': 'BuildingLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_set': 'location_set',
                    'sample_size_locations': 7777,
                    },
                'name': 'BuildingLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'building_categories': """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'dataset_pool': 'dataset_pool',
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, bindex)'
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
                    'agent_set': 'agent_set',
                    'agents_index': 'input_index',
                    'chunk_specification': "{'records_per_chunk':9999}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 8888,
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()