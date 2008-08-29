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
from opus_core.tests import opus_unittest
from opus_core.tests.check_for_sql_password import TestForSQLPassword_abstract
class TestForSQLPassword(TestForSQLPassword_abstract):
    modul = "waterdemand"
            
if __name__ == "__main__":
    opus_unittest.main()
