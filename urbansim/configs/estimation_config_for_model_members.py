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

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configs.estimation_base_config import EstimationBaseConfig
from urbansim.estimation.estimator import update_controller_by_specification_from_module
from opus_core.configuration import Configuration

class model_member_configuration:
    def __init__(self, model_name, type, add_member_prefix=False, base_configuration=AbstractUrbansimConfiguration):
        self.type=type
        self.model_name = model_name
        self.member_prefix_added = add_member_prefix
        self.model_group = model_name
        if add_member_prefix:
            self.model_name = "%s_%s" % (self.type, self.model_name)
        self.base_configuration = base_configuration
        
    def get_configuration(self):
        run_configuration = EstimationBaseConfig(base_configuration=self.base_configuration)
        local_configuration = self.get_local_configuration()
        run_configuration.merge(local_configuration)
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = {}
        run_configuration["models"] = [
            {self.model_group: {"group_members": [{self.type: ["estimate"]}]}}
         ]
        if self.member_prefix_added:
            run_configuration["model_name"] = self.model_name
        else:
            run_configuration["model_name"] = "%s_%s" % (self.type, self.model_name)
        return Configuration(run_configuration)

    def get_updated_configuration_from_module(self, run_configuration, specification_module=None):
        run_configuration = update_controller_by_specification_from_module(
                            run_configuration, self.model_name, specification_module)
        run_configuration["models_configuration"][self.model_name]["controller"]["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec['%s']" % self.type
        return run_configuration  