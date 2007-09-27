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

import os, pickle, sys
from time import localtime, strftime, time

from opus_core.misc import get_host_name
from opus_core.services.run_server.available_runs import AvailableRuns
from sqlalchemy.sql import insert

class RunActivity(object):
    """Abstraction that represents a log of the run runs and information about when/where 
    they were run, how they did, etc """
    
    def __init__(self, storage=None):
        self.storage = storage
        self.available_runs = AvailableRuns(self.storage)
            
    def set_storage(self, storage):
        self.storage = storage    
        
    def get_storage(self):
        return self.storage
        
    def get_new_history_id(self):
        """Returns a unique run_id for a new run_activity trail."""
        last_id = self.storage.GetResultsFromQuery("SELECT MAX(run_id) FROM run_activity")
        
        if last_id[1][0]:
            run_id = int(last_id[1][0]) + 1
        else:
            run_id = 1

        return run_id

    def add_row_to_history(self, history_id, resources, status):
        """update the run history table to indicate changes to the state of this run history trail."""
        
        if not status:
            raise "un-specified status"
        
        resources['run_id'] = history_id
        
        pickled_resources = 'NULL'
        if resources is not None:
            pickled_resources = pickle.dumps(resources)
                             
        values = {"run_id":history_id, 
             "run_name":"'%s'" % resources.get('description', "No description"),
             "status":"'%s'" % status,
             "processor_name":"'%s'" % get_host_name(), 
             "date_time":strftime("'%Y-%m-%d %H:%M:%S'", localtime()),
             "resources":"'%s'" % pickled_resources,
             }        

        run_activity_table = self.storage.get_table('run_activity')
        qry = run_activity_table.insert(values = values)
        self.storage.engine.execute(qry)
    

        if self.available_runs.has_run(history_id):
            self.available_runs.update_status_for_run(history_id,status)
        else:
            self.available_runs.add_run(history_id,resources,status)
    