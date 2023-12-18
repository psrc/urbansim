# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array

from opus_core.configuration import Configuration

from urbansim.configurations.development_project_type_configuration_creator \
    import DevelopmentProjectTypeConfigurationCreator


class DevelopmentProjectTypesConfigurationCreator(object):
    
    _model_name = 'development_project_types'
    
    def __init__(self, *args, **kwargs):
        self.development_project_type_set = {}
        for development_project_type, config in kwargs.items():
            self.development_project_type_set[development_project_type] = config
    
    def execute(self):
        development_project_types = {}
        
        for development_project_type, config in self.development_project_type_set.items():
            development_project_types[development_project_type] = config.execute()
        
        return Configuration(development_project_types)


from opus_core.tests import opus_unittest 


class TestDevelopmentProjectTypesConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentProjectTypesConfigurationCreator(
            commercial = DevelopmentProjectTypeConfigurationCreator(
                categories = [1000, 2000, 5000, 10000],
                developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_commercial_sqft',
                developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_commercial_sqft',
                residential = False,
                units = 'commercial_sqft',
                ),
            industrial = DevelopmentProjectTypeConfigurationCreator(
                categories = [1000, 2000, 5000, 10000],
                developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_industrial_sqft',
                developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_industrial_sqft',
                residential = False,
                units = 'industrial_sqft',
                ),
            residential = DevelopmentProjectTypeConfigurationCreator(
                categories = [1, 2, 3, 5, 10, 20],
                developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_residential_units',
                developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_residential_units',
                residential = True,
                units = 'residential_units',
                )
            )
        
        expected = Configuration({
            'commercial': {
                'categories': array([ 1000,  2000,  5000, 10000]),
                'developable_maximum_unit_variable_full_name': 'urbansim.gridcell.developable_maximum_commercial_sqft',
                'developable_minimum_unit_variable_full_name': 'urbansim.gridcell.developable_minimum_commercial_sqft',
                'residential': False,
                'units': 'commercial_sqft'
                },
            'industrial': {
                'categories': array([ 1000,  2000,  5000, 10000]),
                'developable_maximum_unit_variable_full_name': 'urbansim.gridcell.developable_maximum_industrial_sqft',
                'developable_minimum_unit_variable_full_name': 'urbansim.gridcell.developable_minimum_industrial_sqft',
                'residential': False,
                'units': 'industrial_sqft'
                },
            'residential': {
                'categories': array([ 1,  2,  3,  5, 10, 20]),
                'developable_maximum_unit_variable_full_name': 'urbansim.gridcell.developable_maximum_residential_units',
                'developable_minimum_unit_variable_full_name': 'urbansim.gridcell.developable_minimum_residential_units',
                'residential': True,
                'units': 'residential_units'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentProjectTypesConfigurationCreator(
            foo = DevelopmentProjectTypeConfigurationCreator(
                categories = [9999],
                developable_maximum_unit_variable_full_name = 'package.geography.developable_maximum_stones',
                developable_minimum_unit_variable_full_name = 'package.geography.developable_minimum_stones',
                residential = False,
                units = 'stones',
                ),
            bar = DevelopmentProjectTypeConfigurationCreator(
                categories = [8888, 7777],
                developable_maximum_unit_variable_full_name = 'package.geography.developable_maximum_horsepower',
                developable_minimum_unit_variable_full_name = 'package.geography.developable_minimum_horsepower',
                residential = True,
                units = 'horsepower',
                ),
            baz = DevelopmentProjectTypeConfigurationCreator(
                categories = [6666, 5555, 4444],
                developable_maximum_unit_variable_full_name = 'package.geography.developable_maximum_karats',
                developable_minimum_unit_variable_full_name = 'package.geography.developable_minimum_karats',
                residential = False,
                units = 'karats',
                )
            )
        
        expected = Configuration({
            'foo': {
                'categories': array([9999]),
                'developable_maximum_unit_variable_full_name': 'package.geography.developable_maximum_stones',
                'developable_minimum_unit_variable_full_name': 'package.geography.developable_minimum_stones',
                'residential': False,
                'units': 'stones'
                },
            'bar': {
                'categories': array([8888, 7777]),
                'developable_maximum_unit_variable_full_name': 'package.geography.developable_maximum_horsepower',
                'developable_minimum_unit_variable_full_name': 'package.geography.developable_minimum_horsepower',
                'residential': True,
                'units': 'horsepower'
                },
            'baz': {
                'categories': array([6666, 5555, 4444]),
                'developable_maximum_unit_variable_full_name': 'package.geography.developable_maximum_karats',
                'developable_minimum_unit_variable_full_name': 'package.geography.developable_minimum_karats',
                'residential': False,
                'units': 'karats'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()