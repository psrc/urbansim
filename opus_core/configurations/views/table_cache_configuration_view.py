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

from enthought.traits.api import List, Instance
# later update the ui import to:   from enthought.traits.ui.api import Item, Group, View
from opus_core.traits_ui.api import Item, Group, View

from opus_core.configurations.table_specification import TableSpecification
from opus_core.configurations.editors.list_view_editor import ListViewEditor
from opus_core.configurations.views.table_specification_view import TableSpecificationView


class TableCacheConfigurationView(View):
    """
    This is the usual custom view associated with a 
    TablesCacheConfigurationView.  To keep the model and view separate, 
    it's in a separate file.  Other views or handlers that use it must import 
    this explicitly.
    """
    
    table_cache_configuration_help = ('A list of TableSpecifications.')
    
    def __init__(self, table_cache_configuration):
        table_cache_configuration.add_trait('_table_specifications', 
            List(
                Instance(TableSpecification), 
                editor=ListViewEditor(view=TableSpecificationView(), name='_table_specifications')
                )
            )
        
        View.__init__(self,
            Group(
                Item('_table_specifications', resizable=True, show_label=False, height=150, help=self.table_cache_configuration_help),
                ),
                resizable=True,
            )       

    
# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    import os
    
    from opus_core.configurations.table_cache_configuration import TableCacheConfiguration
    
    
    table_cache_configuration = TableCacheConfiguration(
        table_specifications = 
            [TableSpecification(table_name='table%s'%i, chunks=i) for i in range(1,101)]
        )
    
    table_cache_configuration_view = TableCacheConfigurationView(table_cache_configuration)
    
    table_cache_configuration.configure_traits(view=table_cache_configuration_view)