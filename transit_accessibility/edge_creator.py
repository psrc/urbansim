# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.misc import unique_values
from numpy import where, array, arange, int64, int32
from opus_core.storage_factory import StorageFactory

# TODO: class is not tested in all_tests.py and the test is broken

class EdgeCreator(object):
    def create_edges(self, input_file_dir, input_file_name, output_file_name):
        storage = StorageFactory().get_storage(type='tab_storage', subdir='store', 
            storage_location=input_file_dir)
        dataset = Dataset(in_storage = storage, id_name = ['stop_id','sch_time'], in_table_name = input_file_name)
        
        n = dataset.size()
        trip_ids = dataset.get_attribute("stop_id")
        unique_trip_ids = unique_values(trip_ids)
        source_list = list()
        target_list = list()
        time_list = list()
        
        for trip in unique_trip_ids:
            idx = where(dataset.get_attribute("stop_id") == trip)[0]
            nodes = dataset.get_attribute_by_index("node_id", idx)
            times = dataset.get_attribute_by_index("sch_time", idx)
            for inode in range(nodes.size-1):
                source_list.append(nodes[inode])
                target_list.append(nodes[inode+1])
                time_list.append(times[inode+1] - times[inode])
       
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='edges',
            table_data={
                'edge_id': arange(len(source_list))+1, 
                'source': array(source_list), #type=int64), # <<<< OUTPUT FIELD, USE array
                'target': array(target_list), #type=int64), # <<<< OUTPUT FIELD, USE array
                'cost': array(time_list, dtype=int32)
                }
            )
       
        edges = Dataset(in_storage=storage, in_table_name='edges', id_name = "edge_id")
        
        edges.write_dataset(attributes = ["source", "target", "cost"], out_storage = storage, out_table_name = output_file_name)


### TODO: These tests should be un-'hidden' once they have an input that actually exists...
if __name__ == "__main__":
    class CreateEdgesTests(opus_unittest.OpusTestCase):
        def setUp(self):
            import transit_accessibility.tests
            self.output_file_name = 'same_stop_transfers_nodes_weekday_txt_edges.txt' # <<<< OUTPUT FILE NAME HERE <<<<
            self.test_path = os.path.join(transit_accessibility.tests.__path__[0],'data')
            
        def tearDown(self):
            pass
            #os.remove( os.path.join(self.test_path, self.output_file_name) )
            
        def test_create_file(self):
            edge_creator = EdgeCreator()
            edge_creator.create_edges(self.test_path,
                                      'same_stop_transfers_nodes_weekday_txt.txt',  # <<<< INPUT FILE NAME HERE <<<<
                                      self.output_file_name)
            self.assert_(os.path.isfile(os.path.join(self.test_path, self.output_file_name)))
    
    opus_unittest.main()