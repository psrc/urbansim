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
#

import getpass
from numpy.random import seed, randint
from opus_core.misc import load_table_from_text_file, write_table_to_text_file
from opus_core.misc import get_config_from_opus_path
from opus_core.logger import logger
from remote_run_controller import RemoteRunOptionGroup
from remote_run_controller import RemoteRun
from opus_core.services.run_server.run_activity import RunActivity
from urbansim.tools.run_manager import RunManager

class RemoteRunSetOptionGroup(RemoteRunOptionGroup):
    def __init__(self):
        RemoteRunOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control set of urbansim and travel model runs to run on different computers.")
        self.parser.add_option("--run-id-file", dest="run_id_file", default=None, 
                               help="File with run_ids of the set. None means new set will be started.")
        
class RemoteRunSet(RemoteRun):
    default_run_id_file = 'run_ids'
    
    def prepare_for_run(self, configuration_path, run_id_file=None, **kwargs):
        self.run_ids_dict = {} # dict of run_id and finished year
        if run_id_file is None:
            config = get_config_from_opus_path(configuration_path)
            self.number_of_runs = config.get("number_of_runs", 1)
            root_seed = config.get("seed", 1)
            seed(root_seed)
            # generate different seed for each run (each seed contains 1 number)
            seed_array = randint(1,2**30, self.number_of_runs)
            for irun in range(self.number_of_runs):
                config['seed']= (seed_array[irun],)
                RemoteRun.prepare_for_run(self, config=config)
                self.run_ids_dict[self.run_id] = 0
            self.run_id_file = self.default_run_id_file
        else:
            self.read_run_id_file(run_id_file)
            self.run_id_file = run_id_file
            run_activity = RunActivity(self.services_database)
            self.run_manager = RunManager(run_activity)
        return None
            
    def run(self, start_year, end_year, configuration_path, run_id_file=None):
        self.prepare_for_run(configuration_path=configuration_path, run_id_file=run_id_file)    
        self._do_run(start_year, end_year)
        
    def read_run_id_file(self, filename):
        # filename is a file with a pair (run_id, year) per row
        content = load_table_from_text_file(filename, convert_to_float=True)[0]
        for run_id, year in content:
            self.run_ids_dict[int(run_id)] = int(year)
        
    def _do_run(self, start_year, end_year, *args, **kwargs):
        logger.log_status("run_id_file: %s" % self.run_id_file)
        for run_id, finished_year in self.run_ids_dict.iteritems():
            self.run_id = run_id
            config = self.run_manager.get_resources_for_run_id_from_history(services_host_name=self.services_hostname,
                                                                       services_database_name=self.services_dbname,
                                                                       run_id=self.run_id)
            if start_year is None:
                this_start_year = config['years'][0]
            else:
                this_start_year = start_year
            RemoteRun._do_run(self, max(this_start_year, finished_year+1), end_year, config)
            self.run_ids_dict[self.run_id] = self.get_urbansim_last_year(config)
            self.write_into_run_id_file()
            
    def write_into_run_id_file(self):
        result = array(map(lambda(x,y): [x,y], self.run_ids_dict.iteritems()))
        write_table_to_text_file(self.run_id_file, result)
        
if __name__ == "__main__":
    option_group = RemoteRunSetOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if options.server is None:
        hostname = raw_input('Hostname [%s]: ' % RemoteRunSet.default_hostname)
        if len(hostname) == 0:
            hostname = RemoteRun.default_hostname
    else:
        hostname = options.server
    if options.user is None:
        username = raw_input('Username [%s]: ' % RemoteRunSet.default_username)
        if len(username) == 0:
            username = RemoteRun.default_username
    else:
        username = options.user
    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    try: import wingdbstub
    except: pass
    db = option_group.get_services_database(options)
    run = RemoteRunSet(hostname, username, password, options.host_name, options.database_name, db,
                       options.skip_travel_model, options.skip_urbansim)
    run.run(options.start_year, options.end_year, options.configuration_path, options.run_id_file)
        