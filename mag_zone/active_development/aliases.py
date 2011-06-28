# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
           "remaining_total_capacity = active_development.build_out_capacity - active_development.current_built_units",
           "capacity_this_year = numpy.minimum(mag_zone.active_development.remaining_total_capacity,active_development.max_annual_capacity)",
           ]

