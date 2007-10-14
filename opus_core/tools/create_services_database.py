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

import sys

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.database_management.table_type_schema import TableTypeSchema
from opus_core.logger import logger

class CreateServicesDBOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
                                        description="Create services database.")

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
        
    option_group = CreateServicesDBOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if args:
        parser.print_help()
        sys.exit(1)
    
    db_server = option_group.get_database_server(options)
    if not db_server.has_database(options.database_name):
        db_server.create_database(options.database_name)
        
    db = db_server.get_database(options.database_name)
    if not db.table_exists('run_activity'):
        tt_schema = TableTypeSchema()
        logger.start_block('Creating run_activity table in database %s on host %s' %
                               (options.database_name, options.host_name))
        try:
            db.create_table("run_activity", tt_schema.get_table_schema("run_activity"))
        finally:
            logger.end_block()
        logger.log_status("Table 'run_activity' created.")
    else:
        logger.log_status("Table 'run_activity' already existed.")

