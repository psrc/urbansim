# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

aliases = [
           "number_of_young_households=gridcell.aggregate(urbansim.household.is_young)",
           "number_of_home_owners=gridcell.aggregate(urbansim.household.is_home_owner)",           
           "number_of_home_renters=gridcell.aggregate(urbansim.household.is_home_renter)",
           "number_of_households_with_children=gridcell.aggregate(urbansim.household.has_children)",
           ]