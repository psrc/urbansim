# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "residential_units = zone.aggregate(building.residential_units)",
        "vacant_residential_units = numpy.maximum(0, urbansim_zone.zone.residential_units - urbansim.zone.number_of_households)",
        "commercial_job_spaces = zone.aggregate(building.commercial_job_spaces)",
        "industrial_job_spaces = zone.aggregate(building.industrial_job_spaces)",
        "number_of_vacant_commercial_jobs = numpy.maximum(0, urbansim_zone.zone.commercial_job_spaces - urbansim_zone.zone.number_of_commercial_jobs)",
        "number_of_vacant_industrial_jobs = numpy.maximum(0, urbansim_zone.zone.industrial_job_spaces - urbansim_zone.zone.number_of_industrial_jobs)",
        "developable_residential_units = numpy.maximum(0, zone.aggregate(building.residential_units_capacity - building.residential_units))",
        "residential_units_capacity = zone.aggregate(building.residential_units_capacity)",
        "non_residential_sqft_capacity = zone.aggregate(building.non_residential_sqft_capacity)",
        "number_of_jobs = zone.number_of_agents(job)",
        "population = zone.aggregate(household.persons)",
        "emp_agric = zone.aggregate(job.sector_id==1)",      
        "emp_manuf = zone.aggregate(job.sector_id==2)",
        "emp_retail = zone.aggregate(job.sector_id==3)",
        "emp_finance_prof = zone.aggregate(job.sector_id==4)",
        "emp_health_ed = zone.aggregate(job.sector_id==5)",
        "emp_other = zone.aggregate(job.sector_id==6)"
           ]
