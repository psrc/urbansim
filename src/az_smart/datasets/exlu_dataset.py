#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.datasets.dataset import Dataset

class ExluDataset(Dataset):
    pass


from opus_core.tests import opus_unittest

from numpy import array

from opus_core.storage_factory import StorageFactory


class TestExluDataset(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_exlu(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name = 'exlu',
            table_data = {
                'id': array([1]),
                }
            )
        
        ExluDataset(in_table_name='exlu', id_name='id', in_storage=storage)
        
        
if __name__ == '__main__':
    opus_unittest.main()