# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from urbansim.gridcell.abstract_within_walking_distance import abstract_within_walking_distance

class SSS_within_walking_distance( abstract_within_walking_distance ):
    """Caclulate variable given by SSS within the walking distance range."""
    
    def __init__(self, varname):
        self.dependent_variable = varname
        abstract_within_walking_distance.__init__(self)
