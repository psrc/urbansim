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

from opus_core.tests import opus_unittest

class TestPackageSyntax(opus_unittest.OpusTestCase):
    def test_no_opus_syntax_violations(self):
        from opus_core.tests.find_opus_syntax_violations import OpusSyntaxChecker
        OpusSyntaxChecker().check_syntax_for_opus_package(
            'opus_emme2', 
            file_names_that_do_not_need_gpl = 
                ['wingdbstub.py', 'ez_setup.py', 'path.py'])
        
        
if __name__ == "__main__":
    opus_unittest.main()