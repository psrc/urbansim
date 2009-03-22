# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from variable_functions import my_attribute_label
from urbansim_parcel.building.age_masked import age_masked

class building_age(age_masked):
    """The age of buildings in proposals, computed by subtracting the year built
    from the current simulation year. All values that have year_built <= urbansim_constant["absolute_min_year"]
    are masked.
    """

    year_built = "start_year"

    def dependencies(self):
        return [my_attribute_label(self.year_built), my_attribute_label("has_valid_year_built")]
