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
import sys

from time import strftime, localtime

from enthought.traits.api import HasTraits, Directory, Str, Password, File
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from opus_core.traits_ui.api import View, Group, Item


class ExportDbfToMysqlGUI(HasTraits):
    """
    A GUI to get the parameters necessary for running the 
    do_export_dbf_to_mysql_database tool.
    """
    dbf_file_path = File
    output_database = Str
    output_table_name = Str
    host_name = Str
    user_name = Str
    password = Password

    def __init__(self):
        try: self.host_name = os.environ['MYSQLHOSTNAME']
        except: pass

        try: self.user_name = os.environ['MYSQLUSERNAME']
        except: pass

        try: self.password = os.environ['MYSQLPASSWORD']
        except: pass

    dbf_file_path_help = ("The filesystem path to the .dbf file to load.")
    output_database_help = ("The name of the MySQL database into which to "
        "write the data for this year.")
    output_table_name_help = ("The name of the table to create in the MySQL "
                         "database into which to write the data for this year.")
    host_name_help = ("The host name of the server one which the output "
        "database will be created.")
    user_name_help = ("The user name for the server on which the output "
        "database will be created.")
    password_help = ("The password for the server on which the output database will "
        "be created.")
    
    view = View(
        Group(
            Item('dbf_file_path', label='Dbf file to load', width=400, help=dbf_file_path_help),
            Group(
                Item('output_database', width=400, help=output_database_help),
                Item('output_table_name', width=400, help=output_table_name_help),
                Group(
                    Item('host_name', width=400, help=host_name_help),
                    Item('user_name', width=400, help=user_name_help),
                    Item('password', width=400, help=password_help),
                    show_border = True,
                    label='Database Connection Information',
                    ),
                show_border = True,
                label='Output Database',
                ),
            ),
        kind = 'modal',
        title = 'Export Dbf File to Mysql Database',
        ok=True, apply=False, undo=False, revert=False, help=False,
        )
    
if __name__ == '__main__':
    args = ExportDbfToMysqlGUI()
    
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)
    
    dbf_file_path = str(args.dbf_file_path)
    output_database = str(args.output_database)
    output_table_name = str(args.output_table_name)
    host_name = str(args.host_name)
    user_name = str(args.user_name)
    password= str(args.password)
    
    
    from opus_core.tools.do_export_dbf_to_mysql_database import __file__ as script_path
    
    ev = ('%s %s %s'
        % (sys.executable, script_path, '-c %s -d %s --table-name=%s -o %s -u %s -p %s' 
            % (dbf_file_path, output_database, output_table_name, host_name, user_name, password)))
        
    print "Invoking command: %s" % ev
    os.system(ev)