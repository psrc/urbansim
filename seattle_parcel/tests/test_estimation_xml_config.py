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

# Test that the Seattle parcel simulation runs without crashing for 2 years using an xml configuration

from opus_core.tests import opus_unittest
from urbansim.estimation.estimation_runner import EstimationRunner
from seattle_parcel.tests.test_xml_config_setup import TestXMLConfigSetup

class TestEstimation(TestXMLConfigSetup):
    
    def test_estimation(self):
        xml_config = self.get_xml_config()
        estimation_section = xml_config.get_section('model_manager/estimation')
        estimation_config = estimation_section['estimation_config']
        for model_name in estimation_config['models_to_estimate']:
            if type(model_name) == dict:
                for name, group_members in model_name.items():
                    er = EstimationRunner(model=name, 
                                          xml_configuration=xml_config, 
                                          model_group = group_members['group_members'],
                                          configuration=None)
                    er.estimate()
            else:
                er = EstimationRunner(model=model_name, xml_configuration=xml_config, configuration=None)
                er.estimate()
       
if __name__ == "__main__":
    opus_unittest.main()