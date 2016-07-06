from numpy import setdiff1d, all, equal, logical_not
import pandas as pd
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.models.model import Model
from opus_core.logger import logger

class CompareCaches(Model):
    """Check if two cache directories contain the same data."""
    
    def __init__(self, directory1, directory2):
        self.storage1 = AttributeCache(directory1)
        self.storage2 = AttributeCache(directory2)
    
    def run(self, year=2014):
        SimulationState().set_current_time(year)
        tables1 = self.storage1.get_table_names()
        tables2 = self.storage2.get_table_names()
        dif = setdiff1d(tables1, tables2)
        if dif.size > 0:
            logger.log_status("Tables that are only in one of the caches: %s" % str(dif).strip('[]'))
        for table in tables1:
            if table in dif:
                continue
            logger.log_status("TABLE: %s" % table)
            tabdata1 = self.storage1.load_table(table)
            tabdata2 = self.storage2.load_table(table)
            columns1 = tabdata1.keys()
            columns2 = tabdata2.keys()
            coldif = setdiff1d(columns1, columns2)
            if coldif.size > 0:
                logger.log_status("\tColumns that are only in one of the caches: %s" % str(coldif).strip('[]')) 
                for col in coldif:
                    if col in columns1:
                        del tabdata1[col]
                    if col in columns2:
                        del tabdata2[col]                    
            df1 = pd.DataFrame(tabdata1)
            df2 = pd.DataFrame(tabdata2)
            is_equal = df1.equals(df2)
            if not is_equal:
                logger.log_status("\tDetected differences in columns:")
                for col in tabdata1.keys():
                    if tabdata1[col].size <> tabdata2[col].size:
                        logger.log_status("\t\t%s: size varies" % col)
                    else:
                        eq = equal(tabdata1[col], tabdata2[col])
                        if not all(eq):
                            logger.log_status("\t\t%s (%s mismatched records)" % (col, logical_not(eq).sum()))

            
        
if __name__ == '__main__':
    # Cache directories
    dir1 = '/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/base_year_2014_inputs/luv_scenario_test'
    dir2 = '/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/base_year_2014_inputs/luv_flu_updated'
    #dir2 = '/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_73.run_2016_06_13_16_56'
    # Run the model
    CompareCaches(dir1, dir2).run(year=2014)
    