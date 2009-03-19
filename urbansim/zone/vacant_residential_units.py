# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from variable_functions import my_attribute_label
from urbansim.gridcell.vacant_residential_units import vacant_residential_units as gc_vacant_residential_units

class vacant_residential_units(gc_vacant_residential_units):
    """The residential_units - number_of_households. """

    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.residential_units)]
