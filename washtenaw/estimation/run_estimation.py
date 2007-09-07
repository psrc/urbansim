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


from opus_core.logger import logger

from urbansim.estimation.estimation_runner import EstimationRunner as UrbansimEstimationRunner


class EstimationRunner(object):
    def run_estimation(self, estimation_config, model_name, save_estimation_results=True):
        logger.start_block('Estimating %s' % model_name)
        try:
            estimator = UrbansimEstimationRunner(
                model_name, 
                specification_from_module=True, 
                package="washtenaw",
                configuration=estimation_config,
                save_estimation_results=save_estimation_results
                )
            estimator.estimate()
            
        finally:
            logger.end_block()
        
if __name__ == '__main__':
    #model_name = 'lpm'
    #model_name = 'hlcm'
    #model_name = 'elcm-industrial'
    #model_name = 'elcm-commercial'
    ###model_name = 'elcm-home_based'
    #model_name = 'dplcm-industrial'
    #model_name = 'dplcm-commercial'
    model_name = 'dplcm-residential'
    #model_name = 'rlsm'

    from washtenaw.estimation.my_estimation_config import my_configuration
    
    EstimationRunner().run_estimation(my_configuration, model_name)