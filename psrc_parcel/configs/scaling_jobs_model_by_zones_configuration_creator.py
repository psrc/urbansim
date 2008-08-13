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

from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator

class ScalingJobsModelByZonesConfigurationCreator(GovernmentalEmploymentLocationChoiceModelConfigurationCreator):
    _model_name = 'scaling_jobs_model_by_geography'
    def execute(self):
        result = GovernmentalEmploymentLocationChoiceModelConfigurationCreator.execute(self)
        result['import'] = {
                'psrc_parcel.models.%s' % self._model_name: 'ScalingJobsModelByGeography'
                }
        result['init']['name'] = 'ScalingJobsModelByGeography'
        result["run"]["arguments"]["geography_set"] = 'zone'
        return result
