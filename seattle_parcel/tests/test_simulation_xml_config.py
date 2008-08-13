#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# Test that the Seattle parcel simulation runs without crashing for 2 years using an xml configuration

from opus_core.tests import opus_unittest
from opus_core.tools.start_run import StartRunOptionGroup
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from seattle_parcel.tests.test_xml_config_setup import TestXMLConfigSetup
from opus_core.services.run_server.run_manager import RunManager

class TestSimulation(TestXMLConfigSetup):
           
    def test_simulation(self):
        # check that the simulation proceeds without crashing
        xml_config = self.get_xml_config()
        option_group = StartRunOptionGroup()
        parser = option_group.parser
        # simulate 0 command line arguments by passing in []
        (options, _) = parser.parse_args([])
        run_manager = RunManager(options)
        run_section = xml_config.get_run_configuration('Seattle_baseline')
        insert_auto_generated_cache_directory_if_needed(run_section)
        run_manager.setup_new_run(cache_directory = run_section['cache_directory'])
        run_manager.run_run(run_section)
       
if __name__ == "__main__":
    opus_unittest.main()