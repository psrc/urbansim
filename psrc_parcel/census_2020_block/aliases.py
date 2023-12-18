# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

jobs_by_sector = ["number_of_jobs_of_sector_%s = census_2020_block.aggregate(urbansim_parcel.building.number_of_jobs_of_sector_%s, intermediates=[parcel])" % (x, x) for x in range(1,14)]

aliases = [

           ]
    
aliases = aliases + jobs_by_sector


