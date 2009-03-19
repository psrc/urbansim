# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class gridcell_year_built(Variable):
    """Equal to the primary attribute 'year_built'"""

    year_built = "year_built"

    def dependencies(self):
        return [my_attribute_label(self.year_built)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.year_built)
