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

start_year = 2011
end_year = 2040
years = list(range(start_year, end_year+1))

table_name = 'adoa_oct19Draft_mediumSeries_population'
new_table_name = 'jesse_test_script_delete_me'

for year in years:
    if year == start_year:
        query = '''
            SELECT
                %s as year,
                UID as race_type_id,
                CASE
                    WHEN age is null THEN 85
                    ELSE age
                END age,
                CASE
                    WHEN gender = 'Female' THEN 2
                    ELSE 1
                END sex,
                round(Proj%s,0) as total_population
            into %s
            FROM %s
            WHERE 
                Place = 'Maricopa County' AND
                AgeGroup IS NOT NULL
                ''' % (year, year, new_table_name, table_name)
    else:
        query = '''
            insert into %s
            SELECT
                %s as year,
                UID as race_type_id,
                CASE
                    WHEN age is null THEN 85
                    ELSE age
                END age,
                CASE
                    WHEN gender = 'Female' THEN 2
                    ELSE 1
                END sex,
                round(Proj%s,0) as total_population
            FROM %s
            WHERE 
                Place = 'Maricopa County' AND
                AgeGroup IS NOT NULL
                ''' % (new_table_name, year, year, table_name)            
    result = connection.execute(query)