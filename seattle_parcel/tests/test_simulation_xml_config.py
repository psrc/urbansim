# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# Test that the Seattle parcel simulation runs without crashing for 2 years using an xml configuration

import os
from opus_core.tests import opus_unittest
from opus_core.tools.start_run import StartRunOptionGroup
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.services.run_server.run_manager import RunManager
from opus_core.configurations.xml_configuration import XMLConfiguration


class TestSimulation(opus_unittest.OpusIntegrationTestCase):
           
    def test_simulation(self):
        # check that the simulation proceeds without crashing
        # open the configuration for seattle_parcel.xml
        seattle_parcel_dir = __import__('seattle_parcel').__path__[0]
        xml_config = XMLConfiguration(os.path.join(seattle_parcel_dir, 'configs', 'seattle_parcel.xml'))
        option_group = StartRunOptionGroup()
        parser = option_group.parser
        # simulate 0 command line arguments by passing in []
        (options, _) = parser.parse_args([])
        run_manager = RunManager(option_group.get_services_database_configuration(options))
        run_section = xml_config.get_run_configuration('Seattle_baseline')
        insert_auto_generated_cache_directory_if_needed(run_section)
        run_manager.setup_new_run(cache_directory = run_section['cache_directory'],
                                  configuration = run_section)
        run_manager.run_run(run_section)
       
if __name__ == "__main__":
    opus_unittest.main()