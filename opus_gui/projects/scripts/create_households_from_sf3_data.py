#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

# create households from sf3 data
# This script depends upon the user downloading a file from the census bureau's
# website.  SF3 table P55 by block group is what is needed

import random

all_census_hh_by_income_codes = ['P055003','P055004','P055005','P055006','P055007','P055008','P055009','P055010','P055011','P055012','P055013','P055014','P055015','P055016','P055017','P055018','P055019','P055020','P055021','P055022','P055023','P055024','P055025','P055026','P055027','P055028','P055029','P055030','P055031','P055032','P055033','P055034','P055035','P055036','P055037','P055038','P055039','P055040','P055041','P055042','P055043','P055044','P055045','P055046','P055047','P055048','P055049','P055050','P055051','P055052','P055053','P055054','P055055','P055056','P055057','P055058','P055059','P055060','P055061','P055062','P055063','P055064','P055065','P055066','P055067','P055068','P055069','P055070','P055071','P055072','P055073','P055074','P055075','P055076','P055077','P055078','P055079','P055080','P055081','P055082','P055083','P055084','P055085','P055086','P055087','P055088','P055089','P055090','P055091','P055092','P055093','P055094','P055095','P055096','P055097','P055098','P055099','P055100','P055101','P055102','P055103','P055104','P055105','P055106','P055107','P055108','P055109','P055110','P055111','P055112','P055113','P055114','P055115','P055116','P055117','P055118','P055119','P055120']

age_class_18_24 = ['P055003', 'P055004', 'P055005', 'P055006', 'P055007', 'P055008', 'P055009', 'P055010', 'P055011', 'P055012', 'P055013', 'P055014', 'P055015', 'P055016', 'P055017', 'P055018']
age_class_25_34 = ['P055020', 'P055021', 'P055022', 'P055023', 'P055024', 'P055025', 'P055026', 'P055027', 'P055028', 'P055029', 'P055030', 'P055031', 'P055032', 'P055033', 'P055034', 'P055035']
age_class_35_44 = ['P055037', 'P055038', 'P055039', 'P055040', 'P055041', 'P055042', 'P055043', 'P055044', 'P055045', 'P055046', 'P055047', 'P055048', 'P055049', 'P055050', 'P055051', 'P055052']
age_class_45_54 = ['P055054', 'P055055', 'P055056', 'P055057', 'P055058', 'P055059', 'P055060', 'P055061', 'P055062', 'P055063', 'P055064', 'P055065', 'P055066', 'P055067', 'P055068', 'P055069']
age_class_55_64 = ['P055071', 'P055072', 'P055073', 'P055074', 'P055075', 'P055076', 'P055077', 'P055078', 'P055079', 'P055080', 'P055081', 'P055082', 'P055083', 'P055084', 'P055085', 'P055086']
age_class_65_74 = ['P055088', 'P055089', 'P055090', 'P055091', 'P055092', 'P055093', 'P055094', 'P055095', 'P055096', 'P055097', 'P055098', 'P055099', 'P055100', 'P055101', 'P055102', 'P055103']
age_class_75_100 = ['P055105', 'P055106', 'P055107', 'P055108', 'P055109', 'P055110', 'P055111', 'P055112', 'P055113', 'P055114', 'P055115', 'P055116', 'P055117', 'P055118', 'P055119', 'P055120']
age_classes = [age_class_18_24, age_class_25_34, age_class_35_44, age_class_45_54, age_class_55_64, age_class_65_74, age_class_75_100]
empty_lists = ([], [], [], [], [], [], [])
(age_class_18_24_index, age_class_25_34_index, age_class_35_44_index, age_class_45_54_index, age_class_55_64_index, age_class_65_74_index, age_class_75_100_index) = empty_lists
age_class_indexes = [age_class_18_24_index, age_class_25_34_index, age_class_35_44_index, age_class_45_54_index, age_class_55_64_index, age_class_65_74_index, age_class_75_100_index]

