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
           #"student = numpy.logical_or(person.stype == 2, person.stype == 6)", # to get a value of 1 in persons_for_estimation that corresponds to student=1 in the persons table 
           "student = 1*((person.stype == 2) + (person.stype == 3) + (person.stype == 6)) + 2*((person.stype == 4) + (person.stype == 5)) + 3*((person.stype > 6) + (person.stype < 1))", # match student attribute in persons table (1: primary/secondary student, 2: post-secondary student, 3: no student)
           "attending_school_parcel_id = person.disaggregate(school.parcel_id)",
           "attending_school_zone_id = person.disaggregate(parcel.zone_id, intermediates=[school])",
           "school_district_id = person.disaggregate(parcel.school_district_id, intermediates=[building])", # school district of home location 
           "is_in_private_or_public_k12_school = numpy.logical_and((person.stype == 2)* (person.age <= 18) * (person.age >= 5), numpy.logical_or(psrc_parcel.person.is_in_private_school, psrc_parcel.person.is_in_public_school))",
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
           "age_category = (1 * (person.age < 5)) + (2 * numpy.logical_and(person.age >=5, person.age < 11)) + (3 * numpy.logical_and(person.age >= 11, person.age < 15)) + (4 * numpy.logical_and(person.age >= 15, person.age < 19)) + (5 * (person.age >= 19))",
           "school_of_oldest_child_private = person.disaggregate(psrc_parcel.household.school_of_oldest_child_private)",
           "income_groups_for_tm = person.disaggregate(1*(household.income <= 20000) + 2*(household.income > 20000)*(household.income <= 80000) + 3*(household.income > 80000))",
           "new_zone_id = person.disaggregate(parcel.new_zone_id, intermediates=[building, household])",
           "city_id = person.disaggregate(parcel.city_id, intermediates=[building, household])",
           "tractcity_id = person.disaggregate(parcel.tractcity_id, intermediates=[building, household])",
           "county_id = person.disaggregate(psrc_parcel.household.county_id)"
           ]
has_older_sibl_of_same_age_cat = "has_older_sibling_own_age_category_in_private_school = ((psrc_parcel.person.age_category == 1) * (person.disaggregate(psrc_parcel.household.age_of_oldest_child_age_category_1_in_private_school) > person.age))" 
school_of_older_sibl_of_same_age_cat = "school_of_older_sibling_own_age_category_private = ((psrc_parcel.person.age_category == 1) * (person.disaggregate(psrc_parcel.household.age_of_oldest_child_age_category_1_in_private_school) > person.age) * person.disaggregate(psrc_parcel.household.school_of_oldest_child_in_age_category_1_private))" 
for cat in range(2,6):
    has_older_sibl_of_same_age_cat = "%s + ((psrc_parcel.person.age_category == %s) * (person.disaggregate(psrc_parcel.household.age_of_oldest_child_age_category_%s_in_private_school) > person.age))" % (has_older_sibl_of_same_age_cat, cat, cat)
    school_of_older_sibl_of_same_age_cat = "%s + ((psrc_parcel.person.age_category == %s) * (person.disaggregate(psrc_parcel.household.age_of_oldest_child_age_category_%s_in_private_school) > person.age) * person.disaggregate(psrc_parcel.household.school_of_oldest_child_in_age_category_%s_private))" % (school_of_older_sibl_of_same_age_cat, cat, cat, cat)
    
aliases.append(has_older_sibl_of_same_age_cat)
aliases.append(school_of_older_sibl_of_same_age_cat)

