# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from getpass import getuser
exec('from %s_simulation_config import my_configuration' % getuser(), globals())
from opus_core.configuration import Configuration

from urbansim.configs.base_config_zone import run_configuration as config

class ConfigForSimulation(Configuration):
    def __init__(self):
        Configuration.__init__(self, config)
        self.merge(my_configuration)
        if not my_configuration['creating_baseyear_cache_configuration'].cache_from_database:
            del self["input_configuration"] # don't bother with the database if everything is in cache