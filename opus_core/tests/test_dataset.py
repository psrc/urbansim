# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


import os
import tempfile

from shutil import rmtree

from numpy import array, ma

from opus_core.tests import opus_unittest
from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.resource_factory import ResourceFactory
from opus_core.variables.attribute_type import AttributeType

from exceptions import StandardError
from opus_core.variables.variable_name import VariableName

class MoreDatasetTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.start_year = 2001
        self.expected_sic_data = array([6,4,7,808,6])
        self.job_id = array([1,2,3,4,5])
        self.base_cache_dir = tempfile.mkdtemp(prefix='opus_tmp_test_dataset')
        self.simulation_state = SimulationState(low_memory_run=True, new_instance=True, base_cache_dir=self.base_cache_dir)
        self.dir = self.simulation_state.get_cache_directory()
        self.simulation_state.set_current_time(self.start_year)
        
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.in_storage = StorageFactory().get_storage('dict_storage')
        self.in_storage.write_table(
            table_name='jobs',
            table_data={
                'grid_id':array([10,20,30,40,50]),
                'job_id':self.job_id,
                },
            )
            
        self.out_storage = StorageFactory().get_storage('dict_storage')
    
        self.job_set_resources = ResourceFactory().get_resources_for_dataset(
            'job', 
            in_storage = self.in_storage, 
            out_storage = self.out_storage,
            in_table_name_pair = ('jobs',None),
            out_table_name_pair = ('jobs_exported',None),
            attributes_pair = (None,AttributeType.PRIMARY),
            id_name_pair = ('job_id','job_id'), 
            nchunks_pair = (1,1), 
            debug_pair = (1,None)
            )
            
    def tearDown(self):
        if os.path.exists(self.base_cache_dir):
            rmtree(self.base_cache_dir)
        
    def test_err_when_asking_for_attribute_that_is_not_in_cache(self):
        job_set = Dataset(self.job_set_resources, dataset_name="jobs")
        job_set.add_attribute(self.job_id, "job_id", metadata=AttributeType.PRIMARY)
        job_set.flush_dataset()
        job_set.get_attribute('job_id')
        self.assertRaises(NameError, job_set.get_attribute, 'attribute_that_does_not_exist')
            
    def test_compute_one_variable_when_asking_for_attribute_that_is_not_in_cache(self):
        job_set = Dataset(self.job_set_resources, dataset_name="jobs")
        job_set.add_attribute(self.job_id, "job_id", metadata=AttributeType.PRIMARY)
        job_set.flush_dataset()
        job_id_variable_name = VariableName('opus_core.jobs.attribute_that_does_not_exist')
        
        logger.enable_hidden_error_and_warning_words()
        try:
            self.assertRaises(StandardError, job_set._compute_one_variable, job_id_variable_name)
            
        finally:
            logger.enable_hidden_error_and_warning_words()
            
    def test_flush_dataset_correct_flags(self):
        job_set = Dataset(self.job_set_resources, dataset_name="jobs")
        self.assert_(not 'job_id' in job_set.attribute_boxes)
        
        job_set.get_attribute("job_id")
        self.assert_(job_set.attribute_boxes["job_id"].is_in_memory())
        self.assert_(not job_set.attribute_boxes["job_id"].is_cached())
        
        job_set.flush_dataset()
        self.assert_(not job_set.attribute_boxes["job_id"].is_in_memory())
        self.assert_(job_set.attribute_boxes["job_id"].is_cached())
        
        job_set.get_attribute("job_id")
        self.assert_(job_set.attribute_boxes["job_id"].is_in_memory())
        self.assert_(job_set.attribute_boxes["job_id"].is_cached())
        
    def test_flush_dataset_correct_data(self):
        job_set = Dataset(self.job_set_resources, dataset_name="jobs")
        job_set.add_attribute(self.job_id, "job_id", metadata=AttributeType.PRIMARY)
        job_set.add_attribute(self.expected_sic_data, "sic", metadata=AttributeType.COMPUTED)
        job_set.flush_dataset()
        returned_sic_data = job_set.get_attribute("sic")
        returned_id_data = job_set.get_attribute("job_id")
        self.assert_(ma.allequal(returned_id_data,self.job_id))
        self.assert_(ma.allequal(returned_sic_data,self.expected_sic_data))
        
                   

