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

from enthought.traits.api import HasTraits, Directory, Str, Int
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from opus_core.traits_ui.api import View, Group, Item
from enthought.traits.ui.menu import CloseAction

class GuiExportDbfTableToCache(HasTraits):
    dbf_directory = Directory
    table_name = Str
    cache_directory = Directory
    year = Int
    decimalcount = Int(4)
    
    dbf_directory_help = ('The directory in which the dbf table files can be found.')
    table_name_help = ('The name of the dbf table file to write to.')
    cache_directory_help = ('The location on disk where the attribute cache is.')
    year_help = ('The year from which to import table data from the attribute cache.')
    decimalcount_help = ("""
        The number of digits right of the decimal point. The number of 
        all digits including the sign and the decimal point 
        have to be equal or less than 18
        """
        )
    
    my_view = View(
        Group(
            Group(
                Item('cache_directory', help=cache_directory_help),
                Item('year', help=year_help),
                label='Attribute Cache Configuration',
                show_border=True,
                ),
            ),
            Item('table_name', help=table_name_help),
            Item('dbf_directory', help=dbf_directory_help),
            Item('decimalcount', help=decimalcount_help),
            title = 'Export Cache to DBF Table',
            width = 500,
            ok = True, cancel = True, apply = False, revert = False, undo = False, help = False,
            kind = 'modal',
        )

class MessageDialog(HasTraits):
    message = Str
    title = Str
    width = Int(300)
    height = Int(200)
    
    def get_view(self):
        return View(
            Group(
                  Item('message', style='custom', width=self.width, height=self.height),
                  show_labels=False,
                  ),
            buttons=[CloseAction],
            title=self.title,
            )

       
def run_gui_export_cache_table_to_sql_server():
    """
    Collect the parameters from the user.
    """
    import os
    import sys

    from opus_core.tools.command.export_cache_to_dbf_table_command import ExportCacheToDbfTableCommand
    
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
    decimalcount = args.decimalcount
    
    print ("Exporting table '%s' to '%s' from cache at '%s' in year %s..." 
        % (table_name, dbf_directory, cache_directory, year))
    
    exporter = ExportCacheToDbfTableCommand(
        dbf_directory = dbf_directory,
        table_name = table_name, 
        cache_directory = cache_directory, 
        year = year,
        decimalcount = decimalcount
        )
    short_names = exporter.execute()
    
    name_changed = False
    for key in short_names.keys():
        name_changed = name_changed or short_names[key]==key
        
    message = ''
    if name_changed:
        message += "One or more attribute name changed:\n"
        message += "(You can open an editor, e.g. Excel, and change the attribute names.)\n\n"
        for key in short_names.keys():
            if short_names[key] is not key:
                message += '%s => %s\n' % (key, short_names[key])
        
        dia = MessageDialog(title='Changed Attribute Names', message=message)
        dia.configure_traits(view=dia.get_view())  
    
    print 'Done.'


if __name__ == '__main__':
    run_gui_export_cache_table_to_sql_server()