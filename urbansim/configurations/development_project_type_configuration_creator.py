# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array

from opus_core.configuration import Configuration


class DevelopmentProjectTypeConfigurationCreator(object):
    _model_name = 'development_project_type'
    
    def __init__(self,
            categories = [1, 2, 3, 5, 10, 20],
            developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_residential_units',
            developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_residential_units',
            residential = True,
            units = 'residential_units'
            ):
        self.categories = categories
        self.developable_maximum_unit_variable_full_name = developable_maximum_unit_variable_full_name
        self.developable_minimum_unit_variable_full_name = developable_minimum_unit_variable_full_name
        self.residential = residential
        self.units = units
        
    def execute(self):        
        return Configuration({
            'categories': array(self.categories),
            'developable_maximum_unit_variable_full_name': self.developable_maximum_unit_variable_full_name,
            'developable_minimum_unit_variable_full_name': self.developable_minimum_unit_variable_full_name,
            'residential': self.residential,
            'units': self.units,
            })


from opus_core.tests import opus_unittest 


class TestDevelopmentProjectTypeConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentProjectTypeConfigurationCreator()
        
        expected = Configuration({
            'categories': array([ 1,  2,  3,  5, 10, 20]),
            'developable_maximum_unit_variable_full_name': 'urbansim.gridcell.developable_maximum_residential_units',
            'developable_minimum_unit_variable_full_name': 'urbansim.gridcell.developable_minimum_residential_units',
            'residential': True,
            'units': 'residential_units'
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentProjectTypeConfigurationCreator(
            categories = [9,9,9,9],
            developable_maximum_unit_variable_full_name = 'developable_maximum_unit_variable_full_name',
            developable_minimum_unit_variable_full_name = 'developable_minimum_unit_variable_full_name',
            residential = False,
            units = 'units',
            )
        
        expected = Configuration({
            'categories': array([9,9,9,9]),
            'developable_maximum_unit_variable_full_name': 'developable_maximum_unit_variable_full_name',
            'developable_minimum_unit_variable_full_name': 'developable_minimum_unit_variable_full_name',
            'residential': False,
            'units': 'units'
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()