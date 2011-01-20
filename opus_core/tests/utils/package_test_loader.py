# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests.utils.test_scanner import TestScanner

class PackageTestLoader(object):
    def load_tests_from_package(self, package, parent=__import__('__main__')):
        self._load_tests_from_package(package, parent, TestScanner().find_opus_test_cases_for_package)


    def load_integration_tests_from_package(self, package, parent=__import__('__main__')):
        self._load_tests_from_package(package, parent, TestScanner().find_opus_integration_test_cases_for_package)


    def _load_tests_from_package(self, package, parent, scanner):
        """
        Load test cases from the package with the given name (e.g. 'opus_core') 
        into the parent object. Use __import__('__main__') as the parent if you 
        wish to simply run opus_unittest.main. Otherwise, call 
        opus_unittest.main(module=parent).
        """
        
        test_cases = scanner(package)
        
        test_case_objects = []
        uid = 1
        for module, test_case in test_cases:
            # Create a unique import name.
            import_name = '%s___%s' % (module, test_case)
            import_name = '__'.join(import_name.split('.'))
            exec('from %s import %s as %s' % (module, test_case, import_name))
            test_case_objects.append((import_name, eval(import_name)))
        
        for object_name, object in test_case_objects:
            parent.__dict__[object_name] = object