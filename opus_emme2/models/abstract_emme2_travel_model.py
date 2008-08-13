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

import os
from opus_core.model import Model

class AbstractEmme2TravelModel(Model):
    """Basic functionality used by all of the emme/2 models.
    Must be subclassed before use.
    """
    def __init__(self, config):
        self.config = config
        self.emme_cmd = config['travel_model_configuration'].get('emme_command', 'emme -ng --set-iks 127.0.0.1')
        
    def get_emme2_dir(self, year, subdir=None):
        """Returns the full path to the given subdirectory of the emme/2 'database'.
        """
        year_config = self.config['travel_model_configuration'][year]
        bank_path_parts = year_config['bank']
        path = os.path.sep.join(bank_path_parts)
        path = os.path.join(os.environ['TRAVELMODELROOT'], path)
        if subdir <> None:
            path = os.path.join(path, subdir)
        return path
    
    def get_emme2_base_dir(self):
        return os.path.join(os.environ['TRAVELMODELROOT'], self.config['travel_model_configuration']['travel_model_base_directory'])
    
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
                            'baseline_travel_model_psrc',
                            '2000_06',
                            ],
                        'emme2_batch_file_name':'MODEL05g.bat',
                        },
                    }, 
                }
            m = AbstractEmme2TravelModel(config)
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2000_06')
            self.assertEqual(m.get_emme2_dir(2001), path)
            path = os.path.join(os.environ['TRAVELMODELROOT'], 'baseline_travel_model_psrc', '2000_06', 'tripgen')
            self.assertEqual(m.get_emme2_dir(2001, 'tripgen'), path)
        
if __name__ == '__main__':
    opus_unittest.main()

        
