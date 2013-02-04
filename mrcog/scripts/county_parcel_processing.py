import numpy as np
import pandas as pd
import pandas.io.sql as sql
import psycopg2

building_tables = []

parcel_tables = []

conn_string = "dbname='postgis_test' user='postgres'"
conn = psycopg2.connect(conn_string)
df = sql.read_frame('select land_use_code, objectid, gen_tax_lu, aprland, aprimp, mf_units, res_sqft, comm_sqft, total_sqft, mean_yrblt, acres_shap, dasz2010 from santafe_parcels_lu_zone', conn)

df.gen_tax_lu[df.gen_tax_lu.isnull()] = 'unknown'
df.land_use_code[df.land_use_code.isnull()] = 0

df['residential_units'] = (df.mf_units>0)*df.mf_units + (df.mf_units<1)*(df.res_sqft>0) + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('R') + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('SR') + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('CRE')  + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('LOT')

df['non_residential_sqft'] = df.comm_sqft

df['improvement_value'] = df.aprimp

df['year_built'] = df.mean_yrblt

df['sqft_per_unit'] = df.res_sqft*1.0 / df.residential_units

df.sqft_per_unit[df.sqft_per_unit.isnull()] = 0

num_parcels1 = df.objectid.size

df['parcel_id'] = np.arange(num_parcels1) + 1

#for parcel table

df['land_value'] = df.aprland

df['parcel_acres'] = df.acres_shap

df['zone_id'] = df.dasz2010

df['county_id'] = 3

df['residential'] = (df.residential_units>0)*1

df.residential[df.mf_units>0]=2

df['has_square_footage_or_units'] = ((df.residential_units + df.non_residential_sqft + df.improvement_value + df.year_built) > 0)*1

df.land_use_code = df.land_use_code.astype('i8')

df['building_type_id'] = df.land_use_code * df.has_square_footage_or_units

df.residential_units[(df.building_type_id==2)*(df.residential_units>0)*(df.residential_units<3)]=3

buildings = df[df.building_type_id>0]

buildings['btype']=0

#SINGLE-FAMILY
buildings.residential_units[(buildings.building_type_id == 1)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=1
buildings.btype[(buildings.building_type_id == 1)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.residential_units>0)]=1

#MULTI-FAMILY
buildings.residential_units[(buildings.building_type_id == 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=3
buildings.btype[(buildings.building_type_id == 2)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.residential_units>0)]=2

buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==1)]=1
buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units>1)]=2

