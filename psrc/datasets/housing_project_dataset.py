# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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