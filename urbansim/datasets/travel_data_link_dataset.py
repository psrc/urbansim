# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from glob import glob
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.logger import logger
from numpy import arange, where, logical_and

class TravelDataLinkDataset(UrbansimDataset):
    """This dataset has only one required attribute called 'data_link' which is 
        a path to travel model skims in hdf5 format. It creates 
        a TravelDataH5SkimDataset dataset which knows how to read the skims.
    """
    id_name_default = ['travel_data_link_id']
    in_table_name_default = "travel_data_link"
    out_table_name_default = "travel_data_link"
    dataset_name = "travel_data_link"
    
    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        if 'data_link' not in self.get_known_attribute_names():
            raise StandardError, 'Attribute "data_link" must be included in TravelDataLinkDataset'
        path_to_h5 = self.get_attribute('data_link')
        self.skim_dataset = TravelDataH5SkimDataset(path_to_h5[0])
        
    def get_skim_dataset(self):
        return self.skim_dataset
        
class TravelDataH5SkimDataset(UrbansimDataset):
    """Read-only travel data containing skims stored in hdf5 files.
        Each time period is stored in a separate file, e.g. 5to6.h5.
        Each file contains a group called 'Skims' with each skim being 
        a 2d array. 
    """

    dataset_name = "travel_data_h5_skim"
    
    def __init__(self, path):
        self.base_directory = path
        if not os.path.exists(self.base_directory):
            raise StandardError("Directory '%s' does not exist!" % self.base_directory)
        self.time_skims = self._get_skim_files()
        self.time_array = array(map(lambda x: x.replace('.h5', '').split('to'), self.time_skims)).astype('int32')
        file_name = os.path.join(self.base_directory, self.time_skims[0])
        f = h5py.File(file_name, "r")
        self._attribute_names = f["Skims"].keys()
        self._primary_attribute_names = self._attribute_names
        self.n = f["Skims"][self._attribute_names[0]].shape[0]
        f.close()
        
    def _get_skim_files(self):
        files = glob(os.path.join(self.base_directory, '*.h5'))
        # return short names
        return array(map(lambda x: os.path.split(x)[1], files))
        
    def get_attribute_names(self):
        return self._attribute_names
      
    def size(self):
        return self.n
      
    def _load_skim(self, name, time):
        file_name = os.path.join(self.base_directory, self.time_skims[time])
        if not os.path.exists(file_name):
            logger.log_warning('Skim file %s does not exist.' % file_name)
            return None
        f = h5py.File(file_name, "r")
        result = f['Skims'][name][...]
        f.close()
        return result 

    def _get_time_index(self, from_time, to_time):
        return where(logical_and(self.time_array[:,0] >= from_time, self.time_array[:,1] <= to_time))[0]
    
    def get_attribute(self, name, from_zone=None, to_zone=None, from_time=5, to_time=24):
        """Return a 1d array of values from the skim called "name". 
            The length of from_zone and to_zone must match.
            If more than one time periods are selected (using from_time, to_time, 
            e.g. from_time=5, to_time=14), the skims are averaged over the given time periods.
        """
        return self._get_attribute(name, as_matrix=False, from_zone=from_zone, to_zone=to_zone, 
                              from_time=from_time, to_time=to_time)
        
    def get_attribute_as_matrix(self, name, from_zone=None, to_zone=None, from_time=5, to_time=24):
        """Return a 2d array. All values of "to_zone" are used for each element of "from_zone".
            If more than one time periods are selected (using from_time, to_time, 
            e.g. from_time=5, to_time=14), the skims are averaged over the given time periods.
        """
        return self._get_attribute(name, as_matrix=True, from_zone=from_zone, to_zone=to_zone, 
                              from_time=from_time, to_time=to_time)
    
    def _get_attribute(self, name, as_matrix=False, from_zone=None, to_zone=None, from_time=5, to_time=24):
        """return attribute "name" of travel_data as a 2d array, index by (from_zone_id, to_zone_id)
        """
        result = None
        time_index = self._get_time_index(from_time, to_time)
        ltime = time_index.size
        nerr = 0
        for i in time_index:
            data = self._load_skim(name, i)
            if data is None:
                nerr = nerr + 1
                continue
            if from_zone is None:
                from_zone=arange(data.shape[0])+1
            if to_zone is None:
                to_zone=arange(data.shape[1])+1
            if as_matrix:
                this_result = data[from_zone-1, :]
                this_result = this_result[:,to_zone-1]
            else:
                this_result = data[from_zone-1, to_zone-1]
   
            if result is None:
                result = this_result
            else:
                result = result + this_result
        if (ltime - nerr) == 0:
            raise StandardError, 'No data available.' 
        result = result/float(ltime-nerr)        
        return result



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
        self.travel_data = TravelDataH5SkimDataset(self.temp_dir)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)  
              
    def test_travel_data(self):
        
        self.assertEqual(self.travel_data.size(), 3, msg = "Data size should be 3 but is %s" % self.travel_data.size())
        
        k = len(self.travel_data.get_attribute_names())
        self.assertEqual(k, 2, msg = "Number of attributes should be 2 but is " + str(k) + ".")
        
        k = len(self.travel_data.get_primary_attribute_names())
        self.assertEqual(k, 2, msg = "Number of stored attributes should be 2 but is " + str(k) + ".")
         
    def test_get_attribute_as_matrix(self):
        result = self.travel_data.get_attribute_as_matrix('distance', from_time=5, to_time=6)
        self.assert_(allclose( result, self.distance),  msg="returned results should be %s but is %s" % (self.distance, result))
        result = self.travel_data.get_attribute_as_matrix('time', from_time=5, to_time=7, to_zone=array([1,2]))
        self.assert_(allclose( result, self.time5to6[:,0:2]+3),  msg="returned results should be %s but is %s" % (self.time5to6[:,0:2]+3, result))
        result = self.travel_data.get_attribute_as_matrix('time', from_time=6, from_zone=array([2,3]), to_zone=array([2]))
        should_be = array([[7],[127]])
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))
        result = self.travel_data.get_attribute('time', from_time=6, from_zone=array([2,3]), to_zone=array([2,1]))
        should_be = array([7, 72.4])
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))

if __name__=="__main__":
    opus_unittest.main()
    

        