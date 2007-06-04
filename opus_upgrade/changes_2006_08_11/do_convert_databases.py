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

import os

from optparse import OptionParser
from classes.convert_databases import ConvertDatabase

from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration


def main():
    parser = OptionParser()
    
    parser.add_option("-o", "--host", dest="host", type="string",
        help="The mysql host (default: 'localhost').")
    parser.add_option("-u", "--username", dest="username", type="string",
        help="The mysql connection password (default: MYSQLUSERNAME environment"
            " variable, then nothing).")
    parser.add_option("-p", "--password", dest="password", type="string",
        help="The mysql connection password (default: MYSQLPASSWORD environment"
            " variable, then nothing).")
    parser.add_option("-n", "--nobackup", action="store_false", dest="backup", 
        help="If this flag is present, no backup tables will be generated.")
    parser.add_option("-f", "--postfix", dest="postfix", type="string",
        help="The postfix to append to backup table names (default: '_old').")
    parser.add_option("-d", "--databases", action="append", dest="databases", 
        type="string", help="Add a databases to convert. This option may be "
            "used multiple times.")
    parser.add_option("-t", "--tables", action="append", dest="tables", 
        type="string", help="Add a table to convert. This option may be used "
            "multiple times.")
    (options, args) = parser.parse_args()
    
    if options.host == None: options.host = 'localhost'
    if options.username == None: 
        try: options.username = os.environ['MYSQLUSERNAME']
        except: options.username = ''
    if options.password == None: 
        try: options.password = os.environ['MYSQLPASSWORD']
        except: options.password = ''
    if options.backup == None: options.backup = True
    if options.postfix == None: options.postfix = '_old'
    
    if options.databases == None or options.tables == None: 
        print 'Nothing to convert.'
        return
    
    table_list = {}
    for db_name in options.databases:
        table_list[db_name] = []
        for table in options.tables:
            table_list[db_name] += [table]    
    
    
    db_config = DatabaseServerConfiguration(
        host_name = options.host,
        user_name = options.username,
        password = options.password,
        )
        
    config = {
        'databases':options.databases,
        'tables':table_list,
        
        'backup':options.backup,
        'backup_postfix':options.postfix,
        }    
    
    if len(options.databases) > 1:
        print "Converting databases on host %s..." % options.host
        ConvertDatabase().convert_databases(db_config, config)
        print "Done."
        
    elif len(options.tables) > 1:
        print "Converting tables in database %s on host %s" % (options.databases[0], options.host)
        db_server = MysqlDatabaseServer(db_config)
        db = db_server.get_database(options.databases[0])
        
        ConvertDatabase().convert_database(db, options.tables, options.backup, options.postfix)
        print "Done."
    
    else:
        print "Converting table %s in database %s on host %s" % (options.tables[0], options.databases[0], options.host)
        db_server = MysqlDatabaseServer(db_config)
        db = db_server.get_database(options.databases[0])
        
        ConvertDatabase().convert_table(db, options.tables[0], options.backup, options.postfix)
        print "Done."

    
if __name__ == "__main__":
    main()