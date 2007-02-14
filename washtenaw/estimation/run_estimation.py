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

from urbansim.estimation.estimation_runner import EstimationRunner as UrbansimEstimationRunner

class EstimationRunner(object):
    def run_estimation(self, estimation_config, model, save_estimation_results=False):
        estimator = UrbansimEstimationRunner(
            model, 
            specification_from_module=True, 
            package="washtenaw",
            configuration=estimation_config,
            save_estimation_results=save_estimation_results
            )
        estimator.estimate()
        #estimator.reestimate("HLCM_specification")
        #estimator.reestimate("ELCM_specification", type="commercial")
        
if __name__ == '__main__':
    #model = 'hlcm'
    #model = 'elcm-industrial'
    #model = 'elcm-commercial'
    #model = 'elcm-home_based'
    #model = dplcm-industrial'
    #model = 'dplcm-commercial'
    #model ='dplcm-residential'
    model = 'lpm'
    #model = 'rlsm'

    from washtenaw.estimation.my_estimation_config import my_configuration
    
    EstimationRunner().run_estimation(my_configuration, model)