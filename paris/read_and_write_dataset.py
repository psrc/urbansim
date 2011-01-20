# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.travel_data import TravelDataDataset
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.neighborhood_dataset import NeighborhoodDataset
from urbansim.datasets.job_dataset import JobDataset
from paris.paris_settings import ParisSettings
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

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
        db_config = DatabaseServerConfiguration(
            host_name=settings.get_db_host_name(),
            user_name=settings.get_db_user_name(),
            password=settings.get_db_password()                                           
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(settings.db)
        
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            storage_location = db)
        
        gcs = GridcellDataset(in_storage=in_storage, nchunks=5)
        print "Read and Write GridcellDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(gcs, out_storage=out_storage, out_table_name=settings.gcsubdir)

class NeighborhoodsReadMySQLWriteFlt(object):
    """Reads Neighborhoods from MySQL and writes them to disk."""
    def __init__(self):
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            hostname=settings.get_db_host_name(),
            username=settings.get_db_user_name(),
            password=settings.get_db_password(),
            database_name=settings.db)
        nbs = NeighborhoodDataset(in_storage=in_storage, nchunks=5)
        print "Read and Write NeighborhoodDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(nbs, out_storage=out_storage, out_table_name=settings.nbsubdir)

class HouseholdsReadMySQLWriteFlt(object):
    """Reads Households from MySQL and writes them to disk."""
    def __init__(self):
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            hostname=settings.get_db_host_name(),
            username=settings.get_db_user_name(),
            password=settings.get_db_password(),
            database_name=settings.db)
        hhs = HouseholdDataset(in_storage=in_storage, nchunks=3)
        print "Read and Write HouseholdDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(hhs, out_storage=out_storage, out_table_name=settings.hhsubdir)
  

class JobsReadMySQLWriteFlt(object):
    """Reads jobs from MySQL and writes them to disk."""
    def __init__(self):
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            hostname=settings.get_db_host_name(),
            username=settings.get_db_user_name(),
            password=settings.get_db_password(),
            database_name=settings.db)
        jobs = JobDataset(in_storage=in_storage, nchunks=5)
        print "Read and Write JobDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(jobs, out_storage=out_storage, out_table_name=settings.jobsubdir)

class TravelDataReadMySQLWriteFlt(object):
    """Reads travel data from MySQL and writes them to disk."""
    def __init__(self):
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            hostname=settings.get_db_host_name(),
            username=settings.get_db_user_name(),
            password=settings.get_db_password(),
            database_name=settings.db)
        traveldata = TravelDataDataset(in_storage=in_storage)
        print "Read and Write TravelDataDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(traveldata, out_storage=out_storage, out_table_name=settings.traveldatasubdir)
              
class ZonesReadMySQLWriteFlt(object):
    """Reads zones from MySQL and writes them to disk."""
    def __init__(self):
        in_storage = StorageFactory().get_storage(
            'sql_storage',
            hostname=settings.get_db_host_name(),
            username=settings.get_db_user_name(),
            password=settings.get_db_password(),
            database_name=settings.db)
        zones = ZoneDataset(in_storage=in_storage)
        print "Read and Write ZoneDataset."
        out_storage = StorageFactory().build_storage_for_dataset(type='flt_storage', 
            storage_location=settings.dir)
        ReadWriteADataset(zones, out_storage=out_storage, out_table_name=settings.zonesubdir)
              
if __name__ == "__main__":
#        GridcellsReadMySQLWriteFlt()
        HouseholdsReadMySQLWriteFlt()      
        JobsReadMySQLWriteFlt()  
        NeighborhoodsReadMySQLWriteFlt()
#        TravelDataReadMySQLWriteFlt()
#        ZonesReadMySQLWriteFlt()