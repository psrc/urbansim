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
    def __init__(self, reference_location):               
        self.reference_storage =  flt_storage(reference_location)
    
    def run(self, directory=None):
        if directory is None:
            directory = SimulationState().get_cache_directory()        
        self.cache = AttributeCache(directory)
        year_orig = SimulationState().get_current_time()
        years = self.years_in_cache()
        SimulationState().set_current_time(years[0])
        storages = {}
        for year in years:
            storages[year] = flt_storage(os.path.join(self.cache.get_storage_location(), '%s' % year))
        df = pd.DataFrame(columns=["Table", "Less-than-ref", "More-than-ref", "Year"])
        tables = self.cache.get_table_names() 
        for table in tables:
            columns = Set(self.cache.get_column_names(table))
            ref_columns = Set(self.reference_storage.get_column_names(table, lowercase=True))
            more = columns.difference(ref_columns)
            less = ref_columns.difference(columns)
            if len(more) > 0 or len(less) > 0:
                df.loc[df.shape[0]] = [table, ', '.join(less), ', '.join(more), '']
                if len(more) > 0:
                    columns_and_years = self.cache._get_column_names_and_years(table)
                    more_years = []
                    for col, year in columns_and_years:
                        if col in more:
                            more_years.append(year)
                    df.loc[df.shape[0]-1, "Year"] = ', '.join(np.unique(np.array(more_years).astype("str")))
        logger.log_status(df)
        return df
    
    def years_in_cache(self):
        return self.cache._get_sorted_list_of_years(start_with_current_year=False)    
    
    
import tempfile
from shutil import rmtree
from opus_core.tests import opus_unittest  
    
class QCDataStructureTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache')
        self.table_name = 'test_table'
        self.storage = AttributeCache(self.temp_dir)
        self.temp_refdir = tempfile.mkdtemp(prefix='opus_tmp_reference_cache')
        self.refstorage = AttributeCache(self.temp_refdir)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        if os.path.exists(self.temp_refdir):
                rmtree(self.temp_refdir)        
    
    def test_detect(self):
        # Create two caches with the same table but with different attributes.
        # The simulation cache has two years
        SimulationState().set_current_time(2010)
        table_data = {'int_column': np.array([100, 70], dtype="int32"),
                      'bool_column': np.array([False, True])}
        self.storage.write_table(self.table_name, table_data)
        SimulationState().set_current_time(2000)
        table_data = {'flt_column': np.array([10, 70], dtype="float32")}
        self.storage.write_table(self.table_name, table_data)
        # create reference cache
        SimulationState().set_current_time(2005)
        table_data = {'str_column': np.array(['a', 'b']),
                      'bool_column': np.array([False, True])}
        self.refstorage.write_table(self.table_name, table_data)
        # run the model
        res = DataStructureModel(os.path.join(self.temp_refdir, "%s" % 2005)).run(self.temp_dir)
        self.assertEqual(res.shape[0], 1) # one row
        self.assertEqual(res.loc[0, "Less-than-ref"], "str_column")
        self.assertEqual("flt_column" in res.loc[0, "More-than-ref"], True)
        self.assertEqual("int_column" in res.loc[0, "More-than-ref"], True)
        self.assertEqual("bool_column" in res.loc[0, "More-than-ref"], False)
        self.assertEqual("bool_column" in res.loc[0, "Less-than-ref"], False)
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/test"
    #refdir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/base_year_data/2010"
    #DataStructureModel(refdir).run(dir)
    opus_unittest.main()