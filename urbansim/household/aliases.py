# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           "is_home_owner = numpy.logical_or(household.tenure==1, household.tenure==2)",
           "is_home_renter = household.tenure==3",
           "has_children = household.children > 0",
           "cars_category=0*(household.cars==0)+1*(household.cars==1)+2*(household.cars==2)+3*(household.cars>=3)"
           ]