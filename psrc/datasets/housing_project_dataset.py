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

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import zeros, where, logical_or, logical_not

class HousingProjectDataset(UrbansimDataset):
    """Set of housing projects.
    """

    id_name_default = ["id_parcel", "yearbuilt"]
    in_table_name_default = "housing_projects"
    out_table_name_default = "housing_projects"
    dataset_name = "housing_project"

    def remove_non_recent_data(self, current_year, recent_years):
        """Removes records that are not in the "recent years".
        """
        years = self.get_attribute("scheduled_year")
        filter = zeros(self.size(), dtype="int32")
        for year in range(current_year-recent_years, current_year+1):
            filter = logical_or(filter, years==year)
        idx = where(logical_not(filter))[0]
        self.remove_elements(idx)