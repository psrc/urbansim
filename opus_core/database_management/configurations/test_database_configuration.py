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

import os

from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.database_management.configurations.database_server_configuration import get_default_database_engine, _get_installed_database_engines

def get_testable_engines():
    engines = []
    for engine in _get_installed_database_engines():
        try:
            TestDatabaseConfiguration(protocol = engine)
        except:
            pass
        else:
            engines.append(engine)
    return engines
    

class TestDatabaseConfiguration(DatabaseConfiguration):
    def __init__(self, 
                 protocol = get_default_database_engine(),
                 host_name = None,
                 user_name = None,
                 password = None,
                 database_name = None,
                 database_configuration = None):
        self.protocol = protocol
        DatabaseConfiguration.__init__(self,
                              protocol = protocol,
                              host_name = host_name,
                              user_name = user_name,
                              password = password,
                              database_name = database_name,
                              database_configuration = database_configuration,
                              test = True)
        
    def _database_configuration_node(self):
        return '%s_test_database_server'%(self.protocol.lower())   