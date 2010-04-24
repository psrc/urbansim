# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# Test that the washtenaw parcel simulation runs without crashing for 3 years using an xml configuration

import os
from subprocess import Popen, PIPE
from opus_core.tests import opus_unittest
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed

class TestSimulation(opus_unittest.OpusIntegrationTestCase):
    """ this integration test checks and downloads a zipped cache from semcog ftp,
        unzip, and run washtenaw_parcel for 3 years
    """
    def setUp(self):
        self.opus_home = os.environ["OPUS_HOME"]
        self.data_path = os.path.join(self.opus_home, 'data', 'washtenaw_parcel')
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
    
    def tearDown(self):
        runs_path = os.path.join(self.data_path, 'runs')
        stderr = Popen( "rm -rf %s" % runs_path,
                        stderr=PIPE ).communicate()[0]
        if stderr:
            raise RuntimeError( "Error when deleting runs directory %s: %s" % (runs_path, stderr) )
    
    def test_simulation(self):
        base_year_data_path = os.path.join(self.data_path, 'base_year_data')        

        ftp_url = os.environ["FTP_URL"]
        file_name = os.path.split(ftp_url)[1]
        ftp_user = os.environ["FTP_USERNAME"]
        ftp_password = os.environ["FTP_PASSWORD"]
        
        stderr = Popen( """
                        cd %s; 
                        wget --timestamping %s --ftp-user=%s --ftp-password=%s;
                        rm -rf 2008;
                        unzip -o %s
                        """ % (base_year_data_path, ftp_url, ftp_user, ftp_password, file_name),
                        stderr=PIPE ).communicate()[0]
        if stderr:
            raise RuntimeError( "Error when downloading and unzipping file from %s: %s" % (ftp_url, stderr) )
                
        run_manager = RunManager()
        run_as_multiprocess = True
        xml_config = XMLConfiguration(os.path.join(self.opus_home, 'project_configs', 'washtenaw_parcel.xml'))
        for scenario_name in ['washtenaw_parcel']:
            config = xml_config.get_run_configuration(scenario_name)
            insert_auto_generated_cache_directory_if_needed(config)
            base_year = config['base_year']
            config['years_to_run'] = (base_year+1, base_year+4) 
            run_manager.setup_new_run(cache_directory = config['cache_directory'],
                                      configuration = config)
            run_manager.run_run(config, run_as_multiprocess = run_as_multiprocess)
                       
if __name__ == "__main__":
    opus_unittest.main()