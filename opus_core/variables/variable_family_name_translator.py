# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import re
from glob import glob1
from functools import reduce

class VariableFamilyNameTranslator(object):
    """Convert between variable names with wildcards 
        in the name (eg devtype_NNN<==>devtype_123)"""
    
    # used to cache variable families
    _variable_families = {} 
    _variable_family_patterns = {'DDD': ('(\d+)', int), 'SSS': ('([a-z_]+)', str)}   # variable pattern to reg_exp mapping. 'NNN': '(\d+)', 

    def _substitute_types(self, string):
        """returns a list of the types that the expression substitutes 
        ie devSSS_DDD -> [str, int]"""
        types = []
        patterns = list(self._variable_family_patterns.keys())
        while string:
            for p in patterns:
                if string.startswith(p):
                    types.append(self._variable_family_patterns[p][1])
                    string = string[len(p)-1:]
                    break
            string = string[1:]
        return types
            
    def _variable_name_to_reg_exp(self, variable_name):
        """Using _variable_family_patterns replace every key with the conjugate value. 
        eg f('devtype_DDD_SSS')->'devtype_(\d+)_(\D+)'"""           
        return reduce(lambda prev_exp, var_symb: prev_exp.replace(var_symb, 
                                                                  self._variable_family_patterns[var_symb][0]),
                      list(self._variable_family_patterns.keys()),
                      variable_name)
        
    def _reg_exp_to_variable_name(self, reg_exp):
        return reduce(lambda prev_exp, var_symb: prev_exp.replace(self._variable_family_patterns[var_symb][0], 
                                                                  var_symb),
                      list(self._variable_family_patterns.keys()),
                      reg_exp)
    
    def is_a_family_variable_name(self, variable_name):
        """Does the variable name contain a variable_family_pattern key?"""
        return re.findall('|'.join(list(self._variable_family_patterns.keys())), variable_name)
    
    def translate_family_name_into_instance_name(self, variable_name, substrings):
        """Returns the fully specified instance name constructed by substituting the
        give subsrings into the variable name, e.g. returns 'a_x_42' for inputs
        'a_SSS_DDD' and ('x', 42').
        """
        v_name = reduce(lambda prev_exp, var_symb: prev_exp.replace(var_symb, '%s'),
                      list(self._variable_family_patterns.keys()),
                      variable_name)
        return  v_name % tuple(map(str, substrings))
    
    def compare_instance_name_of_module_to_variable_name(self, instance_name, variable_name):
        """Compares the instance name of a variable to the family name of the variable to make sure
        that the instance name builds off of the family name.  Returns a boolean based on this 
        determination. 
        """
        variable_name_parts = variable_name.split('.')
        module_name = variable_name_parts[-1]
        instance_variable = instance_name.split('.')[-1]
        relative_path = '.'.join(variable_name_parts[0:-1])
        computed_family_name = self.get_translated_variable_name_and_substring_arguments(
            relative_path, instance_variable)[0]
        return module_name == computed_family_name
    
    def _set_variable_families_for_module(self, module_name):
        """Sets _variable_families[module_name] = [parsable names in module (as regular expressions)] 
        Gets a list of *.py files in the directory at module_name. """
        if module_name in self._variable_families:
            return
        try:
            module = __import__(module_name, globals(), locals(), ['anything_here_will_do'])
        except:
            self._variable_families[module_name] = []
            return
        
        # get python source files in module dir
        submodules_variables = [file_name[:-len('.py')] for file_name in glob1(module.__path__[0], '*.py')]
                
        self._variable_families[module_name] = list(filter(self.is_a_family_variable_name, submodules_variables))       
    
    def get_translated_variable_name_and_substring_arguments(self, directory_path, short_variable_name):
        """Translates the variable name and returns the pertinant substrings. 
        Function takes as argument the full path to the directory containing the variable's Python
        module (e.g. 'C:/myworkspace/urbansim/gridcell', and the short name for the variable 
        (e.g., 'population'). 
        
        Returns a tuple where the first item is the (possibly) translated name and second item are the 
        found arguments parsed out as a tuple.
        
        Example- If there is a family variable in fooDDD
        calling: get_translated_variable_name_and_substring_arguments('package.dataset', 'foo21') 
        returns: ('fooDDD', (21,))
        """
        try:    
            # see if variable name is fine as it is by seeing if we can just import it
            __import__('.'.join([directory_path, short_variable_name]))
        except: # look for family names
            self._set_variable_families_for_module(directory_path)
            family_matches = []
            for var_family_name in self._variable_families[directory_path]:
                substrings = re.findall(self._variable_name_to_reg_exp(var_family_name), short_variable_name)
                if substrings:
                    if not isinstance(substrings[0], tuple):
                        substrings[0] = (substrings[0],)  # only one element, force tuple
                    # translate back to make sure we have the right variable and handle those funny cases
                    if self.translate_family_name_into_instance_name(var_family_name, substrings[0]) != short_variable_name:
                        continue   
                    as_desired_types = list(map(lambda fn, x: fn(x),#(fn_x[0])(fn_1), 
                                           self._substitute_types(var_family_name),
                                           substrings[0]))
                    family_matches.append((var_family_name, tuple(as_desired_types)))
            how_many_matches = len(family_matches)
            if how_many_matches > 1:
                matching_families = str([name_val[0] for name_val in family_matches])
                raise LookupError("""Multiple family variables matched %(short_variable_name)s 
                in %(directory_path)s, these matches where %(matching_families)s""" % locals())
            if how_many_matches == 1:
                return family_matches[0]
        # we could import variable or there was no matching family found
        return (short_variable_name, ()) 
    
