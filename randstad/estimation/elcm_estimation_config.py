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

from urbansim.configs.elcm_estimation_config import elcm_configuration as config
from urbansim.estimation.estimator import update_controller_by_specification_from_module
from randstad.run_config.randstad_baseline import run_configuration as randstad_config

class elcm_configuration(config):
    def get_configuration(self, specification_module="ELCM_specification"):
        run_configuration = config.get_configuration(self)
        run_configuration.merge(randstad_config)
        run_configuration['models'] = [
            'housing_price_model',
            "employment_relocation_model",
            "divide_jobs_model",                                       
            {self.model_name:['estimate']}]
        return self.get_updated_configuration_from_module(run_configuration, specification_module)
