import os
from sqlalchemy import create_engine, MetaData

table_to_copy = 'cnty_outline_arc'
select_str = 'select * from'+table_to_copy
meta = MetaData()

db_type_in = 'mysql'
host_name_in = os.environ.get('MYSQLHOSTNAME','localhost')
user_name_in = os.environ.get('MYSQLUSERNAME','')
password_in = os.environ.get('MYSQLPASSWORD','')
database_in = 'psrc_2005_parcel_baseyear_change_20070706'
str_in = db_type_in+'://'+user_name_in+':'+password_in+'@'+host_name_in+':/'+database_in
engine_in = create_engine(str_in)
meta_in = meta.connect(engine_in)

db_type_out = 'postgres'
host_name_out = os.environ.get('PGSQLHOSTNAME','localhost')
user_name_out = os.environ.get('PGSQLUSERNAME','')
password_out = os.environ.get('PGSQLPASSWORD','')
database_out = 'gisdata'
str_out = db_type_out+'://'+user_name_out+':'+password_out+'@'+host_name_out+':/'+database_out
engine_out = create_engine(str_out)
meta_out = meta.connect(engine_out)


connection_out = engine_out.connect()
result = connection_out.execute(select_str) 
print result