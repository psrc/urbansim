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
from opus_core.table_type_schema import TableTypeSchema
from opus_core.services.run_server.run_state import RunState

class AvailableRuns(object):
    """ keeps a list of available runs. Available runs means that the simulation
    has completed and there's data about the run in the cache"""
    
    def __init__(self, storage):
        self.storage = storage
        if not self.storage.table_exists("available_runs"):
            tt_schema = TableTypeSchema()
            self.storage.create_table(
                "available_runs", 
                tt_schema.get_table_schema("available_runs"))
    
    def close_connection(self):
        self.storage.close()
        
    def add_run(self,run_id,info,status):
        """ adds this information to the available_runs table (or updates info if something with same
            run_id is already there)"""
        
        run_state = RunState(self.storage).set_run_state(run_id,info,status)
        
    def delete_everything_for_this_run(self,run_id):
        """ removes the entire tree structure along with information """
        run_state = RunState(self.storage).get_run_state(run_id)
        
        cache_dirname = run_state['full_cache_dirname']
        shutil.rmtree(cache_dirname,onerror = self._handle_deletion_errors)
        
        while os.path.exists(cache_dirname):
            shutil.rmtree(cache_dirname)
        
        available_runs = self.storage.get_table('available_runs')
        query = available_runs.delete(available_runs.c.run_id==int(run_id))
        self.storage.engine.execute(query)
           
    def delete_year_dirs_in_cache(self, run_id, years_to_delete=None):
        """ only removes the years cache and leaves the indicator, changes status to partial"""
        run_state = RunState(self.storage).get_run_state(run_id)
        cache_dirname = run_state['full_cache_dirname']
        if years_to_delete is None:
            years_to_delete = run_state['years']
            
        for year in years_to_delete:            
            year_dir = os.path.join(cache_dirname, str(year))
            while os.path.exists(year_dir ):
                shutil.rmtree(year_dir, onerror=self._handle_deletion_errors)
        import sets
        years_cached = list(sets.Set(run_state['years']).difference(years_to_delete))
        run_state.change_years_cached(years_cached)
    
    def _handle_deletion_errors(self,function,path,info):
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

        
    def get_run_with_run_id(self,run_id):
        """ retrieve this scenario from cache"""
        return RunState(self.storage).get_run_state(run_id)

    def has_run(self,run_id):
        """ return True iff this run is available"""
        from sqlalchemy.sql import select
        available_runs = self.storage.get_table('available_runs')
                
        query = select(
            columns = [available_runs.c.run_id],
            whereclause = available_runs.c.run_id==int(run_id))

        exists = len(self.storage.engine.execute(query).fetchall()) > 1
        
        return exists

    def update_status_for_run(self,run_id,status):
        """ updates status on the database"""
        available_runs = self.storage.get_table('available_runs')
        values = {available_runs.c.status:status}
        query = available_runs.update(
            available_runs.c.run_id==int(run_id),
            values = values)
        self.storage.engine.execute(query)        

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
