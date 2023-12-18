# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from os import walk
from os import environ
from os.path import join
from opus_core.tests import opus_unittest

class TestForSQLPassword(opus_unittest.OpusTestCase):
    modul = None

    def __init__(self, method_name = 'test_no_sql_password_in_files', package_name = None):
        opus_unittest.OpusTestCase.__init__(self, method_name)
        if package_name is not None:
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
                self.assertTrue(cat.find(password) < 0, "found sql password in %s" % file_name)
          
if __name__ == "__main__":
    opus_unittest.main()
