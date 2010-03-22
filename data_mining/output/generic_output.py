import copy

import MySQLdb
from sqlalchemy import *

NUM_INSERTS = 1000

class Output_manager :
    def __init__(self, xml_elem, query_manager, column_list):

        overwrite_table = True
        self.db_url = None
        self.table_name= None
        if xml_elem != None :
            #Getting info from xml
            self.db_url = xml_elem.attributes["output_db_url"].value
            self.table_name = xml_elem.attributes["output_table_name"].value
            
            #Getting info on whether table should be overwritten
            if xml_elem.hasAttribute("overwrite_table") and xml_elem.attributes["overwrite_table"].value == "FALSE" :
                overwrite_table = False
        else :
            #Query manager info
            self.db_url = query_manager.db_url
            self.table_name = query_manager.table_name + "_new"
        
        #Get SQL connection                                                                    
        db = create_engine(self.db_url)
        metadata = MetaData(db)
        
        
        #Checking if table already exists (only removing it if told to)
        if db.has_table(self.table_name) and overwrite_table:
            temp_table = Table(self.table_name, metadata, autoload=True)
            temp_table.drop()
            metadata = MetaData(db)
        
        #If table doesn't exist then creating a new one
        if not db.has_table(self.table_name) :
            #Initializing table
            table = Table(self.table_name, metadata)
            for c in column_list :
                table.append_column(c)
            table.create()
        
            self.table = table
        #If table does exist then checking if it is compatible
        else :
            table = Table(self.table_name, metadata, autoload=True)
    
            #Checking if the table has exactly the right columns
            temp = copy.deepcopy(column_list)
            tables_equal = True
            for c in table.columns :
                if c.name in temp :
                    temp.remove(c.name)
                else :
                    tables_equal = False
            if len(temp) != 0 :
                tables_equal = False
    
            if tables_equal :
                self.table = table
            else :
                self.table = None
                
    #Insert rows into the output table
    def insert_rows(self, list_rows):
        count = 0
        temp_list = []
        for row in list_rows :

            temp_list.append(row)
            count += 1

            if count % NUM_INSERTS == 0 :
                self.table.insert().execute(temp_list)
                temp_list = []
        
        self.table.insert().execute(temp_list)
        
        return 0
    
