# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

class IndicatorsDatabaseConfiguration(DatabaseConfiguration):
    
    def _database_configuration_node(self):
        return 'indicators_database_server'

if __name__ == '__main__':
    config = IndicatorsDatabaseConfiguration()
#    print config   