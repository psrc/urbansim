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

from opus_core.tests.utils.test_scanner import TestScanner

class PackageTestLoader(object):
    def load_tests_from_package(self, package, parent=__import__('__main__')):
        """
        Load test cases from the package with the given name (e.g. 'opus_core') 
        into the parent object. Use __import__('__main__') as the parent if you 
        wish to simply run opus_unittest.main. Otherwise, call 
        opus_unittest.main(module=parent).
        """
        
        test_cases = TestScanner().find_opus_test_cases_for_package(package)
        
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