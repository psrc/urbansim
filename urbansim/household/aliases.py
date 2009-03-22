# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           "is_home_owner = numpy.logical_or(household.tenure==1, household.tenure==2)",
           "is_home_renter = household.tenure==3",
           "has_children = household.children > 0",
           ]