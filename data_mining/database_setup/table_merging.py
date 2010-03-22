from xml.dom import minidom
import copy
import sys

import MySQLdb
from sqlalchemy import *

BlOCK_SIZES = 10000
NUM_ROWS_ADDED = 1000

def combine_tables(xml_config_address):
    
    #Loading information from the configuration
    xmldoc = minidom.parse(xml_config_address)
    table_list = xmldoc.getElementsByTagName('table')
    
    if len(table_list) > 3 :
        print "ERROR: To many tables in the configuration file."
        return 1
    else :
        #Initializing table variables
        #Initializing variables to store what the joined attributes are
        spatial_t, joined_t, new_t = None, None, None
        spatial_ja, joined_ja = None, None
        
        spatial_attributes = []
        joined_attributes = []
        
        #Getting spatial and joined table info
        for element in table_list :
            type = element.attributes["type"].value
            name = element.attributes["name"].value
            
            db_url = element.attributes["db_url"].value
            
            if type == "spatial" :
                spatial_t = util_get_table(db_url, name)
                spatial_ja = element.attributes["join_attribute"].value
                
                attributes_element = element.getElementsByTagName('attributes')[0]
                spatial_attributes = util_get_attribute_list(attributes_element)

            elif type == "joined" :
                joined_t = util_get_table(db_url, name)    
                joined_ja = element.attributes["join_attribute"].value

                attributes_element = element.getElementsByTagName('attributes')[0]
                joined_attributes = util_get_attribute_list(attributes_element)

        #Getting new table info
        for element in table_list :
            type = element.attributes["type"].value
            if type == "new" :
                print "Creating new table"
                #Replace the table if one already exists
                db = create_engine(db_url)
                metadata = MetaData(db)
                if db.has_table(name) :
                    temp_table = Table(name, metadata, autoload=True)
                    temp_table.drop()
                    metadata = MetaData(db)

                #Find redundant columns between spatial and joined
                #Copy spatial columns
                column_name_list = []
                copied_columns = []
                spatial_columns = []
                
                for c in spatial_t.columns :
                    if c.name in spatial_attributes:
                        column_name_list.append(c.name)
                        spatial_columns.append(c.name)
                        
                        copied_c = Column(c.name, c.type) #Avoids having a column considered a PK
                        copied_columns.append(copied_c)
                
                #Add columns from the joined table to the lists
                jtc_mapping = {}
                for c in joined_t.columns :
                    if c.name in joined_attributes :
                        if c.name not in column_name_list :
                            column_name_list.append(c.name)
                            copied_columns.append(c.copy())
                            jtc_mapping[c.name] = c.name
    
                        else :
                            #Creating column name that hasn't been used yet
                            cname = c.name
                            while cname in column_name_list :
                                cname += "x"
                            jtc_mapping[c.name] = cname
    
                            copied_c = Column(cname, c.type)
                                                    
                            column_name_list.append(copied_c.name)
                            copied_columns.append(copied_c)
                        
                #Creating new table
                new_table = Table(name, metadata)
                for c in copied_columns :
                    new_table.append_column(c)
                new_table.create()   
                   
                #Adding rows to the new table
                print "Starting join process"
                count = 0
                current_rows = []
                
                #INCORPORATE BLOCK STUFF EVENTUALLY
                id_set = set([])
                id_mapping = {}
                spatial_rows = []
                
                index = 0
                for s_row in spatial_t.select().execute() :
                    row = {}
                    for c in spatial_columns :
                        row[c] = s_row[c]
                    spatial_rows.append(row)
                        
                    id_set.add(s_row[spatial_ja])
                    id_mapping[s_row[spatial_ja]] = index
                        
                    index += 1
                      
                    if index % 1000 == 0 :
                        print "Indexing Spatial rows: ", index
                        
                print len(spatial_rows)
                    
                for j_row in joined_t.select().execute() :                        
                            
                    #Finding rows with same joined attribute value
                    joined_id = j_row[joined_ja]
                    if joined_id in id_set :
                    
                        s_row = spatial_rows[id_mapping[joined_id]]
                        row = copy.deepcopy(s_row)
                    
                        #Getting joined values
                        for attribute in joined_attributes :
                            row[jtc_mapping[attribute]] = j_row[attribute]

                        current_rows.append(row)
                        count += 1
                            
                    #Inputing new columns
                    if len(current_rows) == NUM_ROWS_ADDED:
                        new_table.insert().execute(current_rows)
                        current_rows = []
                        print "Number of rows added: ", count

                new_table.insert().execute(current_rows)
                        
                        
    return 0

#turns an xml element into a list
def util_get_attribute_list(element):
    list = []
    for node in element.getElementsByTagName('a') :
        list.append(str(node.attributes["name"].value))
    return list

def util_get_table(db_url, table_name) :
    #Get SQL connection                                                                                               
    db = create_engine(db_url)
    metadata = MetaData(db)

    #Get the table that is being used
    t = Table(table_name, metadata, autoload=True)
    return t

combine_tables(sys.argv[1])