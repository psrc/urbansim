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

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait, ListInt, Bool

from opus_core.configuration import Configuration


class DevelopmentProjectTypeConfigurationCreator(HasStrictTraits):
    categories = ListInt([1, 2, 3, 5, 10, 20])
    developable_maximum_unit_variable_full_name = Str('urbansim.gridcell.developable_maximum_residential_units')
    developable_minimum_unit_variable_full_name = Str('urbansim.gridcell.developable_minimum_residential_units')
    residential = Bool(True)
    units = Str('residential_units')
    
    _model_name = 'development_project_type'
    
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