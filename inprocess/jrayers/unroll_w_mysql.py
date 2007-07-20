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
# This is the fastest one yet, runs on mysql and inserts 1.14 million records in ~4min

import sys, os, time, datetime
from sqlalchemy import *

env_vars = raw_input('Use environment variables for db login info? (y or n): ')
if env_vars == 'n':
    # Set up variables
    username = raw_input('Enter your db username: ')
    password = raw_input('Enter your db password: ')
    db_server = raw_input('Enter your db server name: ')
elif env_vars == 'y':
    username = os.environ['MYSQLUSERNAME']
    password = os.environ['MYSQLPASSWORD']
    db_server = os.environ['MYSQLHOSTNAME']
else:
    print 'You did not input a y or n...'
    print 'This script will now exit.'
    sys.exit()
db_name = raw_input('Enter your db name: ')
db_table = raw_input('Enter the table name to unroll: ')
field_to_unroll_with = raw_input('Enter the name of the field to unroll with: ')
new_table_name = raw_input('Enter the new table name: ')

timeHere = time.localtime()
readableTime = time.asctime(timeHere)
print '  Starting operation at ' + readableTime

print 'Setting up database connection...'
exec "db = create_engine('mysql://%s:%s@%s/%s')" % (username, password, db_server, db_name)
metadata = BoundMetaData(db)

print 'Reading table...'
table_to_unroll = Table(db_table, metadata, autoload=True)
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
