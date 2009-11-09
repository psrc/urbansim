# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim_parcel.building.has_valid_year_built import has_valid_year_built as building_has_valid_year_built
from variable_functions import my_attribute_label

class has_valid_year_built(building_has_valid_year_built):
    """If proposals have valid start_year or not."""

    year_built = "start_year"

    def dependencies(self):
        return [my_attribute_label(self.year_built)]
