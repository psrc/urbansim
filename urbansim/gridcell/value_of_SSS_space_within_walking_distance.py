# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class value_of_SSS_space_within_walking_distance(abstract_within_walking_distance):
    """Sum of given units of locations within walking distance of this gridcell"""
    
    def __init__(self, type):
        self.dependent_variable = "total_value_%s" % type
        abstract_within_walking_distance.__init__(self)
