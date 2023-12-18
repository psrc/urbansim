# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
class AbstractEmme4TravelModel(AbstractEmme2TravelModel):
    """Setting various paths for emme4"""
    
    def get_emme2_base_dir(self):
        root = os.environ.get('TRAVELMODELROOT', '')
        return os.path.join(root, self.config['travel_model_configuration']['travel_model_base_directory'])
        
    def get_emme2_dir(self, year, subdir=None):
        """Returns the full path to the given subdirectory of the emme/2 'database'.
        """
        year_config = self.config['travel_model_configuration'][year]
        bank_path_parts = year_config['bank']  # a list by path parts
        bank_path = os.path.sep.join(bank_path_parts)
        path = os.path.join(self.get_emme2_base_dir(),  "inputs",  "tripgen", bank_path)
        if subdir != None:
            path = os.path.join(path, subdir)
        return path
    
    def get_emme2_batch_file_path(self, year):
        """Path to the batch file.
        """
        emme2_batch_file_name = self.config['travel_model_configuration'][year].get('emme2_batch_file_name', None)
        if emme2_batch_file_name is None or len(emme2_batch_file_name) == 0:
            emme2_batch_file_name = self.config['travel_model_configuration'].get('emme2_batch_file_name')
        path = os.path.join(self.get_emme2_base_dir(), "src", emme2_batch_file_name)
        return path

        
from opus_core.tests import opus_unittest
class AbstractEmme2TravelModelTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self._has_travel_model = 'TRAVELMODELROOT' in os.environ

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
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', 'inputs', '2000_06')
            self.assertEqual(m.get_emme2_dir(2001), path)
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', 'inputs', '2000_06', 'tripgen')
            self.assertEqual(m.get_emme2_dir(2001, 'tripgen'), path)
            batch_file = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', 'src', 'MODEL05g.bat')
            self.assertEqual(m.get_emme2_batch_file_path(2001), batch_file)
            batch_file = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', 'src', 'MODEL06g.bat')
            self.assertEqual(m.get_emme2_batch_file_path(2005), batch_file)
        
if __name__ == '__main__':
    opus_unittest.main()

        
