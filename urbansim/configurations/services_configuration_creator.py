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

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait, ListInt

from opus_core.configuration import Configuration


class ServicesConfigurationCreator(HasStrictTraits):
    host_name = Str('localhost')
    user_name = Trait(None, None, Str)
    database_name = Str('services')
    
    _model_name = 'services_configuration'
    
    def execute(self):        
        return Configuration({
            'host_name':self.host_name,
            'user_name':self.user_name,
            'database_name':self.database_name,
            })
            

from opus_core.tests import opus_unittest 


class TestServicesConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = ServicesConfigurationCreator()
        
        expected = Configuration({
            'host_name':'localhost',
            'user_name':None,
            'database_name':'services',
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = ServicesConfigurationCreator(
            host_name = 'host_name',
            user_name = 'user_name',
            database_name = 'database_name',
            )
            
        expected = Configuration({
            'host_name':'host_name',
            'user_name':'user_name',
            'database_name':'database_name',
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()