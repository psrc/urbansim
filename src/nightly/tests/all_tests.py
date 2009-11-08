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

from opus_core.opus_package_info import package

from opus_core.tests import opus_unittest
import os

from opus_core.logger import logger

class AllTests(opus_unittest.OpusTestCase):
    def test_all_opus_packages(self):
        
        opus_path = package().get_package_parent_path()
        
        packages_to_test = [
            'opus_core',
            'eugene',
            'opus_emme2',
            'opus_manual',
            'opus_upgrade',
            'psrc',
            'urbansim',
            ]
        for opus_package_name in packages_to_test:
            tests_path = os.path.join(opus_path, opus_package_name, 'tests', 'all_tests.py')
            logger.start_block('Running tests for Opus package %s.\n' % opus_package_name)
            try:
                os.system('python %s' % tests_path)
            finally:
                logger.end_block()

if __name__ == "__main__":
    opus_unittest.main()

    