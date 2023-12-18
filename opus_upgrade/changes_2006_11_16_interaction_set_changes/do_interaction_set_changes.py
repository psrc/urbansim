# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import re
import sys

from optparse import OptionParser
from .classes.db_sub_pattern import DBSubPattern

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration



def main():
    my_dir = os.path.split(__file__)[0]
    sub_file = os.path.join(my_dir, 'substitutions.txt')
    
    patterns = []
    f = open(sub_file)
    for line in f:
        if line.endswith('\n'):
            line = line[:-1]
        
        values = line.split(' ')
        if len(values) > 2:
            print ("Invalid format for 'substitutions.txt': Too many "
                "space-separated values on a single line.")
            return
        if len(values) < 2:
            print ("Invalid format for 'substitutions.txt': Too few "
                "space-separated values on a single line.")
            return
        
        pattern, substitution = values
        pattern = r'\b%s\b' % re.escape(pattern)
        substitution = substitution
        patterns.append((pattern, substitution))
    
    parser = OptionParser()
    
    parser.add_option("-o", "--host", dest="host", type="string",
        help="The mysql host (default: 'localhost').")
    parser.add_option("-u", "--username", dest="username", type="string",
        help="The mysql connection password (default: nothing).")
    parser.add_option("-p", "--password", dest="password", type="string",
        help="The mysql connection password (default: nothing).")
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
    
    if options.backup == None: options.backup = True
    if options.postfix == None: options.postfix = '_old'
    
    if (options.databases == None) or (options.tables == None): 
        print ('At least one database and one table must be specified. Please '
            'see the usage instructions provided below.\n\n')
        parser.print_help()
        return
    
    table_list = {}
    for db_name in options.databases:
        table_list[db_name] = []
        for table in options.tables:
            table_list[db_name] += [table]    
    
    
    db_config = DatabaseServerConfiguration(
        protocol = 'mysql',
        host_name = options.host,
        user_name = options.username,
        password = options.password,
        )
        
    if len(options.databases) > 1:
        print("Converting databases on host %s..." % options.host)
        DBSubPattern().convert_databases(db_config, options.databases, table_list, patterns, options.backup, options.postfix)
        print("Done.")
        
    elif len(options.tables) > 1:
        print("Converting tables in database %s on host %s" % (options.databases[0], options.host))
        dbconfig = DatabaseServerConfiguration(
            protocol = 'mysql',
            host_name = db_config.host_name,
            user_name = db_config.user_name,
            password = db_config.password                                       
        )        
        db_server = DatabaseServer(dbconfig)
        db = db_server.get_database(options.databases[0])
        
        DBSubPattern().convert_database(db, options.tables, patterns, options.backup, options.postfix)
        print("Done.")
    
    else:
        print("Converting table %s in database %s on host %s" % (options.tables[0], options.databases[0], options.host))

        dbconfig = DatabaseServerConfiguration(
            host_name = db_config.host_name,
            user_name = db_config.user_name,
            protocol = 'mysql',
            password = db_config.password                                       
        )        
        db_server = DatabaseServer(dbconfig)
        db = db_server.get_database(options.databases[0])
        
        DBSubPattern().convert_table(db, options.tables[0], patterns, options.backup, options.postfix)
        print("Done.")

    
if __name__ == "__main__":
    main()