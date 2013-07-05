# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "employment = travel_zone.aggregate(building.number_of_agents(job),intermediates=[zone])",
    "number_of_jobs = travel_zone.aggregate(building.number_of_agents(job),intermediates=[zone])",
    "number_of_households = travel_zone.aggregate(building.number_of_agents(household),intermediates=[zone])",
    "population = travel_zone.aggregate(household.persons,intermediates=[building,zone])",
    "emp_accom_svc = travel_zone.aggregate(job.sector_id==1,intermediates=[building,zone])",      
    "emp_construction = travel_zone.aggregate(job.sector_id==2,intermediates=[building,zone])",
    "emp_govt_ed = travel_zone.aggregate(job.sector_id==3,intermediates=[building,zone])",
    "emp_healthcare = travel_zone.aggregate(job.sector_id==4,intermediates=[building,zone])",
    "emp_manuf = travel_zone.aggregate(job.sector_id==5,intermediates=[building,zone])",
    "emp_office = travel_zone.aggregate(job.sector_id==6,intermediates=[building,zone])",
    "emp_other = travel_zone.aggregate(job.sector_id==7,intermediates=[building,zone])",
    "emp_extract = travel_zone.aggregate(job.sector_id==8,intermediates=[building,zone])",
    "emp_retail = travel_zone.aggregate(job.sector_id==9,intermediates=[building,zone])",
    "emp_wholesale = travel_zone.aggregate(job.sector_id==10,intermediates=[building,zone])",
    "number_of_jobs_of_sector_1 = travel_zone.aggregate(job.sector_id==1,intermediates=[building,zone])",
    "number_of_jobs_of_sector_2 = travel_zone.aggregate(job.sector_id==2,intermediates=[building,zone])",
    "number_of_jobs_of_sector_3 = travel_zone.aggregate(job.sector_id==3,intermediates=[building,zone])",
    "number_of_jobs_of_sector_4 = travel_zone.aggregate(job.sector_id==4,intermediates=[building,zone])",
    "number_of_jobs_of_sector_5 = travel_zone.aggregate(job.sector_id==5,intermediates=[building,zone])",
    "number_of_jobs_of_sector_6 = travel_zone.aggregate(job.sector_id==6,intermediates=[building,zone])",
    "number_of_jobs_of_sector_7 = travel_zone.aggregate(job.sector_id==7,intermediates=[building,zone])",
    "number_of_jobs_of_sector_8 = travel_zone.aggregate(job.sector_id==8,intermediates=[building,zone])",
    "number_of_jobs_of_sector_9 = travel_zone.aggregate(job.sector_id==9,intermediates=[building,zone])",
    "number_of_jobs_of_sector_10 = travel_zone.aggregate(job.sector_id==10,intermediates=[building,zone])",
           ]
