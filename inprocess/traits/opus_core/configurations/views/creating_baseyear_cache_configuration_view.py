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

from enthought.traits.api import Event, Bool
# later update the ui import to:   from enthought.traits.ui.api import ButtonEditor, EnumEditor, Item, Group, View
from opus_core.traits_ui.api import ButtonEditor, EnumEditor, Item, Group, View

from opus_core.configurations.views.cache_location_view import CacheLocationView
from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.views.database_configuration_view import DatabaseConfigurationView
from opus_core.configurations.views.baseyear_cache_configuration_view import BaseyearCacheConfigurationView
from opus_core.configurations.views.table_cache_configuration_view import TableCacheConfigurationView

class CreatingBaseyearCacheConfigurationView(View):
    """
    This is the usual custom view associated with a 
    CreatingBaseyearCacheConfiguration.  To keep the model and view separate, 
    it's in a separate file.  Other views or handlers that use it must import 
    this explicitly.
    """
    
    cache_mysql_help = ('')
    cache_location_help =  ('')
    cache_from_mysql_help = ('')
    input_configuration_help = ('')
    baseyear_cache_help = ('')
    tables_to_cache_help = ('')
    tables_to_cache_nchunks_help = ('')
    tables_to_copy_to_previous_years_help = ('')
    
    def __init__(self, cbcc):
                
        cbcc.cache_location.trait_view('trait_view', CacheLocationView(cbcc.cache_location))
        
        cbcc.baseyear_cache.trait_view('trait_view', BaseyearCacheConfigurationView(cbcc.baseyear_cache))
        
        cbcc.input_configuration.trait_view('trait_view', DatabaseConfigurationView())

        cbcc.table_cache_configuration.trait_view('trait_view',
            TableCacheConfigurationView(cbcc.table_cache_configuration))
            
        cbcc.add_trait('load_table_specifications_from_input_source', Event(editor=ButtonEditor()))
        cbcc.add_trait('_cache_scenario_database', Bool)
        
        if cbcc.cache_scenario_database == 'opus_core.cache.cache_scenario_database':
            cbcc._cache_scenario_database = False
        else:
            cbcc._cache_scenario_database = True
        
        def on_cache_scenario_database(event):
            if event is False:
                cbcc.cache_scenario_database = 'opus_core.cache.cache_scenario_database'
            else:
                cbcc.cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database'
            
        cbcc.on_trait_event(on_cache_scenario_database, '_cache_scenario_database')
                    
        View.__init__(self,
            Group(
                Group(
                    Item('cache_location', show_label=False, style='custom', help=self.cache_location_help),
                    label='Cache location',
                    ),
                Group(
                    Group('50', Item('cache_from_mysql', label='Remote input source', style='custom', help=self.cache_from_mysql_help), orientation='horizontal'),
                    Group(
                        Group('50',
                            Item('_cache_scenario_database', label='Unroll gridcells', show_label=True, help=self.cache_mysql_help),
                            orientation='horizontal',
                            ),
                        Item('input_configuration', style='custom', help=self.input_configuration_help),
                        label='Remote input source:',
                        show_labels=False,
                        enabled_when='cache_from_mysql',
                        show_border=True,
                        ),
                    Group(
                        Item('baseyear_cache', style='custom', help=self.baseyear_cache_help), 
                        enabled_when='not(cache_from_mysql)',
                        label='Local file-system input source:',
                        show_labels=False,
                        show_border=True,
                        ),
                    label='Input source',
                    ),
                Group(
                    Item('load_table_specifications_from_input_source', show_label=False),
                    Item('table_cache_configuration', style='custom', show_label=False, resizable=True, height=300),
                    label='Table cache configuration',
                    ),
                layout='tabbed',
                ),
            width=800,
            resizable=True,
            )
    
    
# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    import os
    
    from opus_core.configurations.cache_location import CacheLocation
    from opus_core.configurations.table_specification import TableSpecification
    from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
    from opus_core.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
    from opus_core.configurations.table_cache_configuration import TableCacheConfiguration
    
    
    cbcc = CreatingBaseyearCacheConfiguration(
        cache_scenario_database = 'opus_core.cache.cache_scenario_database',
        cache_from_mysql = True,
        cache_location = CacheLocation(
            cache_directory_root = os.path.join('path', 'to', 'cache', 'root'),
            ),
        input_configuration=DatabaseConfiguration(database_name=''),
        table_cache_configuration = TableCacheConfiguration([])
        )
    cbcc.load_table_specifications_from_input_source = True # Trigger event
    
    cbcc_view = CreatingBaseyearCacheConfigurationView(cbcc)
    
    cbcc.configure_traits(view=cbcc_view)