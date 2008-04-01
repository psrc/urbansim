from configure_path import *
from store.MultiDB import DbConnection
import os
from storage_creator import StorageCreator
from gridcellset.gridcells import GridcellSet
from householdset.households import HouseholdSet

class DB_settings:
    #db_host_name=os.environ['MYSQLHOSTNAME']
    db_host_name="localhost"
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']    

class PSRC_Settings:
    dir = "./PSRC_data_dir"
    gcsubdir = "gc"
    hhsubdir = "hh"
    db = "PSRC_2000_baseyear_0510_lmwang"
        
class ReadWriteDataSet:
    def __init__(self, dataset, out_storage_type, out_base, out_place):
        dataset.load_dataset()
        out_storage = StorageCreator().build_storage(base=out_base, type=out_storage_type)
        dataset.write_dataset(out_storage=out_storage, out_place=out_place)
        
class ReadMySQLWriteFlt_PSRC:
    """Reads Gridcells and Households for PSRC from MySQL and writes them to disk."""
    def __init__(self):
        Con = DbConnection(db=PSRC_Settings.db, hostname=DB_settings.db_host_name, \
            username=DB_settings.db_user_name, password=DB_settings.db_password)
        gcs = GridcellSet(in_base = Con, in_storage_type="mysql", nchunks=5)
        hhs = HouseholdSet(in_base = Con, in_storage_type="mysql", nchunks=3)
        print "Read and Write GridcellSet."
        ReadWriteDataSet(gcs, out_storage_type="flt", out_base=PSRC_Settings.dir, \
                out_place=PSRC_Settings.gcsubdir)
        print "Read and Write HouseholdSet."
        ReadWriteDataSet(hhs, out_storage_type="flt", out_base=PSRC_Settings.dir, \
                out_place=PSRC_Settings.hhsubdir)
        Con.close_connection()
        
if __name__ == "__main__":
        ReadMySQLWriteFlt_PSRC()        
