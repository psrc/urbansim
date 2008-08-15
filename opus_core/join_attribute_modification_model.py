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

from numpy import array, arange, setmember1d, where
from opus_core.model import Model
from opus_core.misc import ismember
from opus_core.logger import logger

class JoinAttributeModificationModel(Model):
    """ The model modifies a dataset's attribute given by the id name of a second dataset.
    """
    def run(self, dataset, secondary_dataset, index=None, attribute_to_be_modified=None, value=0):
        """
        'dataset' must contain an attribute of the same name as the id attribute of the secondary_dataset (join_attribute).
        The model finds members of 'dataset' for which the values of the join_attribute correspond to values of that attribute 
        of the secondary_dataset (possibly restricted by the 'index'). For all those members is the attribute
        'attribute_to_be_modified' changed to 'value'. If 'attribute_to_be_modified' is not given,
        the 'join_attribute' is modified.
        """
        
        if index is None:
            index = arange(secondary_dataset.size())
            
        ids = secondary_dataset.get_id_attribute()[index]
        join_attribute = secondary_dataset.get_id_name()[0]
        members_idx = where(ismember(dataset.get_attribute(join_attribute), ids))[0]
        if attribute_to_be_modified is None:
            attribute_to_be_modified = join_attribute
        dataset.modify_attribute(name=attribute_to_be_modified, data=array(index.size*[value]), index=members_idx)
        logger.log_status("%s values of %s.%s are set to %s." % (members_idx.size, dataset.get_dataset_name(), attribute_to_be_modified, value))
        
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_no_change(self):
        """No common values in the join_attribute, therefore no change."""
        data = {
           'my_id': array([1,2,3,4]),
           'attr':  array([10,20,30,50])     
                }
        data2 = {
            'attr': array([2,6,7,3])
                 }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset', table_data=data)
        dataset = Dataset(in_storage = storage, 
                           in_table_name='dataset',
                           id_name='my_id'
                           )
        storage.write_table(table_name='dataset2', table_data=data2)
        dataset2 = Dataset(in_storage = storage, 
                           in_table_name='dataset2',
                           id_name='attr'
                           )
        JoinAttributeModificationModel().run(dataset,dataset2)
        self.assertEqual(ma.allequal(dataset.get_attribute('attr'), data['attr']), True)
        
    def test_change_three_elements(self):
        """3 values are in common - change them to -1. Other attributes stay unchanged."""
        data = {
           'my_id': array([1,2,3,4,5]),
           'attr':  array([10,2,3,50,2]),
           'attr2': array([4,3,2,5,3])    
                }
        data2 = {
            'attr': array([2,6,7,3])
                 }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset', table_data=data)
        dataset = Dataset(in_storage = storage, 
                           in_table_name='dataset',
                           id_name='my_id'
                           )
        storage.write_table(table_name='dataset2', table_data=data2)
        dataset2 = Dataset(in_storage = storage, 
                           in_table_name='dataset2',
                           id_name='attr'
                           )
        JoinAttributeModificationModel().run(dataset,dataset2, value=-1)
        self.assertEqual(ma.allequal(dataset.get_attribute('attr'), array([10,-1,-1,50,-1])), True)
        self.assertEqual(ma.allequal(dataset.get_attribute('attr2'), data['attr2']), True)
        
    def test_change_with_index(self):
        """The secondary dataset is restricted by index."""
        data = {
           'my_id': array([1,2,3,4,5,6]),
           'attr':  array([10,20,30,50,46,100]),
           'attr2': array(6*[1])
                }
        data2 = {
            'attr': array([20, 6, 7, 3, 10, 30, 100, 50])
                 }
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset', table_data=data)
        dataset = Dataset(in_storage = storage, 
                           in_table_name='dataset',
                           id_name='my_id'
                           )
        storage.write_table(table_name='dataset2', table_data=data2)
        dataset2 = Dataset(in_storage = storage, 
                           in_table_name='dataset2',
                           id_name='attr'
                           )
        JoinAttributeModificationModel().run(dataset,dataset2, index=array([0,1,2,7]), attribute_to_be_modified='attr2')
        self.assertEqual(ma.allequal(dataset.get_attribute('attr2'), array([1, 0, 1, 0, 1, 1])), True)
        
if __name__=='__main__':
    opus_unittest.main()