income_class_0_10 = ['P055003', 'P055020', 'P055037', 'P055054', 'P055071', 'P055088', 'P055105']
income_class_10_14 = ['P055004', 'P055021', 'P055038', 'P055055', 'P055072', 'P055089', 'P055106']
income_class_15_19 = ['P055005', 'P055022', 'P055039', 'P055056', 'P055073', 'P055090', 'P055107']
income_class_20_24 = ['P055006', 'P055023', 'P055040', 'P055057', 'P055074', 'P055091', 'P055108']
income_class_25_29 = ['P055007', 'P055024', 'P055041', 'P055058', 'P055075', 'P055092', 'P055109']
income_class_30_34 = ['P055008', 'P055025', 'P055042', 'P055059', 'P055076', 'P055093', 'P055110']
income_class_35_39 = ['P055009', 'P055026', 'P055043', 'P055060', 'P055077', 'P055094', 'P055111']
income_class_40_44 = ['P055010', 'P055027', 'P055044', 'P055061', 'P055078', 'P055095', 'P055112']
income_class_45_49 = ['P055011', 'P055028', 'P055045', 'P055062', 'P055079', 'P055096', 'P055113']
income_class_50_59 = ['P055012', 'P055029', 'P055046', 'P055063', 'P055080', 'P055097', 'P055114']
income_class_60_74 = ['P055013', 'P055030', 'P055047', 'P055064', 'P055081', 'P055098', 'P055115']
income_class_75_99 = ['P055014', 'P055031', 'P055048', 'P055065', 'P055082', 'P055099', 'P055116']
income_class_100_124 = ['P055015', 'P055032', 'P055049', 'P055066', 'P055083', 'P055100', 'P055117']
income_class_125_149 = ['P055016', 'P055033', 'P055050', 'P055067', 'P055084', 'P055101', 'P055118']
income_class_150_199 = ['P055017', 'P055034', 'P055051', 'P055068', 'P055085', 'P055102', 'P055119']
income_class_200 = ['P055018', 'P055035', 'P055052', 'P055069', 'P055086', 'P055103', 'P055120']
income_classes = [income_class_0_10, income_class_10_14, income_class_15_19, income_class_20_24, income_class_25_29, income_class_30_34, income_class_35_39, income_class_40_44, income_class_45_49, income_class_50_59, income_class_60_74, income_class_75_99, income_class_100_124, income_class_125_149, income_class_150_199, income_class_200]
empty_lists2 = ([], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
(income_class_0_10_index, income_class_10_14_index, income_class_15_19_index, income_class_20_24_index, income_class_25_29_index, income_class_30_34_index, income_class_35_39_index, income_class_40_44_index, income_class_45_49_index, income_class_50_59_index, income_class_60_74_index, income_class_75_99_index, income_class_100_124_index, income_class_125_149_index, income_class_150_199_index, income_class_200_index) = empty_lists2
income_class_indexes = [income_class_0_10_index, income_class_10_14_index, income_class_15_19_index, income_class_20_24_index, income_class_25_29_index, income_class_30_34_index, income_class_35_39_index, income_class_40_44_index, income_class_45_49_index, income_class_50_59_index, income_class_60_74_index, income_class_75_99_index, income_class_100_124_index, income_class_125_149_index, income_class_150_199_index, income_class_200_index]


def get_householder_age(age_class):
    if age_class in age_class_18_24_index:
        return random.randint(18, 24)
    elif age_class in age_class_25_34_index:
        return random.randint(25, 34)
    elif age_class in age_class_35_44_index:
        return random.randint(35, 44)
    elif age_class in age_class_45_54_index:
        return random.randint(45, 54)
    elif age_class in age_class_55_64_index:
        return random.randint(55, 64)
    elif age_class in age_class_65_74_index:
        return random.randint(65, 74)
    elif age_class in age_class_75_100_index:
        return random.randint(75, 100)

def get_household_income(income_class):
    if income_class in income_class_0_10_index:
        return random.randint(5000, 10000)
    elif income_class in income_class_10_14_index:
        return random.randint(10000, 14999)
    elif income_class in income_class_15_19_index:
        return random.randint(15000, 19999)
    elif income_class in income_class_20_24_index:
        return random.randint(20000, 24999)
    elif income_class in income_class_25_29_index:
        return random.randint(25000, 29999)
    elif income_class in income_class_30_34_index:
        return random.randint(30000, 34999)
    elif income_class in income_class_35_39_index:
        return random.randint(35000, 39999)
    elif income_class in income_class_40_44_index:
        return random.randint(40000, 44999)
    elif income_class in income_class_45_49_index:
        return random.randint(45000, 49999)
    elif income_class in income_class_50_59_index:
        return random.randint(50000, 59999)
    elif income_class in income_class_60_74_index:
        return random.randint(60000, 74999)
    elif income_class in income_class_75_99_index:
        return random.randint(75000, 99999)
    elif income_class in income_class_100_124_index:
        return random.randint(100000, 124999)
    elif income_class in income_class_125_149_index:
        return random.randint(125000, 149999)
    elif income_class in income_class_150_199_index:
        return random.randint(150000, 199999)
    elif income_class in income_class_200_index:
        return random.randint(200000, 1000000)

def opusRun(progressCB,logCB,params):

    my_dict = {}
    for key, val in params.iteritems():
        my_dict[str(key)] = str(val)

    census_data_file = my_dict['census_data_file']
    output_file = my_dict['output_file']

    #census_data_file = 'c:/tmp/dc_dec_2000_sf3_u_data1.txt'
    #output_file = 'c:/tmp/maricopa_households_from_sf3.txt'

    
    # get first line of census data file
    f = open(census_data_file)
    first_line1 = f.readline().split('|')
    f.close()
    first_line = []
    for i in first_line1:
        x = i.strip('\n')
        first_line.append(x)
    
    # get index positions of income classes
    for i in income_classes:
        for j in i:
            x = first_line.index(j)
            income_class_indexes[income_classes.index(i)].append(x)
    
    # get index positions of age classes
    for i in age_classes:
        for j in i:
            x = first_line.index(j)
            age_class_indexes[age_classes.index(i)].append(x)
    
    # make list of all age class indexes
    relevant_age_class_indexes = age_class_18_24_index + age_class_25_34_index + age_class_35_44_index + age_class_45_54_index + age_class_55_64_index + age_class_65_74_index + age_class_75_100_index
    
    raw_data = open(census_data_file)
    households = []
    for line in raw_data:
        if 'GEO_ID' in line:
            pass
        elif 'Geography Identifier' in line:
            pass
        else:
            lst1 = line.split('|') # line with newline characters
            lst = [] # line stripped of newline characters
            for i in lst1:
                x = i.strip('\n')
                lst.append(x)
            block_group = lst[1]
            index_counter = 0
            for j in lst:
                if j <> '': # if not empty
                    if index_counter in relevant_age_class_indexes: # if in any age class
                        for k in range(0, int(j)):
                            householder_age = get_householder_age(index_counter)
                            household_income = get_household_income(index_counter)
                            #print "value: ", j, "index: ", index_counter, "Generated Age: ", householder_age, "Generated Income: ", household_income
                            strng = '%s, %s, %s\n' % (block_group, householder_age, household_income)
                            households.append(strng)
                index_counter += 1
    
    g = open(output_file, 'w')
    g.write('block_group, householder_age, household_income\n')
    g.writelines(households)
    g.close()