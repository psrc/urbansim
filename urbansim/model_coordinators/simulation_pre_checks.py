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

class SimulationPreChecks(object):
    
    def check_satisfies_model_interdependence(self, models):
        """Some models may require that other models be used in order to run properly. Check this. """
        hbe = 'home_based_employment_location_choice_model' in models
        cel = "commercial_employment_location_choice_model" in models
        iel = "industrial_employment_location_choice_model" in models
        sjm = "scaling_jobs_model" in models

        return (hbe and (cel or iel)) or not(hbe or cel or iel or sjm)
    
    

from opus_core.tests import opus_unittest
class TestSimulationPreChecks(opus_unittest.OpusTestCase):
    def test_check_satisfies_model_interdependence(self):
        complete_models = ['home_based_employment_location_choice_model', 'industrial_employment_location_choice_model', 
                  'another_model', 'yet_another_model']
        incomplete_model_set = ['home_based_employment_location_choice_model', 'another_model', 'yet_another_model']
        incomplete_model_set2 = ['scaling_jobs_model', 'another_model', 'yet_another_model']
        
        self.assert_(SimulationPreChecks().check_satisfies_model_interdependence(complete_models), 
                     'models were actually consistant')
        self.assert_(not SimulationPreChecks().check_satisfies_model_interdependence(incomplete_model_set), 
                     'models really were not interdependent')
        self.assert_(not SimulationPreChecks().check_satisfies_model_interdependence(incomplete_model_set2), 
                     'models really were not interdependent')
        

if __name__=='__main__':
    opus_unittest.main()