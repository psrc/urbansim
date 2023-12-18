# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# Author: Jesse Ayers, MAG

from sqlalchemy import create_engine

username = 'AZSMARTExport'
password = 'thebigone'
server = 'MAG1603\AZSMART'
database = 'AZSMART_V5_zone'

engine = create_engine('mssql://%s:%s@%s/%s' % (username, password, server, database))
connection = engine.connect()

# NOTE! in table_names, the non-home-based table must be 1st in the list!!
table_names = ['jesse_import_v5b_zaresults5_sraz_detailed_totnhbemp_2010_2040', 
               'jesse_import_v5b_zaresults5_sraz_detailed_tothbemp_2010_2040']
new_table_name = 'opus_magZoneV5c_baseYearData_2010_annualEmploymentControlTotalsZaresults5'

start_year = 2011
end_year = 2040
years = list(range(start_year, end_year+1))

sector_names = ['01agricultural'
                ,'02mining'
                ,'03utilities'
                ,'04construction'
                ,'05manufacturing'
                ,'06wholesale'
                ,'07retail'
                ,'08transportation'
                ,'09information'
                ,'10finance'
                ,'11realestate'
                ,'12professional'
                ,'13management'
                ,'14administrative'
                ,'15education'
                ,'16healthcare'
                ,'17arts'
                ,'18accomodation'
                ,'19foodservice'
                ,'20other_services'
                ,'21pubfedstate'
                ,'22publocal']

iteration = 0
home_based_status = 0
home_based_status_string = 'nhb'
for table_name in table_names:
    print(home_based_status_string)
    for year in years:
        print('year = %s' % year)
        for sector_name in sector_names:
            sector_id = str(int(sector_name[0:2]))
            if iteration == 0:
                query = '''
                        SELECT
                            %s as year,
                            cast(super_raz_id as int) as super_raz_id,
                            %s as home_based_status,
                            %s as sector_id,
                            cast(cast(number_of_%s_%s_jobs_%s as float) as int) as total_number_of_jobs
                        INTO %s
                        FROM %s j
                        ''' % (year, home_based_status, sector_id, home_based_status_string, sector_name, year, new_table_name, table_name)
            else:
                query = '''
                        INSERT INTO %s
                        SELECT
                            %s as year,
                            cast(super_raz_id as int) as super_raz_id,
                            %s as home_based_status,
                            %s as sector_id,
                            cast(cast(number_of_%s_%s_jobs_%s as float) as int) as total_number_of_jobs
                        FROM %s j
                        ''' % (new_table_name, year, home_based_status, sector_id, home_based_status_string, sector_name, year, table_name)
            result = connection.execute(query)
            iteration += 1
    home_based_status += 1
    home_based_status_string = 'hb'       
        
        
        
        
        