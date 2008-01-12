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

from enthought.traits.api import HasTraits, Directory, Str, Password
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from opus_core.traits_ui.api import View, Group, Item


class GuiExportDbfTableToSQLServer(HasTraits):
    dbf_directory = Directory
    table_name = Str
    hostname = Str
    username = Str
    password = Password
    database_name = Str
    
    dbf_directory_help = ('The directory in which the dbf table files can be found.')
    table_name_help = ('The name of the dbf table file to load.')
    hostname_help = ('')
    username_help = ('')
    password_help = ('')
    database_name_help = ('')
    
    my_view = View(
        Group(
            Item('dbf_directory', help=dbf_directory_help),
            Item('table_name', help=table_name_help),
            Group(
                Item('hostname', help=hostname_help),
                Item('username', help=hostname_help),
                Item('password', help=hostname_help),
                Item('database_name', help=hostname_help),
                label = 'SQL Server Configuration',
                show_border = True,
                ),
            ),
            title = 'Export DBF Table to MS SQL Server',
            width = 500,
            ok = True, cancel = True, apply = False, revert = False, undo = False, help = False,
            kind = 'modal',
        )
        
def run_gui_export_cache_table_to_sql_server():
    """
    Collect the parameters from the user.
    """
    import os
    import sys

    from opus_core.tools.command.export_dbf_table_to_sql_server_command import ExportDbfTableToSqlServerCommand
    
    args = GuiExportDbfTableToSQLServer()
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)

    dbf_directory = args.dbf_directory
    if not os.path.exists(dbf_directory):
        print "ERROR: No such directory: '%s'." % dbf_directory
        sys.exit(1)
    
    table_name = args.table_name

    hostname = args.hostname
    username = args.username
    password = args.password
    database_name = args.database_name
    
    print ("Exporting table '%s' from '%s' to MS SQL Server on host '%s' in database '%s'..." 
        % (table_name, dbf_directory, hostname, database_name))
    
    exporter = ExportDbfTableToSqlServerCommand(
        dbf_directory = dbf_directory,
        table_name = table_name,
        hostname = hostname,
        username = username,
        password = password,
        database_name = database_name,
        )
    exporter.execute()
    
    print 'Done.'


if __name__ == '__main__':
    run_gui_export_cache_table_to_sql_server()