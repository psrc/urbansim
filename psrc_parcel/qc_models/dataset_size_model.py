import os
import numpy as np
import pandas as pd
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.flt_storage import flt_storage
from opus_core.simulation_state import SimulationState

class DatasetSizeModel(Model):
    """Checks if all datasets after collapsing over all years have attributes of the same size."""
    
    def __init__(self, directory=None):
        if directory is None:
            directory = SimulationState().get_cache_directory()
        self.cache = AttributeCache(directory)
    
    def run(self, target_size={}):
        """Argument target_size can specify tables and the number of records it should have."""
        
        year_orig = SimulationState().get_current_time()
        years = self.years_in_cache()
        SimulationState().set_current_time(years[0])
        storages = {}
        for year in years:
            storages[year] = flt_storage(os.path.join(self.cache.get_storage_location(), '%s' % year))
        tables = self.cache.get_table_names()
        counts = pd.Series(np.zeros(len(tables), dtype="int32"), index=tables)
        for table in tables:
            target = target_size.get(table)
            columns = self.cache._get_column_names_and_years(table)
            values = []
            names = []
            colyears = []
            for col, year in columns:
                if col in names:
                    continue
                data = storages[year].load_table(table, column_names=col)
                values.append(data[col].size)
                names.append(col)
                colyears.append(year)
            values = np.array(values)
            if all(values == values[0]): # all attributes have the same size
                if is_equal_to_target(values[0], target): # size corresponds to target
                    continue
                logger.log_status("Size of table ", table, " (", values[0], ") does not match target (", target, ")\n")
                counts[table] = counts[table] + 1
                continue
            # there is an inconsistency in attributes length
            names = np.array(names)
            colyears = np.array(colyears)
            uc = np.unique(values, return_counts=True)
            imax = np.argmax(uc[1])
            idx = np.where(values <> uc[0][imax])[0]
            df = pd.DataFrame({"column": names[idx],  "year": colyears[idx], "size": values[idx], "target": target})
            df = df.append(pd.DataFrame({"column": np.array(["all other columns"]), "year": np.array([years[0]]), "size": np.array([uc[0][imax]]), "target": target}))
            logger.log_status("Inconsistency in table ", table, ":\n", df)
            counts[table] = df.shape[0] - 1
        SimulationState().set_current_time(year_orig)
        logger.log_status("Model total:", counts.sum(), ' size inconsistencies found.')
        return counts

    
    def years_in_cache(self):
        return self.cache._get_sorted_list_of_years(start_with_current_year=False)

def is_equal_to_target(value, target):
    if target is None:
        return True
    return value == target
                                                    
import tempfile
from shutil import rmtree
from opus_core.tests import opus_unittest  
    
class QCDataSizeTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache')
        self.table_name = 'test_table'
        self.storage = AttributeCache(self.temp_dir)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
    
    def test_detect(self):
        # create cache where a table has attributes of different length,
        # namely size 2 in 1980 and size 3 in 1979 
        SimulationState().set_current_time(1980)
        table_data1 = {'int_column': np.array([100, 70], dtype="int32"),
                      'bool_column': np.array([False, True])}
        self.storage.write_table(self.table_name, table_data1)       
        SimulationState().set_current_time(1979)
        table_data = {'flt_column': np.array([10, 70, 5.7], dtype="float32")}
        self.storage.write_table(self.table_name, table_data)        
        res = DatasetSizeModel(self.temp_dir).run()
        self.assertEqual(res.sum(), 1)
        # test with target
        self.storage.write_table("test_table2", table_data1)
        res = DatasetSizeModel(self.temp_dir).run(target_size={"test_table2":3})        
        self.assertEqual(res.sum(), 2)
        
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/test"
    #DatasetSizeModel(dir).run()
    opus_unittest.main()