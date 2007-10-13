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

import pickle
from opus_core.general_resources import GeneralResources
from opus_core.configuration import Configuration
from sqlalchemy.sql import select

class RunState(GeneralResources):
    """ Object that centralizes data about each run """

    def __init__(self,database):
        """ initialize a run state object with the given run_id and info resources"""
        self.database = database
        
    def set_run_state(self,run_id,info,status):
        """ add row to available_runs """
        if 'input_configuration' in info.keys():
            db_name = info['input_configuration'].database_name
            host_name = info['input_configuration'].host_name
        else:
            db_name = ''
            host_name = ''
        resources = {'config' : info,
                    'status' :status,
                    'run_id' : run_id,
                    'models' :info.get('models',[]),
                    'db_input_database': db_name,
                    'db_host_name' : host_name,
                    'base_year': info['base_year']}
        if info.has_key('years_run'):
            resources['years'] = info['years_run']
        else:
            resources['years'] = []
        
        if info.has_key('end_year'):
            resources['end_year'] =  info['end_year'] 
        else:
            resources['end_year'] =  None
             
        run_activity = self.database.get_table('run_activity')
        query = select(
            columns = [run_activity.c.processor_name,
                       run_activity.c.run_name],
            whereclause = run_activity.c.run_id==run_id               
        )
        results = self.database.engine.execute(query).fetchone()
        resources['processor_name'] = results[0]
        resources['run_name'] = results[1]        
        resources['full_cache_dirname'] = self.get_full_cache_dirname(
            info['cache_directory'],
            resources['processor_name'])    

        self.status = status
        self.run_id = run_id
        
        pickled_info = pickle.dumps(resources)
        self.update(resources)  
        
        available_runs = self.database.get_table('available_runs')
                
        query = select(
            columns = [available_runs.c.run_id],
            whereclause = available_runs.c.run_id==int(self.run_id))

        exists = len(self.database.engine.execute(query).fetchall()) > 1
        
        if exists:
            values = {
                available_runs.c.info: pickled_info,
                available_runs.c.status: self.status
            }
            
            query = available_runs.update(
                whereclause = available_runs.c.run_id == int(self.run_id),
                values = values
            )

        else:
            values = {
                available_runs.c.run_id: run_id,
                available_runs.c.info: pickled_info,
                available_runs.c.status: self.status
            }
            query = available_runs.insert(
                values = values           
            )
            
        self.database.engine.execute(query)

        #TODO: return self? this doesn't make too much sense...
        return self

    def get_run_state(self,run_id):
        """ get row from available runs """
        
        available_runs = self.database.get_table('available_runs')
        query = select(
            columns = [available_runs.c.info,
                       available_runs.c.status],
            whereclause = available_runs.c.run_id==int(run_id))
        
        info, self.status = self.database.engine.execute(query).fetchone()
        self.run_id = run_id
        self.update(Configuration(pickle.loads(info)))
        return self

    def change_years_cached(self,years_cached):
        """Changes set of years cached, and sets status to 'partial'.
        """
        self.status = "partial"
        self['years']  = years_cached
        copy  =self.copy()
        pickled_info = pickle.dumps(copy)  
        
        available_runs = self.database.get_table('available_runs')

        values = {
            available_runs.c.info: pickled_info,
            available_runs.c.status: self.status
        }
        
        query = available_runs.update(
            whereclause = available_runs.c.run_id == int(self.run_id),
            values = values
        )
        
        self.database.engine.execute(query)
        
    def _get_years_available_in_cache(self,years,cache_dirname,processor_name):    
        """ Returns the subset of these years that actually have a directory in their respective
            indicator caches
        """
        
        dir = self.get_full_cache_dirname(cache_dirname,processor_name)
        final_years = []
        years.sort()
        # add base year
        years.insert(0,years[0] -1)
        for year in years:
            if os.path.exists(os.path.join(dir,str(year))):
                final_years.append(year)
        return final_years
 
    def get_full_cache_dirname(self,cache_directory,processor_name):
        """ returns the full path for this indicators directory (e.g.\\server_name\cache_dir_name\run_name)"""
        
        indicator_cache = cache_directory
        if indicator_cache.startswith("d:/"):
            indicator_cache =  indicator_cache.replace("d:/",'\\\%s\\d_' %processor_name)
        elif indicator_cache.startswith("c:/") or indicator_cache.startswith("C:/"):
            indicator_cache =  indicator_cache.replace("c:/",'\\\%s\\c_' % processor_name)
            indicator_cache =  indicator_cache.replace("C:/",'\\\%s\\c_' % processor_name)           
        return indicator_cache


import os
from opus_core.tests import opus_unittest


class RunStateTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
       
    ### TODO: 
    def tearDown(self):
        pass

    ### TODO:
    def test_set_run_state(self):
        pass
        
    ### TODO:
    def test_get_run_state(self):
        pass
        
    ### TODO:
    def test_change_years_cached(self):
        pass
        
    ### TODO:
    def test_get_years_available_in_cache(self):
        pass
    
    ### TODO:
    def test_get_full_cache_dirname(self):
        pass


if __name__ == "__main__":
    opus_unittest.main()