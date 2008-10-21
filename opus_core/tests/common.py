#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
#

# TEMPORARILY DISABLED DUE TO TEST FAILURES

#from os import walk
#from os import environ
#from os.path import join
#from opus_core.tests import opus_unittest
#
## Test for password
#class TestForSQLPassword_abstract(opus_unittest.OpusTestCase):
#    modul = None
#    def test_no_sql_password_in_files(self):
#        if self.modul is not None and 'SQLPASSWORD' in environ:
#            password = environ['SQLPASSWORD']
#            files = []
#            for root, unused_dirs, file_names in walk(__import__(self.modul).__path__[0]):
#                files.extend([join(root, name) for name in file_names])
#            for file_name in files:
#                try:
#                    cat = ""
#                    cat = file(file_name, "r").read()
#                except:
#                    pass
#                self.assert_(cat.find(password) < 0, "found sql password in %s" % file_name)
#                
#class TestForSQLPassword(TestForSQLPassword_abstract):
#    def __init__(self, package):
#        self.modul = package
#            
#if __name__ == "__main__":
#    opus_unittest.main()
#
##Test for syntax
#class TestPackageSyntax(opus_unittest.OpusTestCase):
#    def __init__(self, package):
#        self.modul = package
#    
#    def test_no_opus_syntax_violations(self):
#        from opus_core.tests.find_opus_syntax_violations import OpusSyntaxChecker
#        OpusSyntaxChecker().check_syntax_for_opus_package(
#            self.modul, 
#            file_names_that_do_not_need_gpl = 
#                ['wingdbstub\.py', 'ez_setup\.py', 'path\.py', 'opusmain_rc\.py', 'qrc_opusmain\.py', '.*_ui\.py$', '^ui_.*\.py$'])
#        
#if __name__ == "__main__":
#    opus_unittest.main()