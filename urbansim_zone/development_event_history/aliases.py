# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
           "is_residential = development_event_history.disaggregate(building_type.is_residential)",
           #"total_job_spaces = numpy.round(safe_array_divide(development_event_history.non_residential_sqft, urbansim_zone.development_event_history.building_sqft_per_job))",
           "residential_spaces = urbansim_zone.development_event_history.is_residential * development_event_history.residential_units",
           #"non_residential_job_spaces = numpy.logical_not(urbansim_zone.development_event_history.is_residential) * urbansim_zone.development_event_history.total_job_spaces",
           "non_residential_spaces = numpy.logical_not(urbansim_zone.development_event_history.is_residential) * development_event_history.non_residential_sqft",
           "total_spaces = urbansim_zone.development_event_history.residential_spaces + urbansim_zone.development_event_history.non_residential_spaces",
           "occupied_spaces = -1 * (development_event_history.building_type_id > 0)",   #filled with dummy values; should not be used
           ]
