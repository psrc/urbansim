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


class BuildingTransitionModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    building_set = Str('building')
    location_set = Str('gridcell')
    building_types_table = Str('building_type')
    vacancy_table = Str('target_vacancy')
    
    _model_name = 'building_transition_model'
    
    def execute(self):
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'BuildingTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'BuildingTransitionModel'
                },
            'run': {
                'arguments': {
                    'building_categories':  ### TODO: Construct this list from the development_project_type_configuration info
                        """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'building_set': self.building_set,
                    'building_types_table': self.building_types_table,
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'vacancy_table': self.vacancy_table,
                    'year': 'year',
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestBuildingTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = BuildingTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.building_transition_model': 'BuildingTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'BuildingTransitionModel'
                },
            'run': {
                'arguments': {
                    'building_categories': """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'building_set': 'building',
                    'building_types_table': 'building_type',
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'vacancy_table': 'target_vacancy',
                    'year': 'year',
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = BuildingTransitionModelConfigurationCreator(
            debuglevel = 9999,
            building_set = 'building_set',
            location_set = 'location_set',
            building_types_table = 'building_types_table',
            vacancy_table = 'vacancy_table',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.building_transition_model': 'BuildingTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'BuildingTransitionModel'
                },
            'run': {
                'arguments': {
                    'building_categories': """{
                        'residential': array([1,2,3,5,10,20]), 
                        'commercial': 1000*array([1, 2, 5, 10]), 
                        'industrial': 1000*array([1,2,5,10])
                        }""",
                    'building_set': 'building_set',
                    'building_types_table': 'building_types_table',
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'vacancy_table': 'vacancy_table',
                    'year': 'year',
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()