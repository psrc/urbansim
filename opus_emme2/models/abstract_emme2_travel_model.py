# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.model import Model

class AbstractEmme2TravelModel(Model):
    """Basic functionality used by all of the emme/2 models.
    Must be subclassed before use.
    """
    def __init__(self, config):
        self.config = config
        self.emme_cmd = config['travel_model_configuration'].get('emme_command', 'emme -ng --set-iks 127.0.0.1')

    def get_emme2_base_dir(self):
        root = os.environ.get('TRAVELMODELROOT', '')
        return os.path.join(root, self.config['travel_model_configuration']['travel_model_base_directory'])
        
    def get_emme2_dir(self, year, subdir=None):
        """Returns the full path to the given subdirectory of the emme/2 'database'.
        """
        year_config = self.config['travel_model_configuration'][year]
        bank_path_parts = year_config['bank']  # a list by path parts
        bank_path = os.path.sep.join(bank_path_parts)
        path = os.path.join(self.get_emme2_base_dir(), bank_path)
        if subdir <> None:
            path = os.path.join(path, subdir)
        return path
    
    def get_emme2_batch_file_path(self, year):
        """Returns the full path to emme2_batch_file_name for the specified year in the emme/2 'database'.
        emme2_batch_file is in the directory returned by self.get_emme2_dir()
        """
        emme2_batch_file_name = self.config['travel_model_configuration'][year].get('emme2_batch_file_name', None)
        if emme2_batch_file_name is None or len(emme2_batch_file_name) == 0:
            emme2_batch_file_name = self.config['travel_model_configuration'].get('emme2_batch_file_name')
        path = os.path.join(self.get_emme2_dir(year), emme2_batch_file_name)
        return path
        
from opus_core.tests import opus_unittest
class AbstractEmme2TravelModelTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self._has_travel_model = os.environ.has_key('TRAVELMODELROOT')

    def test_get_emme2_dir(self):
        if self._has_travel_model:
            config = {
                'travel_model_configuration':{
                    2001:{
                        'bank':[
                            '2000_06',
                            ],
                        },
                    2005:{
                        'bank':[
                            '2005_06',
                            ],
                        'emme2_batch_file_name':'MODEL06g.bat',                        
                        },                    
                    'travel_model_base_directory':'baseline_travel_model_psrc',
                    'emme2_batch_file_name':'MODEL05g.bat',
                    }, 
                }
            m = AbstractEmme2TravelModel(config)
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2000_06')
            self.assertEqual(m.get_emme2_dir(2001), path)
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2000_06', 'tripgen')
            self.assertEqual(m.get_emme2_dir(2001, 'tripgen'), path)
            batch_file = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2000_06', 'MODEL05g.bat')
            self.assertEqual(m.get_emme2_batch_file_path(2001), batch_file)
            batch_file = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2005_06', 'MODEL06g.bat')
            self.assertEqual(m.get_emme2_batch_file_path(2005), batch_file)
        
if __name__ == '__main__':
    opus_unittest.main()

        
