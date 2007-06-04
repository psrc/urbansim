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

from enthought.traits import Directory
from enthought.traits.ui import Item, Group, View


class BaseyearCacheConfigurationView(View):
    """
    This is the usual custom view associated with a CacheLocation.  To keep 
    the model and view separate, it's in a separate file.  Other views or 
    handlers that use it must import this explicitly.
    """
    
    existing_cache_to_copy_help = ('The root directory where the caches are normally located.')
    years_to_cache_help = ('Which years to cache.')
        
    def __init__(self, bcc):
        bcc.add_trait('existing_cache_to_copy', Directory)
        
        View.__init__(self,
            Group(
                Item('existing_cache_to_copy', help=self.existing_cache_to_copy_help),
                Group(
#                    Item('years_to_cache', help=self.years_to_cache_help),
                    orientation='horizontal',
                    ),
                layout='normal',
                )
            )


# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    import os
    
    from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
    
    
    bcc = BaseyearCacheConfiguration(
        existing_cache_to_copy = os.path.join('path', 'to', 'cache'),
        years_to_cache = BaseyearCacheConfiguration.ALL_YEARS,
        )
    
    bcc_view = BaseyearCacheConfigurationView(bcc)
    
    bcc.configure_traits(view=bcc_view)