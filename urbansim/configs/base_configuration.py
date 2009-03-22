# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.cache_baseyear_configuration import CacheBaseyearConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration

# This configuration contains all of the informaiton needed for the code
# to know how to process the desired range of development projects.
# This should be globally accessible, so that models and datasets
# can know what flavors of development projects exist.

class AbstractUrbansimConfiguration(GeneralConfiguration):
    """Specifies the common set of configuration values for use by an UrbanSim model system.
    
    Additional configuration information must be provided before running, 
    such as which database name to use for the inputs."""
    def __init__(self):
        config_changes = self._get_initial_config()
        self.merge(config_changes)
    
    def _get_initial_config(self):
        """Encapsulate dirty inner workings"""
        config = GeneralConfiguration()
        caching_config = CacheBaseyearConfiguration()
        config.merge(caching_config)
        return config


from opus_core.tests import opus_unittest
class AbstractUrbansimConfigurationTests(opus_unittest.OpusTestCase):
    def test(self):
        config = AbstractUrbansimConfiguration()
        self.assert_('models' in config)
        self.assert_('scenario_database_configuration' not in config)
        self.assert_('estimation_database_configuration' not in config)
        self.assert_('creating_baseyear_cache_configuration' in config)
    
    
if __name__ == '__main__':
    opus_unittest.main()