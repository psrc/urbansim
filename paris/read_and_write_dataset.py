from opus_core.store.opus_database import OpusDatabase
import os
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.travel_data import TravelDataDataset
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.neighborhood_dataset import NeighborhoodDataset
from urbansim.datasets.job_dataset import JobDataset
from paris.paris_settings import ParisSettings
from opus_core.storage_factory import StorageFactory
#
# Miscellaneous stuff for manually testing and for generating flt binary databases
#

settings = ParisSettings()
       
class ReadWriteADataset(object):
    def __init__(self, dataset, out_storage, out_table_name):
        dataset.load_dataset()
        dataset.write_dataset(out_storage=out_storage, out_table_name=out_table_name)
        
class GridcellsReadMySQLWriteFlt(object):
    """Reads Gridcells from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(),
                           password=settings.get_db_password(),
                           database_name=settings.db)
        gcs = GridcellDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con), nchunks=5)
        print "Read and Write GridcellDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(gcs, out_storage=out_storage, out_table_name=settings.gcsubdir)
        Con.close()

class NeighborhoodsReadMySQLWriteFlt(object):
    """Reads Neighborhoods from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(),
                           password=settings.get_db_password(),
                           database_name=settings.db)
        nbs = NeighborhoodDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con), nchunks=5)
        print "Read and Write NeighborhoodDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(nbs, out_storage=out_storage, out_table_name=settings.nbsubdir)
        Con.close()

class HouseholdsReadMySQLWriteFlt(object):
    """Reads Households from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(), 
                           password=settings.get_db_password(),
                           database_name=settings.db)
        hhs = HouseholdDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con), nchunks=3)
        print "Read and Write HouseholdDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(hhs, out_storage=out_storage, out_table_name=settings.hhsubdir)
        Con.close()
  

class JobsReadMySQLWriteFlt(object):
    """Reads jobs from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(),
                           password=settings.get_db_password(),
                           database_name=settings.db)
        jobs = JobDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con), nchunks=5)
        print "Read and Write JobDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(jobs, out_storage=out_storage, out_table_name=settings.jobsubdir)
        Con.close()

class TravelDataReadMySQLWriteFlt(object):
    """Reads travel data from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(), 
                           password=settings.get_db_password(),
                           database_name=settings.db)
        traveldata = TravelDataDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con))
        print "Read and Write TravelDataDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(traveldata, out_storage=out_storage, out_table_name=settings.traveldatasubdir)
        Con.close()
              
class ZonesReadMySQLWriteFlt(object):
    """Reads zones from MySQL and writes them to disk."""
    def __init__(self):
        Con = OpusDatabase(hostname=settings.get_db_host_name(),
                           username=settings.get_db_user_name(), 
                           password=settings.get_db_password(),
                           database_name=settings.db, )
        zones = ZoneDataset(in_storage=StorageFactory().get_storage('mysql_storage', storage_location=Con))
        print "Read and Write ZoneDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(zones, out_storage=out_storage, out_table_name=settings.zonesubdir)
        Con.close()
              
if __name__ == "__main__":
#        GridcellsReadMySQLWriteFlt()
        HouseholdsReadMySQLWriteFlt()      
        JobsReadMySQLWriteFlt()  
        NeighborhoodsReadMySQLWriteFlt()
#        TravelDataReadMySQLWriteFlt()
#        ZonesReadMySQLWriteFlt()