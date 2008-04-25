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


from numpy import where
from washtenaw.models.regional_scaling_jobs_model import RegionalScalingJobsModel

class RegionalDistributeUnplacedJobsModel(RegionalScalingJobsModel):
    """This model is used to place randomly (within sectors) any unplaced jobs.
    """
    model_name = "Regional Distribute Unplaced Jobs Model"
     
    def run(self, location_set, agent_set, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset. The model selects all unplaced jobs 
            and passes them to ScalingJobsModel.
        """
        agents_index = where(agent_set.get_attribute(location_set.get_id_name()[0]) <= 0)[0]
        
        return RegionalScalingJobsModel.run(self, location_set, agent_set, agents_index, **kwargs)

