# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from sqlalchemy.schema import Table
from sqlalchemy.types import Integer, String, Numeric

class CrossDatabaseOperations(object):
    
    def _row_byte_size(self, table):
        byte_size = 0
        for col in table.columns:
            if isinstance(col.type,Integer):
                type_size = 4    
            elif isinstance(col.type,Numeric):
                type_size = 4
            elif isinstance(col.type,String):
                type_size = 25
            else:
                raise 'unknown col type %s'%repr(col.type)
            byte_size += type_size
            
        return byte_size
        
    def copy_table(self, table_to_copy, 
                   database_in, database_out,
                   new_table_name = None, 
                   use_chunking = True,
                   memory_in_gigabytes = 2):        
        
        in_metadata = database_in.metadata
        out_metadata = database_out.metadata
    
        in_table = Table(table_to_copy, in_metadata, autoload=True)

        out_table = in_table.tometadata(out_metadata)
        if new_table_name is not None:
            out_table.rename(new_table_name)
        out_metadata.create_all()
            
        if use_chunking:
            memory_in_bytes = memory_in_gigabytes * 1024**2
            
            row_size = self._row_byte_size(in_table)
            chunk_size = int( .1 * memory_in_bytes / row_size  )
            
            num_rows = in_table.count().execute().fetchone()[0]
            num_inserted_rows = 0
    
            while num_inserted_rows < num_rows:
                qry = in_table.select().offset(num_inserted_rows).limit(chunk_size)
                    
                result = qry.execute()
                data = [ dict( (col.key, x[col.name]) for col in in_table.c)
                                    for x in result ]
            
                out_table.insert().execute(*data)
                num_inserted_rows += len(data)

        else:
            qry = in_table.select()
            data = [ dict( (col.key, x[col.name]) for col in in_table.c)
                                    for x in qry.execute() ]   
            out_table.insert().execute(*data) 