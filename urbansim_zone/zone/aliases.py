# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
aliases = [
        "residential_units = zone.aggregate(pseudo_building.residential_units)",
        "vacant_residential_units = numpy.maximum(0, urbansim_zone.zone.residential_units - urbansim.zone.number_of_households)",
        "commercial_job_spaces = zone.aggregate(pseudo_building.commercial_job_spaces)",
        "industrial_job_spaces = zone.aggregate(pseudo_building.industrial_job_spaces)",
        "number_of_vacant_commercial_jobs = numpy.maximum(0, urbansim_zone.zone.commercial_job_spaces - urbansim_zone.zone.number_of_commercial_jobs)",
        "number_of_vacant_industrial_jobs = numpy.maximum(0, urbansim_zone.zone.industrial_job_spaces - urbansim_zone.zone.number_of_industrial_jobs)",
        "developable_residential_units = numpy.maximum(0, zone.aggregate(pseudo_building.residential_units_capacity - pseudo_building.residential_units))",
           ]
