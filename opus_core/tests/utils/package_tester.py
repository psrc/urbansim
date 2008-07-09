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

import os
import sys
from opus_core.tests import opus_unittest
from warnings import filterwarnings
from opus_core.tests.utils.opus_test_runner import OpusTestRunner
from opus_core.tests.utils.opus_test_runner import OpusXMLTestRunner
from opus_core.tests.utils.package_test_loader import PackageTestLoader
from opus_core.opus_package import OpusPackage

class PackageTester(object):
    def run_all_tests_for_package(self, package):
        # Defaults
        loader = PackageTestLoader().load_tests_from_package
        xml_file_name = 'TEST_all_tests.xml'

        # Unlike 2.3, Python 2.4 complains about MySQL warnings. 
        #    We don't want to hear it.
        filterwarnings('ignore', "Can't (create|drop) database '[^']*'; ")
        filterwarnings('ignore', "Unknown table '[^']*'")
        filterwarnings('ignore', "Table '[^']*' already exists")
        
        # Will we do integration tests?
        for opt in sys.argv:
            if opt in ('-i','-I','--integration'):
                sys.argv.remove(opt)
                loader = PackageTestLoader().load_integration_tests_from_package
                xml_file_name = 'TEST_all_integration_tests.xml'
        
        loader(package)
        
        output_as_xml = False
        for opt in sys.argv:
            if opt in ('-x','-X','--xml'):
                sys.argv.remove(opt)
                output_as_xml = True

        if output_as_xml:
            file_path = os.path.join(OpusPackage().get_path_for_package(package), 'tests', xml_file_name)
            opus_unittest.main(testRunner=OpusXMLTestRunner(package, stream=open(file_path, 'w')))
        else:
            opus_unittest.main(testRunner=OpusTestRunner(package))

