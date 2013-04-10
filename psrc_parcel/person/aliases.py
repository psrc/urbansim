# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
           "workplace_of_worker1 = person.disaggregate(household.aggregate((psrc.person.worker1==1) * (person.disaggregate(urbansim_parcel.job.zone_id))) )",
           "workplace_of_worker2 = person.disaggregate(household.aggregate((psrc.person.worker2==1) * (person.disaggregate(urbansim_parcel.job.zone_id))) )",
           "sector_id_of_worker1 = person.disaggregate(household.aggregate((psrc.person.worker1==1) * (person.disaggregate(job.sector_id))) )",
           "sector_id_of_worker2 = person.disaggregate(household.aggregate((psrc.person.worker2==1) * (person.disaggregate(job.sector_id))) )",           
           "worker_id = 1*(psrc.person.worker1==1) + 2*(psrc.person.worker2==1)",
           "household_income = person.disaggregate(household.income)",
           "edu_lths = numpy.in1d(person.edu, (1,))",
           "edu_lehs = numpy.in1d(person.edu, (1,2))",
           "edu_hspa = numpy.in1d(person.edu, (2,4,5))",
           "edu_college = numpy.in1d(person.edu, (3,6,7))",
           "edu_pg = numpy.in1d(person.edu, (7,))",
           "edu_adv = numpy.in1d(person.edu, (6, 7))",
           "student = numpy.logical_or(person.stype == 2, person.stype == 6)", # to get a value of 1 in persons_for_estimation that corresponds to student=1 in the persons table
           "school_district_id = person.disaggregate(parcel.school_district_id)", 
           "is_in_private_or_public_k12_school = numpy.logical_and(person.stype == 2, numpy.logical_or(psrc_parcel.person.is_in_private_school, psrc_parcel.person.is_in_public_school))",
           "is_in_private_school = numpy.logical_and(person.is_in_school, person.school_type == 2)",
           "is_in_private_k12_school = numpy.logical_and(psrc_parcel.person.is_in_private_school, person.stype == 2)",
           "is_in_home_school = numpy.logical_and(person.is_in_school, person.stype == 6)",
           "is_in_public_school = numpy.logical_and(person.is_in_school, person.school_type == 1)",
           "has_older_sibling_in_private_school = person.disaggregate(psrc_parcel.household.age_of_oldest_child_in_private_school) > person.age",
           "has_older_sibling_in_home_school = person.disaggregate(psrc_parcel.household.age_of_oldest_child_in_home_school) > person.age",
           "has_older_sibling_in_private_or_home_school = numpy.logical_or(psrc_parcel.person.has_older_sibling_in_private_school, psrc_parcel.person.has_older_sibling_in_home_school)",
           "has_older_sibling = person.disaggregate(psrc_parcel.household.age_of_oldest_child) > person.age",
           "has_older_sibling_in_school = person.disaggregate(psrc_parcel.household.age_of_oldest_child_in_school) > person.age",
           "private_schools_in_neighborhood = person.disaggregate(psrc_parcel.parcel.number_of_private_schools_within_1000_of_parcel, intermediates=[building, household])",
           "age_category = (1 * (person.age < 6)) + (2 * numpy.logical_and(person.age >=6, person.age < 11)) + (3 * numpy.logical_and(person.age >= 11, person.age < 15)) + (4 * numpy.logical_and(person.age >= 15, person.age < 18)) + (5 * (person.age >= 18))",
           "school_of_oldest_child_private = person.disaggregate(psrc_parcel.household.school_of_oldest_child_private)"
           ]
