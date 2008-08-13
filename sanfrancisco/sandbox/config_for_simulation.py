#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from getpass import getuser
exec('from %s_simulation_config import my_configuration' % getuser())
from opus_core.configuration import Configuration

from urbansim.configs.base_config_zone import run_configuration as config

class ConfigForSimulation(Configuration):
    def __init__(self):
        Configuration.__init__(self, config)
        self.merge(my_configuration)
        if not my_configuration['creating_baseyear_cache_configuration'].cache_from_mysql:
            del self["input_configuration"] # don't bother with the database if everything is in cache