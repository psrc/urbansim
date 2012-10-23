#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
    # employment variables:
    'is_employed = numpy.in1d(person.work_status, (1,2,4,5))',

    # age related variables:
    'is_child = person.age<18',
    'is_driving_age = person.age>15',
    'is_young_adult = numpy.logical_and(person.age>17, person.age<36)',
    'is_adult = person.age>17',
    'is_senior_citizen = person.age>64',
    'is_over_55 = person.age>54',
    # education variables:
    'is_student = person.student_status>1',
    'is_college_student = numpy.logical_and(mag_zone.person.is_student, person.education>8)',
    'less_than_high_school_diploma = person.education<9',
    'at_least_high_school_diploma = person.education>8',
    'at_least_associates_degree = person.education>11',
    'at_least_bachelors_degree = person.education>12',
    'at_least_masters_degree = person.education>13',
    # population by geographies:
    'tazi03_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.tazi03_id)))',
    'taz2012_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.taz2012_id)))',
    'razi03_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.razi03_id)))',
    'raz2012_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.raz2012_id)))',
    'mpa_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.mpa_id)))',
    'zone_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.zone_id)))',
    'pseudo_blockgroup_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.pseudo_blockgroup_id)))',
    'census_place_id = person.disaggregate(household.disaggregate(building.disaggregate(zone.census_place_id)))',
    'super_raz_id = person.disaggregate(household.super_raz_id)',
    # other variables:
    'gender = person.sex',
    'head_of_hh = person.relate==1',
    'is_hispanic = numpy.in1d(person.race_id, (6,7,8,9,10))',
    'is_not_hispanic = numpy.in1d(person.race_id, (1,2,3,4,5))',
    'is_married = numpy.in1d(person.marriage_status, (1,2))',

    #for simtravel project
    'wtaz = (person.work_outside_region==0)*person.disaggregate(mag_zone.job.zone_id) + (person.work_outside_region==1)*(person.wtaz0)',
    'synthetic_person_id = person.person_id',
    'tmtowrk = (person.work_outside_region==0)*(mag_zone.person.travel_time_from_home_to_work) + (person.work_outside_region==1)*person.disaggregate(synthetic_person.tmtowrk)',
    'part_time = ~ (person.full_time == 1)',
    'county_id = person.disaggregate(zone.county_id, intermediates=[building, household])',
           ]
