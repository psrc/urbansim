#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator

class EmploymentLocationChoiceModelByZonesConfigurationCreator(EmploymentLocationChoiceModelConfigurationCreator):
    _model_name = 'employment_location_choice_model_by_zones'
    def execute(self):
        result = EmploymentLocationChoiceModelConfigurationCreator.execute(self)
        result['import'] = {
                'psrc_parcel.models.%s' % self._model_name: 'EmploymentLocationChoiceModelByZones'
                }
        result['init']['name'] = 'EmploymentLocationChoiceModelByZones'
        result["run"]["arguments"]["zones"] = 'zone'
        return result