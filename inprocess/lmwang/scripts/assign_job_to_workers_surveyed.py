# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from numpy import where, ones, logical_and, array, median, resize, abs
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

class MysqlStorage:
    def get(self, database):
        db_config = ScenarioDatabaseConfiguration()
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(database)

        storage = StorageFactory().get_storage('sql_storage',
                                               storage_location = db)
        return storage

def groupBy(table, groups, func, where, func_column=''):
    tmp_dict = {}
    if (func_column) > 0:
        values = []
    for row in table.where(where):
        key = tuple([row[field] for field in groups])
        if len(func_column) > 0:
            value = row[func_column]
        else:
            value = row[groups[0]]
        if tmp_dict.has_key(key):
            tmp_dict[key].append(value)
        else:
            tmp_dict[key] = [value]

    for key, values in tmp_dict.iteritems():
        tmp_dict[key]=func(values)

    return tmp_dict

if __name__ == '__main__':
    #import wingdbstub
    from opus_core.simulation_state import SimulationState
    from opus_core.session_configuration import SessionConfiguration
    from opus_core.datasets.dataset import Dataset
    from opus_core.store.attribute_cache import AttributeCache
    from tables import openFile
    #from tables import *
    from opus_core.sampling_toolbox import sample_noreplace

    load_data_to_pytables = False
    assign_job_to_workers = False
    load_pytables_to_mysql = True

    cache_directory = "/urbansim_cache/psrc_parcel/runs/cache_source"
    base_year = 2000
    input_database_name = 'psrc_2005_parcel_baseyear_data_prep_2006_survey'
    instorage = MysqlStorage().get(input_database_name)

    h5file_name = "/home/lmwang/playground/y2000_test.h5"
    if load_data_to_pytables:
        print "Load data to pytables..."
        SimulationState().set_cache_directory(cache_directory)
        SimulationState().set_current_time(base_year)
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim', 'opus_core'],
                             in_storage=attribute_cache)    
        dataset_pool = SessionConfiguration().get_dataset_pool()

        jobs = dataset_pool.get_dataset('job')
        jobs.compute_variables(["urbansim_parcel.job.parcel_id", "urbansim_parcel.job.zone_id"])

        workers = Dataset(in_storage = instorage,
                          in_table_name="workers_surveyed",
                          id_name="person_id", 
                          dataset_name="person")

        # Open a file in "w"rite mode
        h5file = openFile(h5file_name, mode = "w", title = "Test file")
        # Create a new group under "/" (root)
        y2000 = h5file.createGroup("/", 'y'+str(base_year), 'Year 2000 data')

        tjobs = jobs.createTable(h5file, y2000)
        tworkers = workers.createTable(h5file, y2000, name="workers_surveyed")
        #tworkers_sum = persons_for_estimatoin_summary.createTable(h5file, y2000, name="persons_for_estimation_summary")

        h5file.flush()
        #import sys
        #sys.exit(0)
    else:
        h5file = openFile(h5file_name, mode = "a")
        # Create a new group under "/" (root)

        tjobs = h5file.root.y2000.jobs
        tworkers = h5file.root.y2000.workers_surveyed

    if assign_job_to_workers:
        print "Assign job to workers..."
        match_sequences = ['building_id', 'parcel_id', 'sector_id', 'zone_id', 'building_type']
        max_iterations = 4

        assigned_workers = [worker.nrow for worker in tworkers.where('job_id>0')]
        assigned_jobs = [tworkers.cols.job_id[row] for row in assigned_workers]

        #i = 1
        for iteration in range(max_iterations):
            workers_summary_by_group = groupBy(tworkers, match_sequences[iteration:], len, where='job_id<0')
            for attr, num in workers_summary_by_group.iteritems():
                print attr, 
                condition = "&".join([ '(%s==%s)' % (n, v) for n, v in zip(match_sequences[iteration:], attr) ])
                matched_workers = [person.nrow for person in tworkers.where(condition) if person['job_id'] < 0] 
                matched_jobs = [job['job_id'] for job in tjobs.where(condition) if (array(assigned_jobs)==job['job_id']).sum()== 0]
                print '[w%s:j%s]' % ( len(matched_workers), len(matched_jobs) ),
                assert num == len(matched_workers)
                if len(matched_jobs) >= num:
                    tmp_jobs = sample_noreplace(array(matched_jobs), len(matched_workers)).tolist()
                    tmp_workers = matched_workers
                elif len(matched_jobs) > 0:
                    tmp_jobs = matched_jobs
                    tmp_workers = sample_noreplace(array(matched_workers), len(matched_jobs)).tolist()
                else:
                    print '.'
                    continue
                print '(w%s:j%s)' % ( len(tmp_workers), len(tmp_jobs) ),
                print '.'
                assigned_jobs += tmp_jobs
                assigned_workers += tmp_workers

            for i in range(len(assigned_workers)):
                tworkers.cols.job_id[assigned_workers[i]]  = assigned_jobs[i]
            print "%s jobs assigned to workers with matching %s " % (len(assigned_workers), match_sequences[iteration:])
            tworkers.flush()

    if load_pytables_to_mysql:
        print "Load pytables to mysql..."
        output_database_name = input_database_name
        outstorage = MysqlStorage().get(output_database_name)

        data_dict = {}
        dict_storage = StorageFactory().get_storage('dict_storage')
        table_name = 'workers_surveyed_assigned'
        for colname in tworkers.colnames:
            data_dict[colname] = tworkers.cols._f_col(colname)[:]
        dict_storage.write_table( table_name=table_name, table_data=data_dict )
        dataset = Dataset( in_storage=dict_storage, in_table_name=table_name, id_name='person_id' )
        dataset.write_dataset(out_storage=outstorage, out_table_name=table_name)
