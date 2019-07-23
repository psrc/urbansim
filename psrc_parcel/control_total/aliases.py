# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           'county_id = control_total.disaggregate(subreg.county_id)',
           'region_id = control_total.year >= 0', # we want here just the number 1 for all records
           ]
