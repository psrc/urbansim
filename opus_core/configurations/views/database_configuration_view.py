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

# later update the ui import to:   from enthought.traits.ui.api import Item, Group, View
from enthought.traits.api import Item, Group, View


class DatabaseConfigurationView(View):
    # This is the usual custom view associated with a DatabaseConfiguration.  To keep the model
    # and view separate, it's in a separate file.  Other views or handlers that use it must import
    # this explicitly.
    
    env_var_help = ('If checked, use the values of the system environment '
        'variables MYSQLHOSTNAME, MYSQLUSERNAME, or MYSQLPASSWORD; otherwise '
        'use the values entered by the user.')
    
    def __init__(self):
        View.__init__(self,
            Group(
                # Database Name Section
                Group('database_name', show_border=True),
                
                Group( # Host Name Section
                    Group('50',Item('use_environment_variable_for_host_name',help=self.env_var_help), orientation='horizontal'),
                    Item('host_name', enabled_when='not(use_environment_variable_for_host_name)'),
                    show_border=True
                    ),
                    
                Group( # User Name Section
                    Group('50', Item('use_environment_variable_for_user_name', help=self.env_var_help), orientation='horizontal'),
                    Item('user_name', enabled_when='not(use_environment_variable_for_user_name)'),
                    show_border=True
                    ),
                    
                Group( # Password Section
                    Group('50', Item('use_environment_variable_for_password', help=self.env_var_help), orientation='horizontal'),
                    Item('password', enabled_when='not(use_environment_variable_for_password)'),
                    show_border=True
                    ),
                    
                layout='normal'
                )
            )
            
            
# This is just a sample to demonstrate the view.
if __name__ == '__main__':
    from opus_core.configurations.database_configuration import DatabaseConfiguration
    
    db_conf = DatabaseConfiguration(database_name = 'database_name')
    
    db_conf_view = DatabaseConfigurationView()
    
    db_conf.configure_traits(view=db_conf_view)