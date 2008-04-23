#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import os
from numpy import where, ones, logical_and, array, median, resize, abs
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.logger import logger

class MysqlStorage:
    def get(self, database):
        db_config = DatabaseServerConfiguration(
            host_name = os.environ['MYSQLHOSTNAME'],
            user_name = os.environ['MYSQLUSERNAME'],
            password = os.environ['MYSQLPASSWORD']                                              
            )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(database)
        
        storage = StorageFactory().get_storage('sql_storage',
                                                storage_location = db)
        return storage

if __name__ == '__main__':
    input_database_name = 'psrc_2005_parcel_baseyear_data_prep_2006_survey'
    output_database_name = input_database_name
    instorage = MysqlStorage().get(input_database_name)
    outstorage = MysqlStorage().get(output_database_name)

    cache_directory = "/urbansim_cache/psrc_parcel/wcm_estimation"
    base_year = 2000
    #import wingdbstub
    from opus_core.simulation_state import SimulationState
    from opus_core.session_configuration import SessionConfiguration
    from opus_core.datasets.dataset import Dataset
    from opus_core.store.attribute_cache import AttributeCache
    from tables import openFile
    #from tables import *
    from opus_core.sampling_toolbox import sample_noreplace
    
    SimulationState().set_cache_directory(cache_directory)
    SimulationState().set_current_time(base_year)
    attribute_cache = AttributeCache()
    SessionConfiguration(new_instance=True,
                         package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim', 'opus_core'],
                         in_storage=attribute_cache)
    dataset_pool = SessionConfiguration().get_dataset_pool()
    jobs = dataset_pool.get_dataset('job')
    jobs.compute_variables("urbansim_parcel.job.zone_id")
    
#    person_for_estimatoin = Dataset('persons_for_estimation')
    persons_for_estimatoin = Dataset(in_storage = attribute_cache,
                                    in_table_name="persons_for_estimation",
                                    id_name="person_id", 
                                    dataset_name="person")

    # Open a file in "w"rite mode
    h5file = openFile("/home/lmwang/playground/y2000.h5", mode = "w", title = "Test file")
    # Create a new group under "/" (root)
    y2000 = h5file.createGroup("/", 'y2000', 'Year 2000 data')

    tjobs = jobs.createTable(h5file, y2000)
    tpersons = persons_for_estimatoin.createTable(h5file, y2000, name="persons_for_estimation")
    
    h5file.flush()
    #import sys
    #sys.exit(0)
    
    assigned_jobs = []
    #i = 1
    for person in tpersons.where('is_worker>0'):
        print person.nrow, person['workplace_zone_id'], person['worker_sector_id'], person['work_at_home'], '=',
        matched_jobs = [job['job_id'] for job in tjobs.where('(zone_id == workplace_zone_id) & ' \
                                         '(sector_id == worker_sector_id) & ' \
                                         '(building_type == work_at_home)',
                                         {'workplace_zone_id':person['workplace_zone_id'],
                                          'worker_sector_id':person['worker_sector_id'],
                                          'work_at_home':person['work_at_home']                                        
                                         }
                                     )]
        print str(len(matched_jobs)),
        if len(matched_jobs)>0:
            while True:
                tmp_job = sample_noreplace(array(matched_jobs), 1)
                #tmp_job = matched_jobs[0]
                if (array(assigned_jobs) == tmp_job).sum() == 0:
                    break
        
            person['job_id'] = tmp_job
            person.update()
            
            assigned_jobs.append(tmp_job)
        
        print "."
        #i += 1
    
    #is_worker = where(persons_for_estimatoin.get_attribute("is_worker")>0)[0]
    #workplace_zone_id = persons_for_estimatoin.get_attribute("workplace_zone_id")[is_worker]
    #worker_sector_id = persons_for_estimatoin.get_attribute("worker_sector_id")[is_worker]
    #job_zone_id = jobs.get_attribute("zone_id")
    #job_sector_id = jobs.get_attribute("sector_id")
    #assigned_job = array([])
    #from numpy import where
    #for zone in unique_values(workplace_zone_id):
        #workers_in_this_zone = where(workplace_zone_id == zone)[0]
        #worker_sectors = worker_sector_id[workers_in_this_zone]
        #for sector in unique_values(worker_sectors):
            #workers_in_this_zone_of_this_sector = logical_and(workers_in_this_zone==zone,
                                                              #worker_sectors == sector)
            #jobs_in_this_zone_of_this_sector = 

    #logger.log_status("Loading parcels ...")
    #parcels.load_dataset(attributes=['parcel_sqft', 'parcel_sqft_2005', 'land_value', 'improvement_value', 'land_value_2005',
                                     #'improvement_value_2005', "zone_id", "land_use_type_id"])
    #logger.log_status("Loading finished.")
    #sqft_2000 = parcels.get_attribute('parcel_sqft').astype("float32")
    #sqft_2005 = parcels.get_attribute('parcel_sqft_2005').astype("float32")
    #total_value_2000 = (parcels.get_attribute('land_value')+parcels.get_attribute('improvement_value')).astype("float32")
    #total_value_2005 = (parcels.get_attribute('land_value_2005')+parcels.get_attribute('improvement_value_2005')).astype("float32")
    #is_valid = logical_and(logical_and(logical_and(logical_and(sqft_2000 > 0, sqft_2005 > 0), 
                           #total_value_2005>0), total_value_2000>0), abs(total_value_2005-total_value_2000)>0)
    #increases = (total_value_2000[is_valid]/sqft_2000[is_valid])/(total_value_2005[is_valid]/sqft_2005[is_valid])
    ##zones = parcels.get_attribute("zone_id")[is_valid]
    #zones = parcels.compute_variables(["large_area_id = parcel.disaggregate(faz.large_area_id, intermediates=[zone])"], dataset_pool=dataset_pool)[is_valid]
    #lu_types = parcels.get_attribute("land_use_type_id")[is_valid]
    #unique_zones = unique_values(zones)
    #unique_types = unique_values(lu_types)
    #result_zone = []
    #result_lut = []
    #result_rate = []
    #result_n = []
    #for zone in unique_zones:
        #logger.log_status("LA id: %s" % zone)
        #is_zone = zones == zone
        #for lut in unique_types:
            #is_lut = logical_and(is_zone, lu_types == lut)
            #if is_lut.sum() > 0:
                #result_zone.append(zone)
                #result_lut.append(lut)
                #mid = round(median(increases[is_lut]),3)
                #result_rate.append(mid)
                #result_n.append(is_lut.sum())
                
    #storage = StorageFactory().get_storage('dict_storage')
    #storage.write_table(
            #table_name='average_increase_of_total_value',
            #table_data={
                        ##"zone_id": array(result_zone),
                        #"large_area_id": array(result_zone),
                        #"land_use_type_id" : array(result_lut),
                        #"increase_rate": array(result_rate),
                        #'number_of_observations': array(result_n)
                        #}
                        #)
    #ds = Dataset(in_storage=storage, id_name=['large_area_id', 'land_use_type_id'], in_table_name='average_increase_of_total_value')
    #ds.write_dataset(out_storage=outstorage, out_table_name='average_increase_of_total_value')
