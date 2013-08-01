# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.model import Model

class AbstractDaysimTravelModel(Model):
    """Basic functionality used by all of the opus_daysim models.
    Must be subclassed before use.
    """
    def __init__(self, config):
        self.config = config

    def get_daysim_base_dir(self):
        return self.config['travel_model_configuration']['daysim_base_directory']
        
    def get_daysim_dir(self, year):
        """Returns the full path to the given subdirectory of the daysim data.
        """
        year_config = self.config['travel_model_configuration'][year]
        return os.path.join(self.get_daysim_base_dir(), year_config['daysim_exchange_dir'])
    
    def get_daysim_skim_dir(self, year):
        """Returns the full path to the given subdirectory of the daysim skim data.
        """
        year_config = self.config['travel_model_configuration'][year]
        return os.path.join(self.get_daysim_base_dir(), year_config['daysim_skim_dir'])

    def get_daysim_config_file(self, year):
        """Returns the full path to the config file for the specified year.
        """
        config_file_name = self.config['travel_model_configuration'][year].get('daysim_config_file', None)
        if config_file_name is None or len(config_file_name) == 0:
            config_file_name = self.config['travel_model_configuration'].get('daysim_config_file')
        path = os.path.join(self.get_daysim_dir(year), config_file_name)
        return path
    
        
from opus_core.tests import opus_unittest
class AbstractDaysimTravelModelTests(opus_unittest.OpusTestCase):

    def test_get_daysim_dir(self):
        config = {
            'travel_model_configuration':{
                2001:{
                    'daysim_exchange_dir': 'daysim_2001'
                    },
                2005:{
                    'daysim_exchange_dir': 'daysim_2005'                      
                    },                    
                'daysim_base_directory':'/homes/user/daysim',
                }, 
            }
        m = AbstractDaysimTravelModel(config)
        path = os.path.join('/homes/user/daysim', 'daysim_2001')
        self.assertEqual(m.get_daysim_dir(2001), path)
        self.assertEqual(m.get_daysim_dir(2005), os.path.join('/homes/user/daysim', 'daysim_2005'))
        
if __name__ == '__main__':
    opus_unittest.main()

        
