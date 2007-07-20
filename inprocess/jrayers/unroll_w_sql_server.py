# First attempt to allow MSSQL

import sys, os, time, datetime
from sqlalchemy import *

username = #os.environ['MYSQLUSERNAME']
password = #os.environ['MYSQLPASSWORD']
db_server = #os.environ['MYSQLHOSTNAME']
db_name = 
db_table = 
field_to_unroll_with = 
new_table_name =

timeHere = time.localtime()
readableTime = time.asctime(timeHere)
print '  Starting operation at ' + readableTime

print 'Setting up database connection...'
exec "db = create_engine('mssql://%s:%s@%s/%s')" % (username, password, db_server, db_name)
metadata = BoundMetaData(db)

print 'Reading table...'
table_to_unroll = Table(db_table, metadata, autoload=True, schema='sde') #TODO: fix hardcoded schema
s = table_to_unroll.select()
e = s.execute()
rows = e.fetchall()

print 'Creating list of column objects...'
table_to_unroll_columns = list(table_to_unroll.columns)

print 'Creating list of column names...'
table_to_unroll_column_names= []
for i in table_to_unroll_columns:
    table_to_unroll_column_names.append(i.name)

#print 'Unrolling rows...'
#rows_unrolled = []
#for i in rows:
#    for j in range(i[table_to_unroll_column_names.index(field_to_unroll_with)]):
#        rows_unrolled.append(i)

print 'Creating new table...'
metadata2 = BoundMetaData(db)
new_table = table_to_unroll.tometadata(metadata2)
new_table.name = new_table_name
new_table.create()

print 'Unrolling rows, converting, and inserting...'
for i in rows:
    rows_unrolled = []
    for j in range(i[table_to_unroll_column_names.index(field_to_unroll_with)]):
        rows_unrolled.append(i)
    else:
        rows_unrolled_as_dicts = []
        for k in rows_unrolled:
            x = zip(table_to_unroll_column_names, k)
            y = dict(x)
            rows_unrolled_as_dicts.append(y)
        else:
            new_table.insert().execute(rows_unrolled_as_dicts)


#print 'Converting unrolled rows to a list of dictionaries...'
#rows_as_dicts = []
#for i in rows_unrolled:
#    x = zip(table_to_unroll_column_names, i)
#    y = dict(x)
#    rows_as_dicts.append(y)

#print 'Inserting records into new table...'
#new_table.insert().execute(rows_as_dicts)

timeHere = time.localtime()
readableTime = time.asctime(timeHere)
print '  Operation ended at ' + readableTime
