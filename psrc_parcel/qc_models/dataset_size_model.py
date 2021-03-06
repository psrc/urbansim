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
    
    def run(self):
        year_orig = SimulationState().get_current_time()
        years = self.years_in_cache()
        SimulationState().set_current_time(years[0])
        storages = {}
        for year in years:
            storages[year] = flt_storage(os.path.join(self.cache.get_storage_location(), '%s' % year))
        tables = self.cache.get_table_names()
        counts = pd.Series(np.zeros(len(tables), dtype="int32"), index=tables)
        for table in tables:
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
            if(all(values == values[0])):
                continue # all attributes have the same size
            # there is an inconsistency in attributes length
            names = np.array(names)
            colyears = np.array(colyears)
            uc = np.unique(values, return_counts=True)
            imax = np.argmax(uc[1])
            idx = np.where(values <> uc[0][imax])[0]
            df = pd.DataFrame({"column": names[idx],  "year": colyears[idx], "size": values[idx]})
            df = df.append(pd.DataFrame({"column": np.array(["all other columns"]), "year": np.array([years[0]]), "size": np.array([uc[0][imax]])}))
            logger.log_status("Inconsistency in table ", table, ":\n", df)
            counts[table] = df.shape[0] - 1
        SimulationState().set_current_time(year_orig)
        logger.log_status("Model total:", counts.sum(), ' size inconsistencies found.')
        return counts

    
    def years_in_cache(self):
        return self.cache._get_sorted_list_of_years(start_with_current_year=False)

                                                    
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
        table_data = {'int_column': np.array([100, 70], dtype="int32"),
                      'bool_column': np.array([False, True])}
        # file name will be e.g. 'int_column.li4' for a little-endian machine
        self.storage.write_table(self.table_name, table_data)
        SimulationState().set_current_time(1979)
        table_data = {'flt_column': np.array([10, 70, 5.7], dtype="float32")}
        self.storage.write_table(self.table_name, table_data)        
        res = DatasetSizeModel(self.temp_dir).run()
        SimulationState().set_current_time(2000)
        self.assertEqual(res.sum(), 1)
        # reset time to the original one
        self.assertEqual(SimulationState().get_current_time(), 2000)
   
    
    
if __name__=="__main__":
    #dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/test"
    #DatasetSizeModel(dir).run()
    opus_unittest.main()