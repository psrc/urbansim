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

from enthought.traits.api import HasTraits, Directory, Str, Password, Int
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from enthought.traits.api import View, Group, Item

from opus_core.tools.command.export_sql_server_to_cache_command import ExportSqlServerToCacheCommand 

class GuiExportSqlServerToCacheTable(HasTraits):
    cache_directory = Directory
    year = Int
    table_name = Str
    hostname = Str
    username = Str
    password = Password
    database_name = Str
    
    help_cache_directory = ('The base directory of the attribute cache.')
    help_year = ('The year in which the table will be exported.')
    help_table_name = ('The name of the table to export.')
    help_hostname = ('The hostname where the server is found, e.g. WICKERSHAM\SQLEXPRESS')
    help_username = ('The username to use to connect to the MS SQL Server service.')
    help_password = ('The password to use to connect to the MS SQL Server service.')
    help_database_name = ('The name of an existing database where the table is found.')
    
    my_view = View(
        Group(
            Group(
                Item('hostname', help=help_hostname),
                Item('username', help=help_username),
                Item('password', help=help_password),
                Item('database_name', help=help_database_name),
                label='SQL Server configuration',
                show_border=True,
                ),
            Item('table_name', help=help_table_name),
            Group(
                Item('cache_directory', help=help_cache_directory),
                Item('year', help=help_year),
                label='AttributeCache configuration',
                show_border=True,
                ),
                layout='normal',
            ),
        title = 'Export SQL Server to Cache Table',
        width = 500,
        ok = True, cancel = True, apply = False, revert = False, undo = False, help = False,
        kind = 'modal',
        )
    
def run_gui_export_sql_server_to_cache_table():
    """
    Collect the parameters from the user.
    """
    import os
    import sys

    args = GuiExportSqlServerToCacheTable()
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)

    cache_directory = args.cache_directory
    if not os.path.exists(cache_directory):
        print "ERROR: No such directory: '%s'." % cache_directory
        sys.exit(1)
    
    table_name = args.table_name
    year = args.year
    cache_directory = args.cache_directory
    hostname=args.hostname
    username=args.username
    password=args.password
    database_name=args.database_name 
    
    print ("Exporting table '%s' from '%s' to cache at '%s' in year %s..." 
        % (table_name, hostname, cache_directory, year))
    
    exporter = ExportSqlServerToCacheCommand(
        cache_directory=cache_directory,
        table_name=table_name, 
        year=year,
        hostname=hostname,
        username=username,
        password=password,
        database_name=database_name, 
        )
    exporter.execute()
    
    print 'Done.'


if __name__ == '__main__':
    run_gui_export_sql_server_to_cache_table()