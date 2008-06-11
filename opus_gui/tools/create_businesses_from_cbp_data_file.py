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

import random, os

def generate_random_number_of_employees(size_class):
    if size_class == 3:
        return random.randint(1,4)
    elif size_class == 4:
        return random.randint(5,9)
    elif size_class == 5:
        return random.randint(10,19)
    elif size_class == 6:
        return random.randint(20,49)
    elif size_class == 7:
        return random.randint(50,99)
    elif size_class == 8:
        return random.randint(100,249)
    elif size_class == 9:
        return random.randint(250,499)
    elif size_class == 10:
        return random.randint(500,999)
    elif size_class == 11:
        return random.randint(1000,10000)
    else:
        pass

def get_sqft_per_job(naics):
    if naics == 11:
        return 150
    elif naics == 21:
        return 150
    elif naics == 22:
        return 130
    elif naics == 23:
        return 240
    elif naics == 31:
        return 420
    elif naics == 32:
        return 420
    elif naics == 33:
        return 420
    elif naics == 42:
        return 590
    elif naics == 44:
        return 410
    elif naics == 45:
        return 410
    elif naics == 48:
        return 280
    elif naics == 49:
        return 280
    elif naics == 51:
        return 360
    elif naics == 52:
        return 1010
    elif naics == 53:
        return 1010
    elif naics == 54:
        return 670
    elif naics == 55:
        return 670
    elif naics == 56:
        return 170
    elif naics == 61:
        return 450
    elif naics == 62:
        return 310
    elif naics == 71:
        return 310
    elif naics == 72:
        return 310
    elif naics == 81:
        return 540
    elif naics == 92:
        return 170
    elif naics == 95:
        return 300
    elif naics == 99:
        return 300

def opusRun(progressCB,logCB,params):

    my_dict = {}
    for key, val in params.iteritems():
        my_dict[str(key)] = str(val)

    # zip_code_file is a text file with a list of zip codes
    # to generate business establishments for.  It should
    # have 1 zip code per line
    zip_codes_path = my_dict['zip_codes_path']
    # raw_cbp_data_file is the 'Complete ZIP Code Industry
    # Detail File' downloaded from the County Business Patterns
    # website:
    # http://www.census.gov/epcd/cbp/download/00_data/index.html
    raw_cbp_data_file = my_dict['raw_cbp_data_file']
    # output_file is an output text file of your choosing:
    output_file_path = my_dict['output_file_path']

    # Prepare list of zip codes to be used
    zip_codes = open(zip_codes_path).readlines()
    zip_codes_stripped = []
    for i in zip_codes:
        x = i.strip('\n')
        zip_codes_stripped.append(x)
    
    # Search raw data file for zip codes and
    # generate a csv file with each line taking
    # the form:
    #   zip code, naics code, random number of employees
    raw_data = open(raw_cbp_data_file)
    business = []
    for line in raw_data:
        if '"------"' in line:
            pass
        elif '"zip"' in line:
            pass
        elif '----' in line:
            lst = []
            lst = line.split(',')
            zipcode = lst[0].strip('"')
            if zipcode in zip_codes_stripped:
                naics_code1 = lst[1].strip('"')
                naics_code = int(naics_code1.replace('-', ''))
                for i in range(3,12):
                    if int(lst[i]) != 0:
                        for j in range(0, int(lst[i])):
                            employees = generate_random_number_of_employees(i)
                            sqft_per_job = get_sqft_per_job(naics_code)
                            strng = '%s, %s, %s, %s\n' % (zipcode, naics_code, employees, sqft_per_job)
                            business.append(strng)
                else:
                    pass
            else:
                pass
        else:
            pass
    
    g = open(output_file_path, 'w')
    g.write('zipcode, naics_code, employees, sqft_per_job\n')
    g.writelines(business)
    g.close()