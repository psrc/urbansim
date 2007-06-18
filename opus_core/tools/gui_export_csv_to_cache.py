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

from enthought.traits.api import HasTraits, Directory, Int, Str, File
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from enthought.traits.api import View, Group, Item


class ExportCSVToCacheGUI(HasTraits):
    """
    A GUI to get the parameters necessary for running the 
    do_export_csv_to_cache tool.
    """
    csv_file_path = File
    output_year = Int
    output_cache_directory = Directory

    csv_file_path_help = ("The filesystem path to the .csv file to load.")
    output_cache_directory_help = ("The filesystem directory path into which "
        "the cache will be written.")
    output_year_help = ("The year under which the data will be stored in the cache.")
    
    view = View(
        Group(
            Item('csv_file_path', label='CSV file to load', width=400, help=csv_file_path_help),
            Item('output_cache_directory', width=400, help=output_cache_directory_help),
            Item('output_year', width=50, help=output_year_help),
            ),
        kind = 'modal',
        title = 'Export CSV File to Cache',
        ok=True, apply=False, undo=False, revert=False, help=False,
        )
    
if __name__ == '__main__':
    args = ExportCSVToCacheGUI()
    
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)
    
    csv_file_path = str(args.csv_file_path)
    output_cache_directory = str(args.output_cache_directory)
    output_year = args.output_year
    
    if csv_file_path == '':
        print 'The CSV file path is required.'
        sys.exit(1)
        
    if (not os.path.exists(csv_file_path) or not os.path.isfile(csv_file_path)
            or not csv_file_path.endswith('.csv')):
        print 'Invalid CSV file: %s' % csv_file_path
        sys.exit(1)
    
    csv_directory, csv_filename = os.path.split(csv_file_path)
    table_name = csv_filename[:-len('.csv')]
        
    if output_cache_directory == '':
        print 'The output cache directory is required.'
        sys.exit(1)
    
    
    from opus_core.tools.do_export_csv_to_cache import __file__ as script_path
    
    ev = ('python %s %s' % (
              script_path, 
              ('--csv_directory=%s '
              '--attribute_cache_directory=%s '
              '--table_name=%s '
              '--cache_year=%s') % (
                  csv_directory, 
                  output_cache_directory, 
                  table_name,
                  output_year
                  )
              )
          )
        
    print "Invoking command: %s" % ev
    os.system(ev)