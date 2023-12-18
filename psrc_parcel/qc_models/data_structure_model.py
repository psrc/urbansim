import os
import numpy as np
import pandas as pd
from sets import Set
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.flt_storage import flt_storage
from opus_core.simulation_state import SimulationState

class DataStructureModel(Model):
    """
    Checks the structure of datasets in a given cache (or run cache) when compared to a reference cache.
    It writes out all columns that are missing as well as those that are not present in the reference cache.
    It can also compare the sizes of the datasets. 
    """
    def __init__(self, reference_location=None):
        """
        "reference_location" is the directory of the reference cache and should include the year.
        If it is None, the simulation directory in its start year is taken. 
        """
        if reference_location is None:
            reference_location = os.path.join(SimulationState().get_cache_directory(), "%s" % SimulationState().get_start_time())
        self.reference_storage =  flt_storage(reference_location)
    
    def run(self, directory=None, check_size=True):
        """
        "directory" is the cache to be compared to the reference. It should not include the year
        as the model checks all years.
        Set "check_sizes" to False if no size check of the datasets is required. 
        """
        if directory is None:
            directory = SimulationState().get_cache_directory()        
        self.cache = AttributeCache(directory)
        year_orig = SimulationState().get_current_time()
        years = self.years_in_cache()
        SimulationState().set_current_time(years[0])
        storages = {}
        for year in years:
            storages[year] = flt_storage(os.path.join(self.cache.get_storage_location(), '%s' % year))
        df = pd.DataFrame(columns=["Table", "Less-than-ref", "More-than-ref", "Year", "Size", "Size-ref"])
        tables = self.cache.get_table_names() 
        for table in tables:
            columns_list = self.cache.get_column_names(table)
            columns = Set(columns_list)
            ref_columns_list = self.reference_storage.get_column_names(table, lowercase=True)
            ref_columns = Set(ref_columns_list)
            more = columns.difference(ref_columns)
            less = ref_columns.difference(columns)
            samesize = True
            if check_size:
                table_size = self.cache.load_table(table, columns_list[0])[columns_list[0]].size
                reftable_size = self.reference_storage.load_table(table, ref_columns_list[0])[ref_columns_list[0]].size
                if table_size != reftable_size:
                    samesize = False
            if len(more) == 0 and len(less) == 0 and samesize:
                continue
            df.loc[df.shape[0]] = [table, ', '.join(less), ', '.join(more), '', 0, 0]
            if len(more) == 0 and samesize:
                continue
            # if there are columns in the "more" column, write out the corresponding years
            columns_and_years = self.cache._get_column_names_and_years(table)
            more_years = []
            for col, year in columns_and_years:
                if col in more:
                    more_years.append(year)
            df.loc[df.shape[0]-1, "Year"] = ', '.join(np.unique(np.array(more_years).astype("str")))
            if not samesize:  # there is difference in table sizes
                df.loc[df.shape[0]-1, "Size"] = table_size
                df.loc[df.shape[0]-1, "Size-ref"] = reftable_size
           
        if not check_size or (df['Size'].sum()==0 and df['Size-ref'].sum()==0):
            # remove the size columns if not used
            del df['Size']
            del df['Size-ref']
        if df.shape[0] > 0:
            logger.log_status("Differences in data structure relative to %s:" % self.reference_storage.get_storage_location())
            logger.log_status(df)
        else:
            logger.log_status("Data structure corresponds to the one in %s" % self.reference_storage.get_storage_location())
        return df
    
    def years_in_cache(self):
        return self.cache._get_sorted_list_of_years(start_with_current_year=False)    
    
    
import tempfile
from shutil import rmtree
from opus_core.tests import opus_unittest  
    
class QCDataStructureTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache')
        table_name = 'test_table'
        storage = AttributeCache(self.temp_dir)
        self.temp_refdir = tempfile.mkdtemp(prefix='opus_tmp_reference_cache')
        refstorage = AttributeCache(self.temp_refdir)
        # Create two caches with the same table but with different attributes.
        # The simulation cache has two years
        SimulationState().set_current_time(2010)
        table_data = {'int_column': np.array([100, 70], dtype="int32"),
                      'bool_column': np.array([False, True])}
        storage.write_table(table_name, table_data)
        SimulationState().set_current_time(2000)
        table_data = {'flt_column': np.array([10, 70], dtype="float32")}
        storage.write_table(table_name, table_data)
        # create reference cache
        SimulationState().set_current_time(2005)
        table_data = {'str_column': np.array(['a', 'b']),
                      'bool_column': np.array([False, True])}
        refstorage.write_table(table_name, table_data)
        # create another simulation cache with a table of different length
        self.temp_dir2 = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache2')
        storage = AttributeCache(self.temp_dir2)
        SimulationState().set_current_time(2010)
        table_data = {'str_column': np.array(['a', 'b', 'c']),
                      'bool_column': np.array([False, True, True])}
        storage.write_table(table_name, table_data)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        if os.path.exists(self.temp_refdir):
            rmtree(self.temp_refdir)        
    
    def test_different_attributes(self):
        res = DataStructureModel(os.path.join(self.temp_refdir, "%s" % 2005)).run(self.temp_dir)
        self.assertEqual(res.shape[0], 1) # one row
        self.assertEqual(res.loc[0, "Less-than-ref"], "str_column")
        self.assertTrue("flt_column" in res.loc[0, "More-than-ref"])
        self.assertTrue("int_column" in res.loc[0, "More-than-ref"])
        self.assertTrue("bool_column" not in res.loc[0, "More-than-ref"])
        self.assertTrue("bool_column" not in res.loc[0, "Less-than-ref"])
        self.assertTrue("Size" not in res.columns.values.tolist())
        self.assertTrue("Size-ref" not in res.columns.values.tolist())
        
    def test_different_sizes(self):
        res = DataStructureModel(os.path.join(self.temp_refdir, "%s" % 2005)).run(self.temp_dir2)
        self.assertEqual(res.shape[0], 1)
        self.assertEqual(res.loc[0, "Size"], 3)
        self.assertEqual(res.loc[0, "Size-ref"], 2)
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/test"
    #refdir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/base_year_data/2010"
    #DataStructureModel(refdir).run(dir)
    opus_unittest.main()