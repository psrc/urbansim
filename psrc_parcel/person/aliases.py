# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
           "workplace_of_worker1 = person.disaggregate(household.aggregate((person.worker1==1) * (person.disaggregate(urbansim_parcel.job.zone_id))) )",
           "workplace_of_worker2 = person.disaggregate(household.aggregate((person.worker2==1) * (person.disaggregate(urbansim_parcel.job.zone_id))) )",
           "sector_id_of_worker1 = person.disaggregate(household.aggregate((person.worker1==1) * (person.disaggregate(job.sector_id))) )",
           "sector_id_of_worker2 = person.disaggregate(household.aggregate((person.worker2==1) * (person.disaggregate(job.sector_id))) )",           
           "worker_id = 1*(person.worker1==1) + 2*(person.worker2==1)",
           "household_income = person.disaggregate(household.income)",
           "edu_lths = numpy.in1d(person.edu, (1,))",
           "edu_lehs = numpy.in1d(person.edu, (1,2))",
           "edu_hspa = numpy.in1d(person.edu, (2,4,5))",
           "edu_college = numpy.in1d(person.edu, (3,6,7))",
           "edu_pg = numpy.in1d(person.edu, (7,))",
           "edu_adv = numpy.in1d(person.edu, (6, 7))",
           ]
