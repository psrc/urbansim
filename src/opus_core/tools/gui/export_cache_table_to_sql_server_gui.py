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

from enthought.traits import Directory, Str, Password, Int
from enthought.traits.ui import View, Group, Item

from opus_core.tools.gui.command_gui import CommandGui
from opus_core.tools.command.export_cache_table_to_sql_server_command import ExportCacheTableToSqlServerCommand

class ExportCacheTableToSqlServerGui(CommandGui):
    cache_directory = Directory
    year = Int
    table_name = Str
    hostname = Str
    username = Str
    password = Password
    database_name = Str
    
    def __init__(self):
        CommandGui.__init__(self, 
            command_class = ExportCacheTableToSqlServerCommand
            )
    
    help_cache_directory = ('The base directory of the attribute cache.')
    help_year = ('The year in which the table to export is found.')
    help_table_name = ('The name of the table to export.')
    help_hostname = ('The hostname where the server is found, e.g. WICKERSHAM\SQLEXPRESS')
    help_username = ('The username to use to connect to the MS SQL Server service.')
    help_password = ('The password to use to connect to the MS SQL Server service.')
    help_database_name = ('The name of an existing database to which the table will be exported.')
    
    my_view = View(
        Group(
            Group(
                Item('cache_directory', help=help_cache_directory),
                Item('year', help=help_year),
                Item('table_name', help=help_table_name),
                label='AttributeCache configuration',
                show_border=True,
                ),
            '10',
            Group(
                Item('hostname', help=help_hostname),
                Item('username', help=help_username),
                Item('password', help=help_password),
                Item('database_name', help=help_database_name),
                label='SQL Server configuration',
                show_border=True,
                ),
                layout='normal',
            ),
        title = 'Export Cache Table to SQL Server',
        width = 500,
        buttons = CommandGui._buttons,
        kind = 'livemodal',
        )


if __name__ == '__main__':
    from opus_core.store.attribute_cache import AttributeCache
    from opus_core.session_configuration import SessionConfiguration
    
    SessionConfiguration(new_instance=True, in_storage=AttributeCache)
    args = ExportCacheTableToSqlServerGui()
    args.configure_traits()