from opus_core.tests import opus_unittest
import time
class VariableFamilyNameTranslatorTests(opus_unittest.OpusTestCase):
    def test_compare_instance_name_of_module_to_variable_name(self):
        instance_name = "opus_core.test.attr_test_family_32"
        variable_name = "opus_core.test.attr_test_family_DDD"
        self.assertTrue(VariableFamilyNameTranslator().\
                     compare_instance_name_of_module_to_variable_name(instance_name, variable_name))
    
        instance_name = "opus_core.test.attr_test_family_32"
        variable_name = "opus_core.test.not_a_member"
        self.assertTrue(not VariableFamilyNameTranslator().\
                     compare_instance_name_of_module_to_variable_name(instance_name, variable_name))
    
    def test_translate_family_name_into_instance_name(self):
        trans = VariableFamilyNameTranslator()
        self.assertEqual(trans.translate_family_name_into_instance_name('a_SSS_DDD_var', ('x', 42)),
                         'a_x_42_var')
        self.assertEqual(trans.translate_family_name_into_instance_name('a_SSS_DDD_var', ('x_o_x', 42)),
                         'a_x_o_x_42_var')
        
    def test_variable_translation(self):
        short_name, arguments = VariableFamilyNameTranslator(). \
                  get_translated_variable_name_and_substring_arguments(
                      'opus_core.tests', 
                      'a_test_one_variable_123_five_parts_in_this_substring')
        self.assertTrue(short_name=='a_test_SSS_variable_DDD_SSS')
        self.assertTrue(('one', 123, 'five_parts_in_this_substring')==arguments)
        
    def test_no_variable_translation(self):
        short_name, arguments = VariableFamilyNameTranslator(). \
                  get_translated_variable_name_and_substring_arguments(
                      'opus_core.tests', 
                      'a_test_variable')
        self.assertTrue(short_name=='a_test_variable')
        self.assertTrue(()==arguments)
        
    def test_no_variable_found(self):
        short_name, arguments = VariableFamilyNameTranslator(). \
                  get_translated_variable_name_and_substring_arguments(
                      'opus_core.tests', 
                      'not_a_123_variable')
        self.assertTrue(short_name=='not_a_123_variable')
        self.assertTrue(()==arguments)
    
    def test_two_variables_next_to_each_other(self):
        short_name, arguments = VariableFamilyNameTranslator(). \
                  get_translated_variable_name_and_substring_arguments(
                      'opus_core.tests', 
                      'a_test_123_five_parts_in_this_substring')
        self.assertTrue(short_name=='a_test_DDDSSS')
        self.assertTrue((123, '_five_parts_in_this_substring')==arguments)
        
    def test_multiple_matches(self):
        translator = VariableFamilyNameTranslator()
        module = 'opus_core.tests'
        translator._set_variable_families_for_module(module)
        translator._variable_families[module].append('a_SSSDDDSSS')    # add a fake variable name, to get ambigious answer
        try:
            self.assertRaises(LookupError, 
                translator.get_translated_variable_name_and_substring_arguments,
                module, 'a_test_123_five_parts_in_this_substring')
        finally:
            translator._variable_families.clear()
            
if __name__=='__main__':
    opus_unittest.main()