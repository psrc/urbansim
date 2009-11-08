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

from enthought.traits import List, Instance
from enthought.traits.ui import Item, Group, View

from opus_core.configurations.editors.list_view_editor import ListViewEditor


class TableSpecificationView(View):
    """
    This is the usual custom view associated with a TableSpecification.  To keep
    the model and view separate, it's in a separate file.  Other views or 
    handlers that use it must import this explicitly.
    """
    
    table_name_help = ('The name of the table to cache.')
    copy_this_table_to_previous_years_help = ('Copy this table to previous years?')
    how_many_years_help = ('How many years back to copy the table?')
    cache_this_table_help = ('Cache this table?')
    chunks_help = ('The number of chunks in which to cache the table.')
    
    def __init__(self):
        View.__init__(self,
            Group(
                Item('cache_this_table', label='Cache', help=self.cache_this_table_help),
                '_',
                Group(
                    Item('chunks', width=-30, help=self.chunks_help),
                    '_',
                    Item('copy_this_table_to_previous_years', show_label=False, help=self.copy_this_table_to_previous_years_help),
                    enabled_when='cache_this_table',
                    orientation='horizontal',
                    show_border=False,
                    ),
                Group(    
                    Item('how_many_years', label='Back-copy this many years', width=-30, help=self.how_many_years_help),
                    enabled_when='cache_this_table and copy_this_table_to_previous_years',
                    ),
                '_',
                '10',
                Item('table_name', show_label=False, style='readonly', help=self.table_name_help),
                orientation='horizontal',
                ),
            resizable=True,
            )       

    
# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    import os
    
    from opus_core.configurations.table_specification import TableSpecification
    
    
    table_spec = TableSpecification(table_name='households')
    
    table_spec_view = TableSpecificationView()
    
    table_spec.configure_traits(view=table_spec_view)