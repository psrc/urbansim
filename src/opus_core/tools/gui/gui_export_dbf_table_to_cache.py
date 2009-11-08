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

from enthought.traits import HasTraits, Directory, Str, Int
from enthought.traits.ui import View, Group, Item


class GuiExportDbfTableToCache(HasTraits):
    dbf_directory = Directory
    table_name = Str
    cache_directory = Directory
    year = Int
    
    dbf_directory_help = ('The directory in which the dbf table files can be found.')
    table_name_help = ('The name of the dbf table file to load.')
    cache_directory_help = ('The location on disk where the attribute cache is to be exported.')
    year_help = ('The year in which to place the exported table data in the attribute cache.')
    
    my_view = View(
        Group(
            Item('dbf_directory', help=dbf_directory_help),
            Item('table_name', help=table_name_help),
            Group(
                Item('cache_directory', help=cache_directory_help),
                Item('year', help=year_help),
                label='Attribute Cache Configuration',
                show_border=True,
                ),
            ),
            title = 'Export DBF Table to Cache',
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

    from opus_core.tools.command.export_dbf_table_to_cache_command import ExportDbfTableToCacheCommand
    
    args = GuiExportDbfTableToCache()
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)

    dbf_directory = args.dbf_directory
    if not os.path.exists(dbf_directory):
        print "ERROR: No such directory: '%s'." % dbf_directory
        sys.exit(1)
    
    table_name = args.table_name
    year = args.year
    cache_directory = args.cache_directory
    
    print ("Exporting table '%s' from '%s' to cache at '%s' in year %s..." 
        % (table_name, dbf_directory, cache_directory, year))
    
    exporter = ExportDbfTableToCacheCommand(
        dbf_directory = dbf_directory,
        table_name = table_name, 
        cache_directory = cache_directory, 
        year = year,
        )
    exporter.execute()
    
    print 'Done.'


if __name__ == '__main__':
    run_gui_export_cache_table_to_sql_server()