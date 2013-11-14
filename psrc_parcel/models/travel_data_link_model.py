from numpy import array
from opus_core.model import Model
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.travel_data_link_dataset import TravelDataLinkDataset
from opus_core.logger import logger

class TravelDataLinkModel(Model):
    """ Creates a TravelDataLink dataset which has a pointer to skims in hdf5 format.
    """
    model_name = "Travel Data Link Model"
          
    def run(self, directory, dataset_pool=None):
        """ Create a TravelDataLink dataset that points to 'directory' which should contain 
            travel data skims in hdf5 format.
        """
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'travel_data_link',
                            table_data = {'travel_data_link_id': array([1]),
                                          'data_link': array([directory])})       
        link_dataset = TravelDataLinkDataset(in_storage = storage, 
                           in_table_name='travel_data_link')
        if dataset_pool is not None:
            dataset_pool._add_dataset('travel_data_link', link_dataset)
        return link_dataset
        
import os
from glob import glob
from opus_core.tests import opus_unittest
from numpy import array, ma, allclose
import h5py
from shutil import rmtree
from tempfile import mkdtemp

class Test(opus_unittest.OpusTestCase):
    def setUp(self):
        self.distance = array([[0, 3, 5],
                          [4, 0, 10],
                          [6, 12, 0]])
        self.time5to6 = array([[1, 30.6, 50.3],
                          [40.9, 1, 108],
                          [66.4, 121, 1]])
        self.time6to7 = self.time5to6 + 6
        self.temp_dir = mkdtemp(prefix='urbansim_test_travel_data_h5')
        f = h5py.File(os.path.join(self.temp_dir, "5to6.h5"), "w")
        group = f.create_group("Skims")
        group.create_dataset("distance", data=self.distance)
        group.create_dataset("time", data=self.time5to6)
        f.close()
        f = h5py.File(os.path.join(self.temp_dir, "6to7.h5"), "a")
        group = f.create_group("Skims")
        group.create_dataset("distance", data=self.distance)
        group.create_dataset("time", data=self.time6to7)
        f.close()      
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)  
              
    def test_travel_data_link_model(self):
        model = TravelDataLinkModel()
        link_dataset = model.run(self.temp_dir)
        self.assertEqual(link_dataset.size(), 1, msg = "Dataset size should be 1 but is %s" % link_dataset.size())
        
        travel_data = link_dataset.skim_dataset
        self.assertEqual(travel_data.size(), 3, msg = "Skim size should be 3 but is %s" % travel_data.size())
        
        k = len(travel_data.get_attribute_names())
        self.assertEqual(k, 2, msg = "Number of attributes should be 2 but is " + str(k) + ".")
        
        k = len(travel_data.get_primary_attribute_names())
        self.assertEqual(k, 2, msg = "Number of stored attributes should be 2 but is " + str(k) + ".")

if __name__=="__main__":
    opus_unittest.main()        