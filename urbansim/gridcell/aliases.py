# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           "number_of_young_households=gridcell.aggregate(urbansim.household.is_young)",
           "number_of_home_owners=gridcell.aggregate(urbansim.household.is_home_owner)",           
           "number_of_home_renters=gridcell.aggregate(urbansim.household.is_home_renter)",
           "number_of_households_with_children=gridcell.aggregate(urbansim.household.has_children)",
           ]