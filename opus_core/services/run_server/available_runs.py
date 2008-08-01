#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os, pickle, shutil, sys

from opus_core.logger import logger
from opus_core.services.run_server.run_state import RunState
from sqlalchemy.sql import select
from opus_core.general_resources import GeneralResources
from opus_core.configuration import Configuration


#TODO: eliminate hard coded drive labels 
def _get_full_cache_dirname(cache_directory, processor_name):
    """ returns the full path for this indicators directory (e.g.\\server_name\cache_dir_name\run_name)"""
    
    indicator_cache = cache_directory
    if indicator_cache.startswith("d:/"):
        indicator_cache =  indicator_cache.replace("d:/",'\\\%s\\d_' %processor_name)
    elif indicator_cache.startswith("c:/") or indicator_cache.startswith("C:/"):
        indicator_cache =  indicator_cache.replace("c:/",'\\\%s\\c_' % processor_name)
        indicator_cache =  indicator_cache.replace("C:/",'\\\%s\\c_' % processor_name)           
    return indicator_cache

    
class AvailableRuns(object):
    """ keeps a list of available runs. Available runs means that the simulation
    has completed and there's data about the run in the cache"""
    
    def __init__(self, storage):
        self.services_database = storage
        self.run_state = RunState(self.services_database)
        self.resources = GeneralResources()
        
    def close_connection(self):
        self.services_database.close()
        
    def add_run(self, run_id, info, status):
        """ adds this information to the available_runs table (or updates info if something with same
            run_id is already there)"""

        db_name = ''
        host_name = ''

        if 'input_configuration' in info.keys():
            db_name = info['input_configuration'].database_name
            host_name = info['input_configuration'].host_name
            
        resources = {'config' : info,
                    'status' :status,
                    'run_id' : run_id,
                    'models' :info.get('models',[]),
                    'db_input_database': db_name,
                    'db_host_name' : host_name,
                    'base_year': info['base_year']}

        resources['years'] = info.get('years_run', [])
        resources['end_year'] = info.get('end_year', None)
             
        run_activity = self.services_database.get_table('run_activity')
        query = select(
            columns = [run_activity.c.processor_name,
                       run_activity.c.run_name],
            whereclause = run_activity.c.run_id==run_id               
        )
        results = self.services_database.engine.execute(query).fetchone()
        resources['processor_name'] = results[0]
        resources['run_name'] = results[1]        
        resources['full_cache_dirname'] = _get_full_cache_dirname(
            info['cache_directory'],
            resources['processor_name'])    

        self.status = status
        
        pickled_info = pickle.dumps(resources)
        self.resources.update(resources)  
        
        available_runs = self.services_database.get_table('available_runs')
                
        query = select(
            columns = [available_runs.c.run_id],
            whereclause = available_runs.c.run_id==int(self.run_id))

        exists = self.services_database.engine.execute(query).fetchone() is not None
        
        if exists:
            values = {
                available_runs.c.info: pickled_info,
                available_runs.c.status: self.status
            }
            
            query = available_runs.update(
                whereclause = available_runs.c.run_id == int(self.run_id),
            )

        else:
            values = {
                available_runs.c.run_id: run_id,
                available_runs.c.info: pickled_info,
                available_runs.c.status: self.status
            }
            query = available_runs.insert()
            
        try:
            import pydevd;pydevd.settrace()
        except:
            pass
        
        print self.services_database, self.services_database.get_connection_string()
        self.services_database.engine.execute(query, values = values)

    def get_run_state(self, run_id):
        """ get row from available runs """
        
        available_runs = self.services_database.get_table('available_runs')
        query = select(
            columns = [available_runs.c.info,
                       available_runs.c.status],
            whereclause = available_runs.c.run_id==int(run_id))
        
        info, self.status = self.services_database.engine.execute(query).fetchone()
        self.resources.update(Configuration(pickle.loads(info)))
           
    def delete_everything_for_this_run(self, run_id):
        """ removes the entire tree structure along with information """
        self.run_state.get_run_state(run_id)
        
        cache_dirname = self.run_state['full_cache_dirname']
        shutil.rmtree(cache_dirname,onerror = self._handle_deletion_errors)
        
        while os.path.exists(cache_dirname):
            shutil.rmtree(cache_dirname)
        
        available_runs = self.services_database.get_table('available_runs')
        query = available_runs.delete(available_runs.c.run_id==int(run_id))
        self.services_database.engine.execute(query)
           
    def delete_year_dirs_in_cache(self, run_id, years_to_delete=None):
        """ only removes the years cache and leaves the indicator, changes status to partial"""
        self.run_state.get_run_state(run_id)
        cache_dirname = self.run_state['full_cache_dirname']
        if years_to_delete is None:
            years_to_delete = self.run_state['years']
            
        for year in years_to_delete:            
            year_dir = os.path.join(cache_dirname, str(year))
            while os.path.exists(year_dir ):
                shutil.rmtree(year_dir, onerror=self._handle_deletion_errors)

        years_cached = [year for year in self.run_state['years'] if year not in years_to_delete]
        self._update_years_cached(years_cached, run_id)

    def _update_years_cached(self, years_cached, run_id):
        """Changes set of years cached, and sets status to 'partial'.
        """
        self.status = "partial"
        self['years']  = years_cached
        copy  =self.copy()
        pickled_info = pickle.dumps(copy)  
        
        available_runs = self.services_database.get_table('available_runs')

        values = {
            available_runs.c.info: pickled_info,
            available_runs.c.status: self.status
        }
        
        query = available_runs.update(
            whereclause = available_runs.c.run_id == int(run_id),
            values = values
        )
        
        self.services_database.engine.execute(query)
                                         
    def _handle_deletion_errors(self, function, path, info):
        """try to close the file if it's a file """
        logger.log_warning("in AvailableRuns._handle_deletion_errors: Trying  to delete %s error from function %s: \n %s" % (path,function.__name__,info[1]))
        if function.__name__ == 'remove':
            try:
                logger.disable_all_file_logging()
                file = open(path)
                file.close()
                os.remove(path)
            except:
                logger.log_warning("in AvailableRuns._handle_deletion_errors:unable to delete %s error from function %s: \n %s" % (path,function.__name__,info[1]))
        else:
            logger.log_warning("in AvailableRuns._handle_deletion_errors:unable to delete %s error from function %s: \n %s" % (path,function.__name__,info[1]))

    def has_run(self, run_id):
        """ return True iff this run is available"""
        available_runs = self.services_database.get_table('available_runs')
                
        query = select(
            columns = [available_runs.c.run_id],
            whereclause = available_runs.c.run_id==int(run_id))

        exists = self.services_database.engine.execute(query).fetchone() is not None
        
        return exists

    def get_all_runs(self):
        """Return all run_ids in available runs."""
        from sqlalchemy.sql import select
        available_runs = self.services_database.get_table('available_runs')
                
        query = select(
            columns = [available_runs.c.run_id])
        return self.services_database.engine.execute(query).fetchall()
    
    def update_status_for_run(self, run_id, status):
        """ updates status on the database"""
        available_runs = self.services_database.get_table('available_runs')
        values = {available_runs.c.status:status}
        query = available_runs.update(
            available_runs.c.run_id==int(run_id),
            values = values)
        self.services_database.engine.execute(query)        

from opus_core.tests import opus_unittest

class  AvailableRunsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    ### TODO:
    def test_close_connection(self):
        pass
        
    ### TODO:
    def test_add_run(self):
        pass
        
    ### TODO:
    def test_delete_everything_for_this_run(self):
        pass
    
    ### TODO:
    def test_delete_year_dirs_in_cache(self):
        pass
    
    ### TODO:
    def test_handle_deletion_err(self):
        pass
        
    ### TODO:
    def test_get_run_with_run_id(self):
        pass

    ### TODO:    
    def test_has_run(self):
        pass
        
    ### TODO:
    def test_update_status_for_run(self):
        pass


if __name__ == "__main__":
    opus_unittest.main()
