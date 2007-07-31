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

from enthought.traits.api import HasTraits, Directory
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from opus_core.traits_ui.api import View, Group, Item


class ExportTabConfig(HasTraits):
    cache_path = Directory
    output_directory = Directory

    cache_path_help = ("The filesystem path to the year directory in the cache "
        "of the data to export, "
        r"e.g. 'C:\urbansim_cache\%s\1980'." 
        % strftime('%Y_%m_%d_%H_%M',localtime()))
    output_directory_help = ("The filesystem path to the directory into which "
        "to write the csv files for the data in this year.")
    
    view = View(
        Group(
            Item('cache_path', label='Directory of cached year', width=400, help=cache_path_help),
            Item('output_directory', width=400, help=output_directory_help),
            ),
        kind = 'modal',
        title = 'Export UrbanSim Baseyear Cache to Tab Delimited Files',
        ok=True, apply=False, undo=False, revert=False, help=False,
        )
    
if __name__ == '__main__':
    args = ExportTabConfig()
    
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)
    
    cache_dir = str(args.cache_path)
    output_dir = str(args.output_directory)
    
    
    from opus_core.tools.do_export_cache_to_tab_delimited_files import __file__ as script_path
    
    ev = ('%s %s %s'
        % (sys.executable, script_path, '-c %s -o %s' % (cache_dir, output_dir)))
        
    print "Invoking command: %s" % ev
    os.system(ev)