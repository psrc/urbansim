# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "number_of_jobs = zone.aggregate(building.number_of_agents(job))",
    "emp_accom_svc = zone.aggregate(job.sector_id==1), intermediates=[building]",      
    "emp_construction = zone.aggregate(job.sector_id==2), intermediates=[building]",
    "emp_govt_ed = zone.aggregate(job.sector_id==3), intermediates=[building]"
    "emp_healthcare = zone.aggregate(job.sector_id==4), intermediates=[building]",
    "emp_manuf = zone.aggregate(job.sector_id==5), intermediates=[building]",
    "emp_office = zone.aggregate(job.sector_id==6), intermediates=[building]",
    "emp_other = zone.aggregate(job.sector_id==7), intermediates=[building]",
    "emp_extract = zone.aggregate(job.sector_id==8), intermediates=[building]",
    "emp_retail = zone.aggregate(job.sector_id==9), intermediates=[building]",
    "emp_wholesale = zone.aggregate(job.sector_id==10), intermediates=[building]",
           ]
