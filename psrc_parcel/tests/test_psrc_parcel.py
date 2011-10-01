# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# Test that the washtenaw parcel simulation runs without crashing for 3 years using an xml configuration

import os
from subprocess import Popen, PIPE
from opus_core.tests import opus_unittest
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from urbansim.estimation.estimation_runner import EstimationRunner
from opus_core import paths

class TestSimulation(opus_unittest.OpusIntegrationTestCase):
    """ this integration test runs san_antonio_baseline_test in project_configs/psrc_parcel_test.xml
    """
    def setUp(self):
        """
        set up opus data path, a base_year_data cache directory needs to exists 
        or be created through downloading and unzipping etc
        
        """
        self.opus_home = paths.OPUS_HOME
        self.data_path = paths.get_opus_data_path_path('psrc_parcel')
        
        self.xml_config = XMLConfiguration(os.path.join(self.opus_home, 'project_configs', 'psrc_parcel_test.xml'))
        
        base_year_data_path = os.path.join(self.data_path, 'base_year_data')        
        if not os.path.exists(base_year_data_path):
            os.makedirs(base_year_data_path)

#        ftp_url = os.environ["FTP_URL"]
#        file_name = os.path.split(ftp_url)[1]
#        ftp_user = os.environ["FTP_USERNAME"]
#        ftp_password = os.environ["FTP_PASSWORD"]
#
#        try:
#            Popen( """
#                        cd %s;
#                        pwd;
#                        ls -la;
#                        echo wget --timestamping %s --ftp-user=%s --ftp-password=%s > /dev/null 2>&1;
#                        rm -rf 2008;
#                        unzip -o %s
#                        """ % (base_year_data_path, ftp_url, ftp_user, ftp_password, file_name),
#                        shell = True
#                        ).communicate()
#        except:
#            print "Error when downloading and unzipping file from %s." % ftp_url
#            raise            
    
    def tearDown(self):
        """
        delete [project_name]/runs directory to free up disk space
        """
        runs_path = os.path.join(self.data_path, 'runs')
        #if os.path.exists(runs_path):
        #    Popen( "rm -rf %s" % runs_path, shell=True)

    def test_estimation(self):
        for model_name in ['residential_building_type_choice_model', 
                           'tenure_choice_model', 
                           'work_at_home_choice_model',
                           'workplace_choice_model_for_resident',
                           'auto_ownership_choice_model',
                           'hbw_mode_choice_model',
                           'real_estate_price_model',
                           'household_location_choice_model',
                           'shopping_destination_choice_model',
                           ('employment_location_choice_model', 'home_based'),
                           ('employment_location_choice_model', 'non_home_based')
                           ]:
            if type(model_name)==tuple:
                model_name, group_member = model_name
            else:
                group_member = None        
                
            estimator = EstimationRunner(model=model_name,  
                                         model_group=group_member,
                                         xml_configuration=self.xml_config,
                                         configuration = None
                                         )
            estimator.estimate()
                            
    def test_simulation(self):
        services_db = ServicesDatabaseConfiguration( database_name = 'services',                         
                                                     database_configuration = 'services_database_server' )
        run_manager = RunManager(services_db)
        run_as_multiprocess = True
        for scenario_name in ['psrc_baseline_test']:
            config = self.xml_config.get_run_configuration(scenario_name)
            insert_auto_generated_cache_directory_if_needed(config)
            run_manager.setup_new_run(cache_directory = config['cache_directory'],
                                      configuration = config)
            run_manager.run_run(config, run_as_multiprocess = run_as_multiprocess)
        
                       
if __name__ == "__main__":
    opus_unittest.main()
