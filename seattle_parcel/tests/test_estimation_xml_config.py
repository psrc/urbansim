# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# Test that the Seattle parcel simulation runs without crashing for 2 years using an xml configuration

import os
from opus_core.tests import opus_unittest
from opus_core.configurations.xml_configuration import XMLConfiguration
from urbansim.estimation.estimation_runner import EstimationRunner

class TestEstimation(opus_unittest.OpusIntegrationTestCase):
    
    def test_estimation(self):
        # open the configuration for seattle_parcel.xml
        seattle_parcel_dir = __import__('seattle_parcel').__path__[0]
        xml_config = XMLConfiguration(os.path.join(seattle_parcel_dir, 'configs', 'seattle_parcel.xml'))

        for model_name in ['real_estate_price_model', 
                           'household_location_choice_model']:
            er = EstimationRunner(model=model_name, xml_configuration=xml_config, configuration=None)
            er.estimate()
        
        # test run with group members
        er = EstimationRunner(model='employment_location_choice_model', 
                                xml_configuration=xml_config, 
                                model_group = 'home_based',
                                configuration=None)
        er.estimate()
       
if __name__ == "__main__":
    opus_unittest.main()