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
from os import walk
from os import environ
from os.path import join
from opus_core.tests import opus_unittest

class TestForMySQLPassword_abstract(opus_unittest.OpusTestCase):
    modul = None
    def test_no_mysql_password_in_files(self):
        if self.modul is not None:
            password = environ['MYSQLPASSWORD']
            files = []
            for root, unused_dirs, file_names in walk(__import__(self.modul).__path__[0]):
                files.extend([join(root, name) for name in file_names])
            for file_name in files:
                try:
                    cat = ""
                    cat = file(file_name, "r").read()
                except:
                    pass
                self.assert_(cat.find(password) < 0, "found mysql password in %s" % file_name)
                
class TestForMySQLPassword(TestForMySQLPassword_abstract):
    modul = "opus_core"
            
if __name__ == "__main__":
    opus_unittest.main()
