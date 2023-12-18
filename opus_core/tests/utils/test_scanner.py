# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, inspect, traceback, re
from opus_core.tests import opus_unittest

from opus_core.logger import logger

class TestScanner(object):

    def find_opus_test_cases_for_package(self, package):
        return self._find_opus_test_cases_for_package(package, opus_unittest.OpusTestCase)


    def find_opus_integration_test_cases_for_package(self, package):
        return self._find_opus_test_cases_for_package(package, opus_unittest.OpusIntegrationTestCase)


    def _find_opus_test_cases_for_package(self, package, test_case_class):
        root = OpusPackage().get_path_for_package(package)
        
        modules_with_test_cases = []
        
        for path, dirs, files in os.walk(root, topdown=True):
            for file in files:
                if not file.endswith('.py'):
                    continue
                    
                f = open(os.path.join(path,file), 'r')
                import_pattern = re.compile('^\s*(import|from).*unittest')
                skip_pattern = re.compile('^.*#.*IGNORE_THIS_FILE')
                
                found_import = False
                for line in f:
                    if skip_pattern.match(line):
                        break
                    if import_pattern.match(line):
                        found_import = True
                        break
                    
                if not found_import: # No unittest import found in file.
                    continue
                
                module_name = self._get_module_name(package, root, path, file)
                
                try:
                    exec('import %s' % module_name)
                except Exception as val: 
                    logger.log_error("Could not import %s!" % module_name)
                    
                    traceback.print_exc()
                    
                    continue

                module = eval(module_name)
                
                if inspect.ismodule(module):
                    members = inspect.getmembers(module)
                    
                    member_dict = {}
                    for key, value in members:
                        member_dict[key] = value
                    
                    for key in list(member_dict.keys()):
                        try:
                            is_subclass = issubclass(
                                member_dict[key], 
                                test_case_class)
                        except: pass
                        else:
                            if is_subclass:
                                class_name = member_dict[key].__name__
                                
                                modules_with_test_cases.append(
                                    (module_name, class_name))
                        
                else:
                    logger.log_warning(
                        'WARNING: %s is not a module!' % module)
                               
        return modules_with_test_cases
        

    def _get_module_name(self, package, root, path, file):
        file = file[0:-len('.py')]
        
        path = path.replace(root, '')
        if path.startswith(os.sep):
            path = path[1:]
        module_path = path.replace(os.sep, '.')
        
        if module_path is not '':
            module_path = '.'.join([package, module_path])
        else:
            module_path = package
            
        return '.'.join([module_path, file])


from opus_core.tests import opus_unittest
from random import randint
from opus_core.opus_package import OpusPackage

main_test_case = 'TestTestScanner'
class TestTestScanner(opus_unittest.OpusTestCase):
    def setUp(self):
        # While any warnings we receive ought to be legitimate, we are not
        # concerned with those right now.
        logger.enable_hidden_error_and_warning_words()
        
    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()
    
    def test_get_module_name(self):
        package = 'opus_core'
        base_path = os.path.join('workspace', 'opus', package)
        module_name = 'test_scanner'
        file_name = '%s.py' % module_name
        path = TestScanner()._get_module_name(
            package,
            base_path,
            os.path.join(base_path, 'tests', 'utils'),
            file_name)
        
        expected = '%s.tests.utils.%s' % (package, module_name)
        self.assertTrue(path == expected,
            "Unexpected module path: Expected %s. Received %s."
                % (expected, path))
                
        package = 'package'
        base_path = os.path.join('workspc', package)
        module_name = 'test_module'
        file_name = '%s.py' % module_name
        path = TestScanner()._get_module_name(
            package,
            base_path,
            os.path.join(base_path, 'test'),
            file_name)
        
        expected = '%s.test.%s' % (package, module_name)
        self.assertTrue(path == expected,
            "Unexpected module path: Expected %s. Received %s."
                % (expected, path))
            
    
    def test_find_files_with_test_cases(self):
        package = 'opus_core'
        test_modules = TestScanner().find_opus_test_cases_for_package(package)
        
        self.assertTrue(
            'opus_core.tests.utils.test_scanner' in [i[0] for i in test_modules],
            "TestScanner did not find itself "
            "(opus_core.tests.utils.test_scanner)!")
            
        for test_case in test_cases_in_this_file:
            self.assertTrue(
                test_case in [i[1] for i in test_modules],
                "TestScanner did not find one of its own test cases "
                "(%s)!" % test_case)
        
            
    def test_does_not_find_files_without_test_cases(self):
        path = OpusPackage().get_path_for_package('opus_core')
        path = os.path.join(path, 'tests', 'utils')
        
        module_name = 'test_scanner_test_file'
        file_name = '%s.py' % module_name
        file_name = os.path.join(path, file_name)
        
        f = open(file_name, 'w')
        
        f.write("""class TestClass(object):
    def test_method(self):
        print 'Delete me if you wish, for I am but a unit-test test file!'"""
            )
        
        f.close()
        
        self.assertTrue(os.path.exists(file_name))
        
        package = 'opus_core'
        test_modules = TestScanner().find_opus_test_cases_for_package(package)
                            
        self.assertTrue(
            'opus_core.tests.utils.%s' % module_name not in test_modules,
            "TestScanner found a test file created without unit tests "
            "(opus_core.tests.utils.%s)!" % module_name)
        
        os.remove(file_name)
        

test_cases_in_this_file = [main_test_case]
for i in range(5):
    name = 'AutoTestCase%s' % i
    test_cases_in_this_file.append(name)
    exec("""class %s(opus_unittest.OpusTestCase):
    \"""Automatic test case generated for %s.\""" """ % (name, main_test_case))

    
if __name__ == '__main__':
    opus_unittest.main()