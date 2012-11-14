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
table_name = 'jesse_import_v5b_zaresults5_sraz_pop_emp_2010_2040' 
new_table_name = 'opus_magZoneV5c_baseYearData_2010_annualHouseholdControlTotalsZaresults5'

start_year = 2011
end_year = 2040
years = range(start_year, end_year+1)

iteration = 0
for year in years:
    print 'year = %s' % year
    if iteration == 0:
        query = '''
                SELECT 
                    %s as year,
                    cast(super_raz_id as int) as super_raz_id,
                    cast(sraz_total_population_%s as int) as total_population
                INTO %s
                FROM %s
                ''' % (year, year, new_table_name, table_name)
    else:
        query = '''
                INSERT INTO %s
                SELECT 
                    %s as year,
                    cast(super_raz_id as int) as super_raz_id,
                    cast(sraz_total_population_%s as int) as total_population
                FROM %s
                ''' % (new_table_name, year, year, table_name)
    result = connection.execute(query)
    iteration += 1

        
        
        
        