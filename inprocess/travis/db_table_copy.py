#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

import os
from sqlalchemy \
    import create_engine, Table, Column, MetaData, select, and_
from sqlalchemy.types import Integer, String, Float
from sqlalchemy.sql import func

def connection_string(protocol, database_name, username = None, password = None, 
                      hostname = None, port = None):
    
    if hostname is None:
        hostname = os.environ.get('%sHOSTNAME'%protocol.upper(),'localhost')
    if password is None:
        password = os.environ.get('%sPASSWORD'%protocol.upper(),'')        
    if username is None:
        username = os.environ.get('%sUSERNAME'%protocol.upper(),'')  
    
    if port is None:
        port_string = ''
    else:
        port_string = ':%s' % port
        
    return '%s://%s:%s@%s%s/%s' % (
            protocol,
            username,
            password,
            hostname,
            port_string,
            database_name
            )     

def row_byte_size(table):
    byte_size_type_map = {                          
        Integer:4,
        Float:4,
        String:25 #this is a guess; strings of length 25                  
    }
    byte_size = 0
    for col in table.columns:
        if isinstance(col.type,Integer):
            type_size = 4    
        elif isinstance(col.type,Float):
            type_size = 4
        elif isinstance(col.type,String):
            type_size = 25
        else:
            raise 'unknown col type %s'%repr(col.type)
        byte_size += type_size
        
    return byte_size

def get_primary_key(table):
    if len(table.primary_key) > 1:
        raise 'Composite primary key found for table %s'%table.name
    elif len(table.primary_key) == 0:
        raise 'No primary key found for table %s'%table.name
    
    for primary_key in table.primary_key:
        return primary_key
    
def copy_table(table_to_copy, 
               db_type_in, database_in, 
               db_type_out, database_out, 
               memory_in_gigabytes = 2):        

    str_in = connection_string(protocol = db_type_in,
                               database_name = database_in)
    
    str_out = connection_string(protocol = db_type_out,
                               database_name = database_out)

    in_metadata = MetaData(bind = str_in)
    out_metadata = MetaData(bind = str_out)

    in_table = Table(table_to_copy, in_metadata, autoload=True)
    out_table = in_table.tometadata(out_metadata)
    
    primary_key = get_primary_key(in_table)
    
    out_metadata.create_all()

    memory_in_bytes = memory_in_gigabytes * 1024**3
    
    row_size = row_byte_size(in_table)
    chunk_size = int( .25 * memory_in_bytes / row_size  )
    
    num_rows = in_table.count().execute().fetchone()[0]
    num_inserted_rows = 0
    floor = 2000
    #in_metadata.get_engine().echo = True
    while num_inserted_rows < num_rows:
        ceiling = floor + chunk_size
        print "(%i, %i)"%(floor,ceiling)
        qry = in_table.select(and_(primary_key >= floor,
                                   primary_key < ceiling) )
            
        data = [ dict( (col.key, x[col.name]) for col in in_table.c)
                            for x in qry.execute() ]
    
        out_table.insert().execute(*data)
        num_inserted_rows += len(data)
        floor += chunk_size

    
if __name__=='__main__':
    copy_table(
        table_to_copy = 'parcels',
        db_type_in = 'mysql',
        database_in = 'psrc_2005_parcel_baseyear_change_20070706',
        db_type_out = 'postgres',
        database_out = 'scratch_travis',
    )

#    copy_table(
#        db_type_in = 'postgres',
#        database_in = 'postgis_test',
#        db_type_out = 'postgres',
#        database_out = 'scratch_travis',
#        table_to_copy = 'spatial_ref_sys'
#    )