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

from urbansim.models.distribute_unplaced_jobs_model import DistributeUnplacedJobsModel as UrbansimDistributeUnplacedJobsModel

class DistributeUnplacedJobsModel(UrbansimDistributeUnplacedJobsModel):
    """
    This model works exactly as its parent. It uses different variable_package.
    It is used for locating scalable jobs into buildings.  
    """
    variable_package = "urbansim_parcel"
