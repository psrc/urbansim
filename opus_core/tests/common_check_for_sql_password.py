# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from os import walk
from os import environ
from os.path import join
from opus_core.tests import opus_unittest

class TestForSQLPassword(opus_unittest.OpusTestCase):
    def __init__(self, method_name = 'test_no_sql_password_in_files', package_name = None):
        opus_unittest.OpusTestCase.__init__(self, method_name)
        self.modul = package_name

    def test_no_sql_password_in_files(self):
        if self.modul is not None and 'SQLPASSWORD' in environ:
            password = environ['SQLPASSWORD']
            files = []
            for root, unused_dirs, file_names in walk(__import__(self.modul).__path__[0]):
                files.extend([join(root, name) for name in file_names])
            for file_name in files:
                try:
                    cat = ""
                    cat = file(file_name, "r").read()
                except:
                    pass
                self.assert_(cat.find(password) < 0, "found sql password in %s" % file_name)
          
if __name__ == "__main__":
    opus_unittest.main()