buildings.btype[(buildings.building_type_id == 3)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=3
buildings.btype[(buildings.building_type_id == 4)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=4
buildings.btype[(buildings.building_type_id == 5)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=5
buildings.btype[(buildings.building_type_id == 6)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=6
buildings.btype[(buildings.building_type_id == 7)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=7
buildings.btype[(buildings.building_type_id == 8)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=8
buildings.btype[(buildings.building_type_id == 9)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=9
buildings.btype[(buildings.building_type_id == 10)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=10
buildings.btype[(buildings.building_type_id == 11)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=11
buildings.btype[(buildings.building_type_id == 12)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 13)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=13
buildings.btype[(buildings.building_type_id == 14)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 15)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 16)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=16
buildings.btype[(buildings.building_type_id == 17)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=17
buildings.btype[(buildings.building_type_id == 18)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=18
buildings.btype[(buildings.building_type_id == 19)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=19
buildings.btype[(buildings.building_type_id == 20)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=20
buildings.btype[(buildings.building_type_id == 31)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=31
buildings.btype[(buildings.building_type_id == 41)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 51)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=51
buildings.btype[(buildings.building_type_id == 61)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=61

buildings.btype[(buildings.building_type_id > 100)]=99

buildings.building_type_id = buildings.btype

buildings = buildings[['residential_units','non_residential_sqft','improvement_value','year_built','sqft_per_unit','parcel_id','building_type_id']]

buildings['building_id']= np.arange(buildings.parcel_id.size) + 1

df['land_use_type_id'] = df.land_use_code

parcels = df[['land_use_type_id','objectid','parcel_id','land_value','parcel_acres','zone_id','county_id']]

building_tables.append(buildings)

parcel_tables.append(parcels)

#buildings.to_csv('buildings_bernalillo.csv')
#parcels.to_csv('parcels_bernalillo.csv')

import numpy as np
import pandas as pd
import pandas.io.sql as sql
import psycopg2

conn_string = "dbname='postgis_test' user='postgres'"
conn = psycopg2.connect(conn_string)
df = sql.read_frame('select land_use_code, objectid, gen_tax_lu, aprland, aprimp, mf_units, res_sqft, comm_sqft, total_sqft, mean_yrblt, acres_shap, dasz2010 from valencia_parcels_lu_zone', conn)

df.gen_tax_lu[df.gen_tax_lu.isnull()] = 'unknown'
df.land_use_code[df.land_use_code.isnull()] = 0

df['residential_units'] = (df.mf_units>0)*df.mf_units + (df.mf_units<1)*(df.res_sqft>0) + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('R') + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('SR')

df['non_residential_sqft'] = df.comm_sqft

df['improvement_value'] = df.aprimp

df['year_built'] = df.mean_yrblt

df['sqft_per_unit'] = df.res_sqft*1.0 / df.residential_units

df.sqft_per_unit[df.sqft_per_unit.isnull()] = 0

num_parcels2 = df.objectid.size

df['parcel_id'] = np.arange(num_parcels2) + 1 + num_parcels1

#for parcel table

df['land_value'] = df.aprland

df['parcel_acres'] = df.acres_shap

df['zone_id'] = df.dasz2010

df['county_id'] = 5

df['residential'] = (df.residential_units>0)*1

df.residential[df.mf_units>0]=2

df['has_square_footage_or_units'] = ((df.residential_units + df.non_residential_sqft + df.improvement_value + df.year_built) > 0)*1

df.land_use_code = df.land_use_code.astype('i8')

df['building_type_id'] = df.land_use_code * df.has_square_footage_or_units

df.residential_units[(df.building_type_id==2)*(df.residential_units>0)*(df.residential_units<3)]=3

buildings = df[df.building_type_id>0]

buildings['btype']=0

#SINGLE-FAMILY
buildings.residential_units[(buildings.building_type_id == 1)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=1
buildings.btype[(buildings.building_type_id == 1)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.residential_units>0)]=1

#MULTI-FAMILY
buildings.residential_units[(buildings.building_type_id == 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=3
buildings.btype[(buildings.building_type_id == 2)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.residential_units>0)]=2

buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==1)]=1
buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units>1)]=2

buildings.btype[(buildings.building_type_id == 3)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=3
buildings.btype[(buildings.building_type_id == 4)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=4
buildings.btype[(buildings.building_type_id == 5)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=5
buildings.btype[(buildings.building_type_id == 6)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=6
buildings.btype[(buildings.building_type_id == 7)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=7
buildings.btype[(buildings.building_type_id == 8)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=8
buildings.btype[(buildings.building_type_id == 9)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=9
buildings.btype[(buildings.building_type_id == 10)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=10
buildings.btype[(buildings.building_type_id == 11)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=11
buildings.btype[(buildings.building_type_id == 12)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 13)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=13
buildings.btype[(buildings.building_type_id == 14)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 15)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 16)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=16
buildings.btype[(buildings.building_type_id == 17)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=17
buildings.btype[(buildings.building_type_id == 18)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=18
buildings.btype[(buildings.building_type_id == 19)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=19
buildings.btype[(buildings.building_type_id == 20)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=20
buildings.btype[(buildings.building_type_id == 31)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=31
buildings.btype[(buildings.building_type_id == 41)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 51)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=51
buildings.btype[(buildings.building_type_id == 61)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=61

buildings.building_type_id = buildings.btype

buildings = buildings[['residential_units','non_residential_sqft','improvement_value','year_built','sqft_per_unit','parcel_id','building_type_id']]

buildings['building_id']= np.arange(buildings.parcel_id.size) + 1

df['land_use_type_id'] = df.land_use_code

parcels = df[['land_use_type_id','objectid','parcel_id','land_value','parcel_acres','zone_id','county_id']]

building_tables.append(buildings)

parcel_tables.append(parcels)

#buildings.to_csv('buildings_bernalillo.csv')
#parcels.to_csv('parcels_bernalillo.csv')

import numpy as np
import pandas as pd
import pandas.io.sql as sql
import psycopg2

conn_string = "dbname='postgis_test' user='postgres'"
conn = psycopg2.connect(conn_string)
df = sql.read_frame('select land_use_code, objectid, gen_tax_lu, aprland, aprimp, mf_units, res_sqft, comm_sqft, total_sqft, mean_yrblt, acres_shap, dasz2010 from bernalillo_parcels_lu_zone', conn)

df.gen_tax_lu[df.gen_tax_lu.isnull()] = 'unknown'
df.land_use_code[df.land_use_code.isnull()] = 0

df['residential_units'] = (df.mf_units>0)*df.mf_units + (df.mf_units<1)*(df.res_sqft>0) + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('R') + (df.mf_units<1)*(df.res_sqft<1)*df['gen_tax_lu'].str.startswith('SR')

df['non_residential_sqft'] = df.comm_sqft

df['improvement_value'] = df.aprimp

df['year_built'] = df.mean_yrblt

df['sqft_per_unit'] = df.res_sqft*1.0 / df.residential_units

df.sqft_per_unit[df.sqft_per_unit.isnull()] = 0

num_parcels3 = df.objectid.size

df['parcel_id'] = np.arange(num_parcels3) + 1 + num_parcels1 + num_parcels2

#for parcel table

df['land_value'] = df.aprland

df['parcel_acres'] = df.acres_shap

df['zone_id'] = df.dasz2010

df['county_id'] = 1

df['residential'] = (df.residential_units>0)*1

df.residential[df.mf_units>0]=2

df['has_square_footage_or_units'] = ((df.residential_units + df.non_residential_sqft + df.improvement_value + df.year_built) > 0)*1

df.land_use_code = df.land_use_code.astype('i8')

df['building_type_id'] = df.land_use_code * df.has_square_footage_or_units

df.residential_units[(df.building_type_id==2)*(df.residential_units>0)*(df.residential_units<3)]=3

buildings = df[df.building_type_id>0]

buildings['btype']=0

#SINGLE-FAMILY
buildings.residential_units[(buildings.building_type_id == 1)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=1
buildings.btype[(buildings.building_type_id == 1)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.residential_units>0)]=1

#MULTI-FAMILY
buildings.residential_units[(buildings.building_type_id == 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==0)]=3
buildings.btype[(buildings.building_type_id == 2)*(buildings.non_residential_sqft>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.improvement_value>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 1)*(buildings.year_built>0)*(buildings.residential_units==0)]=99
buildings.btype[(buildings.building_type_id == 2)*(buildings.residential_units>0)]=2

buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units==1)]=1
buildings.btype[(buildings.building_type_id > 2)*(buildings.non_residential_sqft==0)*(buildings.residential_units>1)]=2

buildings.btype[(buildings.building_type_id == 3)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=3
buildings.btype[(buildings.building_type_id == 4)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=4
buildings.btype[(buildings.building_type_id == 5)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=5
buildings.btype[(buildings.building_type_id == 6)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=6
buildings.btype[(buildings.building_type_id == 7)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=7
buildings.btype[(buildings.building_type_id == 8)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=8
buildings.btype[(buildings.building_type_id == 9)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=9
buildings.btype[(buildings.building_type_id == 10)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=10
buildings.btype[(buildings.building_type_id == 11)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=11
buildings.btype[(buildings.building_type_id == 12)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 13)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=13
buildings.btype[(buildings.building_type_id == 14)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 15)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 16)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=16
buildings.btype[(buildings.building_type_id == 17)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=17
buildings.btype[(buildings.building_type_id == 18)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=18
buildings.btype[(buildings.building_type_id == 19)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=19
buildings.btype[(buildings.building_type_id == 20)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=20
buildings.btype[(buildings.building_type_id == 31)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=31
buildings.btype[(buildings.building_type_id == 41)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=99
buildings.btype[(buildings.building_type_id == 51)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=51
buildings.btype[(buildings.building_type_id == 61)*(((buildings.residential_units==0)+(buildings.non_residential_sqft>0))>0)]=61

buildings.building_type_id = buildings.btype

buildings = buildings[['residential_units','non_residential_sqft','improvement_value','year_built','sqft_per_unit','parcel_id','building_type_id']]

buildings['building_id']= np.arange(buildings.parcel_id.size) + 1

df['land_use_type_id'] = df.land_use_code

parcels = df[['land_use_type_id','objectid','parcel_id','land_value','parcel_acres','zone_id','county_id']]

building_tables.append(buildings)

parcel_tables.append(parcels)

#buildings.to_csv('buildings_bernalillo.csv')
#parcels.to_csv('parcels_bernalillo.csv')

buildings = pd.concat(building_tables)

parcels = pd.concat(parcel_tables)

#parcels['parcel_id'] = np.arange(parcels.objectid.size) + 1

buildings['building_id']= np.arange(buildings.parcel_id.size) + 1

buildings.to_csv('buildings_regional.csv')
parcels.to_csv('parcels_regional.csv')

####################

conn_string = "host='192.168.1.14' dbname='mrcog' user='urbanvision' password='Visua1ization' port=5433"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

#load buildings to db
field_names = buildings.columns.values
str = ''
for name in field_names:
    str = str + name + ','
field_names = str[:-1]
num_fields = buildings.columns.size
placeholder_s = '%s,'*(num_fields - 1) + '%s'
for idx, row in buildings.iterrows():
    i = 0
    to_tuple = []
    while i < num_fields:
        to_tuple.append(row.values[i])
        i = i + 1
    to_tuple = tuple(to_tuple)
    insert_query = "insert into buildings (" + field_names + ") values (" + placeholder_s + ")"
    insert_query = (insert_query) % (to_tuple)
    cursor.execute(insert_query)
    conn.commit()
    
#load parcels to db
field_names = parcels.columns.values
str = ''
for name in field_names:
    str = str + name + ','
field_names = str[:-1]
num_fields = parcels.columns.size
placeholder_s = '%s,'*(num_fields - 1) + '%s'
for idx, row in parcels.iterrows():
    i = 0
    to_tuple = []
    while i < num_fields:
        to_tuple.append(row.values[i])
        i = i + 1
    to_tuple = tuple(to_tuple)
    insert_query = "insert into parcels (" + field_names + ") values (" + placeholder_s + ")"
    insert_query = (insert_query) % (to_tuple)
    cursor.execute(insert_query)
    conn.commit()



