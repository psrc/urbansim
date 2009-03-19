# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

class ValidationInformation(object):
    def __init__(self, is_valid, error_data=None):
        self.is_valid = is_valid
        self._error_data = error_data
    
    def get_failed_parameter_names(self):
        if self._error_data is None:
            return None
        
        return self._error_data.keys()
    
    def get_string(self):
        if self._error_data is None:
            return "All parameters passed validation."
        
        parameter_messages = [
            "* %s: %s" % (key, value)
            for key, value in self._error_data.iteritems()
            ]
        
        return ("The following parameters failed to validate:\n\n%s" 
            % '\n\n'.join(parameter_messages))
    
    def __str__(self):
        return self.get_string()
        
    
from opus_core.tests import opus_unittest

from sets import Set


class ValidationInformationTest(opus_unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_is_valid_property_is_set_through_constructor(self):
        expected_is_valid = False
        info = ValidationInformation(is_valid=expected_is_valid)
        self.assertEqual(expected_is_valid, info.is_valid)
        
        # Triangulate
        expected_is_valid = True
        info = ValidationInformation(is_valid=expected_is_valid)
        self.assertEqual(expected_is_valid, info.is_valid)
        
    def test_returns_a_nicely_formatted_string_from_get_string_when_error_data_is_present(self):
        possible_string1 = ("The following parameters failed to validate:\n\n"
            "* parameter1: The parameter1 parameter is just wrong, OK?!?\n\n"
            "* parameter2: (Just kidding)")
        possible_string2 = ("The following parameters failed to validate:\n\n"
            "* parameter1: The parameter1 parameter is just wrong, OK?!?\n\n"
            "* parameter2: (Just kidding)")
        info = ValidationInformation(
            is_valid = False, 
            error_data = {
                'parameter1':'The parameter1 parameter is just wrong, OK?!?',
                'parameter2':'(Just kidding)',
                }
            )
        self.assert_(
            (info.get_string() == possible_string1) or
            (info.get_string() == possible_string1)
            )
        
        expected_string = ("The following parameters failed to validate:\n\n"
            "* parameterA: ParameterA message.")
        info = ValidationInformation(
            is_valid = False, 
            error_data = {
                'parameterA':'ParameterA message.',
                }
            )
        self.assertEqual(info.get_string(), expected_string)
        
    def test_returns_a_nicely_formatted_string_from_get_string_when_there_is_no_error_data(self):
        expected_string = "All parameters passed validation."

        info = ValidationInformation(is_valid=True)
            
        self.assertEqual(info.get_string(), expected_string)
        
    def test_returns_a_nicely_formatted_string_from_str_when_error_data_is_present(self):
        expected_string = ("The following parameters failed to validate:\n\n"
            "* parameterA: ParameterA message.")

        info = ValidationInformation(
            is_valid = False, 
            error_data = {
                'parameterA':'ParameterA message.',
                }
            )
            
        self.assertEqual(str(info), expected_string)
        
    def test_returns_a_nicely_formatted_string_from_str_when_there_is_no_error_data(self):
        expected_string = "All parameters passed validation."

        info = ValidationInformation(is_valid=True)
            
        self.assertEqual(str(info), expected_string)
        
    def test_returns_list_of_failed_parameter_names_on_get_failed_parameter_names_when_error_data_is_present(self):
        expected_failed_parameters = ['A', 'B', 'C']
        info = ValidationInformation(
            is_valid = False, 
            error_data = {
                'A':None,
                'B':None,
                'C':None,
                }
            )
        self.assertEqual(Set(info.get_failed_parameter_names()), Set(expected_failed_parameters))
        
        # Triangulate
        expected_failed_parameters = ['Mr', 'E']
        info = ValidationInformation(
            is_valid = False, 
            error_data = {
                'Mr':None,
                'E':None,
                }
            )
        self.assertEqual(Set(info.get_failed_parameter_names()), Set(expected_failed_parameters))
        
    def test_returns_list_of_failed_parameter_names_on_get_failed_parameter_names_when_there_is_no_error_data(self):
        expected_failed_parameters = None
        
        info = ValidationInformation(is_valid=True)
        
        self.assertEqual(info.get_failed_parameter_names(), expected_failed_parameters)
        
        
if __name__ == '__main__':
    opus_unittest.main()