class TestDataset(opus_unittest.OpusTestCase): 
    def setUp(self):
        self.start_year = 2001
        self.expected_sic_data = array([6,4,7,808,6])
        self.job_id = array([1,2,3,4,5])
        self.base_cache_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.simulation_state = SimulationState(low_memory_run=True, new_instance=True, base_cache_dir=self.base_cache_dir)
        self.dir = self.simulation_state.get_cache_directory()
        self.simulation_state.set_current_time(self.start_year)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        
        
    def tearDown(self):
        # the logger has a file open in the cache directory (by default, disable that file logging)
        if logger._file_stream:
            logger.disable_file_logging()
        
        for root, dirs, files in os.walk(self.dir, topdown=False):
            for filename in files:
                os.remove(os.path.join(root, filename))
            for directory in dirs:
                os.rmdir(os.path.join(root, directory))
        os.rmdir(self.dir)
        os.rmdir(self.base_cache_dir)
    
            
    def test_dict_dataset(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='dataset',
            table_data={
                "id":array([1,2,3,4]), 
                "attr":array([4,7,2,1])
                }
            )
        
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name="id")
        
        self.assert_(ds.get_attribute("attr").sum()==14, "Something is wrong with the dataset.")
        self.assert_(ds.size()==4, "Wrong size of dataset.")
        
    def test_flt_dataset(self):
        import opus_core
        from opus_core.store.flt_storage import flt_storage
        
        attribute = 'little_endian'
        
        location = os.path.join(opus_core.__path__[0], 'data', 'flt')
        storage = flt_storage(storage_location=location)
        ds = Dataset(in_storage=storage, id_name=attribute, in_table_name='endians')
        
        self.assertAlmostEqual(11.0, ds.get_attribute_by_index(attribute, 0))
        self.assertEqual(None, ds.get_attribute_header(attribute))
 
    def test_join_by_rows(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='dataset1', 
            table_data={    
                'id':array([2,4,6,8]), 
                'attr':array([4,7,2,1])
                }
            )
            
        storage.write_table(
            table_name='dataset2',
            table_data={
                'id':array([1,5,9]), 
                'attr':array([55,66,100])
                }
            )
        
        ds1 = Dataset(in_storage=storage, in_table_name='dataset1', id_name='id')
        ds2 = Dataset(in_storage=storage, in_table_name='dataset2', id_name='id')
        
        ds1.join_by_rows(ds2)
        self.assert_(ma.allclose(ds1.get_attribute('attr'), array([4,7,2,1,55,66,100])))
        self.assert_(ma.allclose(ds2.get_attribute('attr'), array([55,66,100])))
        
    def test_join_by_rows_for_unique_ids(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='dataset1', 
            table_data={
                "id":array([2,4]), 
                "attr":array([4,7])
                }
            )
            
        storage.write_table(
            table_name='dataset2',
            table_data={
                "id":array([1,2]), 
                "attr":array([55,66])
                }
            )
        
        ds1 = Dataset(in_storage=storage, in_table_name='dataset1', id_name='id')
        ds2 = Dataset(in_storage=storage, in_table_name='dataset2', id_name='id')
        
        threw_exception = False
        try: 
            ds1.join_by_rows(ds2)
        except StandardError:
            threw_exception = True
        self.assert_(threw_exception)
        
    def test_join_by_rows_for_char_arrays(self):
        from numpy import alltrue
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='dataset1', 
            table_data={
                'id':array([2,4,6,8]), 
                'attr':array(['4','7','2','1'])
                }
            )
            
        storage.write_table(
            table_name='dataset2',
            table_data={
                'id':array([1,5,9]), 
                'attr':array(['55','66','100'])
                }
            )
        
        ds1 = Dataset(in_storage=storage, in_table_name='dataset1', id_name='id')
        ds2 = Dataset(in_storage=storage, in_table_name='dataset2', id_name='id')
        
        ds1.join_by_rows(ds2)
        self.assert_(alltrue(ds1.get_attribute('attr') == array(['4','7','2','1','55','66','100'])))
        self.assert_(alltrue(ds2.get_attribute('attr') == array(['55','66','100'])))
        
    def test_variable_dependencies_tree_with_versioning(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                'id':array([2,4]), 
                'a_dependent_variable':array([4,7]),
                'a_dependent_variable2':array([10,1])
                }
            )
        
        ds = Dataset(in_storage=storage, in_table_name='tests', id_name='id', dataset_name='tests')
        
        ds.compute_variables(["opus_core.tests.a_test_variable_with_two_dependencies"])
        
        self.assert_(ds.get_version("a_test_variable_with_two_dependencies")==0) #initially version=0
        self.assert_(ds.get_version("a_dependent_variable")==0)
        self.assert_(ds.get_version("a_dependent_variable2")==0)
        
        ds.modify_attribute("a_dependent_variable", array([0,0]))
        self.assert_(ds.get_version("a_dependent_variable")==1) # version=1
        
        ds.modify_attribute("a_dependent_variable", array([1,1]))
        self.assert_(ds.get_version("a_dependent_variable")==2) # version=2
        
        ds.compute_variables(["opus_core.tests.a_test_variable_with_two_dependencies"])
        self.assert_(ds.get_version("a_test_variable_with_two_dependencies")==1)
        
        ds.compute_variables(["opus_core.tests.a_test_variable_with_two_dependencies"])
        self.assert_(ds.get_version("a_test_variable_with_two_dependencies")==1) # version does not change
        
        autogen_variable = "my_var = 3 * opus_core.tests.a_dependent_variable"
        ds.compute_variables([autogen_variable])
        self.assert_(ds.get_version("my_var")==0)
        ds.compute_variables([autogen_variable])
        self.assert_(ds.get_version("my_var")==0)
        
    def test_compute_variable_with_unknown_package(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                'id':array([2,4]), 
                'attr1':array([4,7]),
                }
            )
        
        ds = Dataset(in_storage=storage, in_table_name='tests', id_name='id', dataset_name='test')
        
        ds.compute_one_variable_with_unknown_package("attr1_times_2", package_order=["opus_core"])
        
    def test_join_datasets_with_2_ids(self):
        from numpy import ma
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='data1',
            table_data={
                'id1':array([2,4,2]),
                'id2':array([1,2,3]),
                'attr1':array([4,7,1]),
                'attr2':array([100,0,1000]),
                }
            )
        storage.write_table(
            table_name='data2',
            table_data={
                'id1':array([4,2,2]),
                'id2':array([2,3,1]),
                'attr1':array([50,60,70])
                }
            )
        
        ds1 = Dataset(in_storage=storage, in_table_name='data1', id_name=['id1', 'id2'], dataset_name='data1')
        ds2 = Dataset(in_storage=storage, in_table_name='data2', id_name=['id1', 'id2'], dataset_name='data2')
        ds1.join(ds2, 'attr1')
        self.assertEqual(ma.allequal(ds1.get_attribute('attr1'), array([70,50,60])), True)
        self.assertEqual(ma.allequal(ds1.get_attribute('attr2'), array([100,0,1000])), True)
        
if __name__ == "__main__":
    opus_unittest.main()