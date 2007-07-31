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

from enthought.traits.api import Event
from opus_core.traits_ui.api import Item, Group, View, ButtonEditor
# later update the ui import to:   from enthought.traits.ui.api import Item, Group, View, ButtonEditor


class CacheLocationView(View):
    """
    This is the usual custom view associated with a CacheLocation.  To keep 
    the model and view separate, it's in a separate file.  Other views or 
    handlers that use it must import this explicitly.
    """
    
    root_help = ('The root directory where the caches are normally located.')
    dir_help = ('The subdirectory in the cache directory root where the cache is '
        'located. ')
    
    def __init__(self, cache_loc):
        cache_loc.add_trait('use_standard_template_for_cache_directory', Event(editor=ButtonEditor()))
        
        View.__init__(self,
            Group(
                Item('cache_directory_root', help=self.root_help),
                '5',
                Item('cache_directory', help=self.dir_help),
                Item('use_standard_template_for_cache_directory', enabled_when='not(cache_directory==_default_cache_directory)', show_label=False),
                layout='normal',
                )
            )
    
# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    import os
    
    from opus_core.configurations.cache_location import CacheLocation
    
    
    cache_loc = CacheLocation(
        cache_directory_root = os.path.join('path', 'to', 'cache', 'root'),
        )
    
    cache_loc_view = CacheLocationView(cache_loc)
    
    cache_loc.configure_traits(view=cache_loc_view)