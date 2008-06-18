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

# Test that the Seattle parcel estimates correctly for the real estate price model, and that the
# simulation runs without crashing for 2 years using an xml configuration

import os
from opus_core.tests import opus_unittest
import tempfile
from shutil import rmtree
from opus_core.tools.start_run import StartRunOptionGroup
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.configurations.xml_configuration import XMLConfiguration
from urbansim.estimation.estimation_runner import EstimationRunner

# This is a template for an xml configuration for running the test -- it runs for 2 years (sometimes
# the default is 1 year), and there is a bit in it where we will substitute the 
# temp directory into which to write the results.
config_template = """<opus_project>
  <general>
    <parent type="file">seattle_parcel/configs/seattle_parcel.xml</parent>
    </general>
  <scenario_manager>
    <Seattle_baseline copyable="True" executable="True" setexpanded="True" type="scenario">
      <years_to_run config_name="years" type="tuple">
        <endyear type="integer">2002</endyear>
      </years_to_run>
      <creating_baseyear_cache_configuration type="class">
        <cache_directory_root parser_action="prefix_with_opus_data_path" type="directory">%s/runs</cache_directory_root>
        </creating_baseyear_cache_configuration>
      </Seattle_baseline>
  </scenario_manager>
</opus_project>
"""


class EstimationAndSimulationTest(opus_unittest.OpusTestCase):
    
    def setUp(self):
        # By putting the creation and removal of the temp_dir in the setUp and tearDown methods, we ensure that it 
        # gets removed even if test_estimation, test_simulation, or the helper method _get_xml_config gets an exception.
        # Note that mkdtemp returns an absolute directory path.
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
    def tearDown(self):
        rmtree(self.temp_dir)
        
    def test_estimation(self):
        xml_config = self._get_xml_config()
        estimation_section = xml_config.get_section('model_manager/estimation')
        estimation_config = estimation_section['estimation_config']
        for model_name in estimation_config['models_to_estimate']:
            er = EstimationRunner(model=model_name, xml_configuration=xml_config, configuration=None)
            er.estimate()
           
    def test_simulation(self):
        # check that the simulation proceeds without crashing
        xml_config = self._get_xml_config()
        option_group = StartRunOptionGroup()
        parser = option_group.parser
        # simulate 0 command line arguments by passing in []
        (options, _) = parser.parse_args([])
        run_manager = option_group.get_run_manager(options)
        run_section = xml_config.get_run_configuration('Seattle_baseline')
        insert_auto_generated_cache_directory_if_needed(run_section)
        run_manager.setup_new_run(run_name = run_section['cache_directory'])
        run_manager.run_run(run_section)
       
    def _get_xml_config(self):
        # Return the xml configuration to run these unit tests.
        # We don't want to do this in the setup method, since if XMLConfiguration gets an exception we still want to
        # delete the temp directory on teardown.
        # generate an xml configuration to run the test (we want to write the results into the temp directory).
        config_path = os.path.join(self.temp_dir, 'testconfig.xml')
        f = open(config_path, 'w')
        f.write(config_template % self.temp_dir)
        f.close()
        return XMLConfiguration(config_path)
        
if __name__ == "__main__":
    opus_unittest.main()