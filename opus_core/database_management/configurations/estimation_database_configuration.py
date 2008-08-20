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

class EstimationDatabaseConfiguration(DatabaseConfiguration):
    
    def _database_configuration_node(self):
        return 'estimation_database_server'   
    
if __name__ == '__main__':
    config = EstimationDatabaseConfiguration()
    print config