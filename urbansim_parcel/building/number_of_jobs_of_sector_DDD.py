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

from urbansim.gridcell.number_of_jobs_of_sector_DDD import number_of_jobs_of_sector_DDD as us_number_of_jobs_of_sector_DDD
from urbansim.functions import attribute_label

class number_of_jobs_of_sector_DDD(us_number_of_jobs_of_sector_DDD):
    """Sum the number of jobs for a given building that are in the employment sector specified by DDD.
       (see code in the parent's class) 
    """
    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector),
                'job.building_id']
