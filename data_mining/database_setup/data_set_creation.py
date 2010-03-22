from xml.dom import minidom
import copy
import sys
import math
import random

import MySQLdb
from sqlalchemy import *

NUM_INCRIMENTS = 100

def create_data_set(xml_config_address):
    
    #Loading information from the configuration
    xmldoc = minidom.parse(xml_config_address)
    
    #Getting old table info
    old_table_elem = xmldoc.getElementsByTagName('old_table')[0]
    db_url = old_table_elem.attributes["db_url"].value
    name = old_table_elem.attributes["name"].value
    old_t = util_get_table(db_url, name)
    ot_xcoord = old_table_elem.attributes["x_coord"].value
    ot_ycoord = old_table_elem.attributes["y_coord"].value

    #Creating new table
    new_table_elem = xmldoc.getElementsByTagName('new_table')[0]
    db_url = new_table_elem.attributes["db_url"].value
    name = new_table_elem.attributes["name"].value
    replace_table = new_table_elem.attributes["replace"].value
    data_set_size = int(new_table_elem.attributes["data_set_size"].value)
  
    #Checking if random starting coordinates should be used
    get_rand_coords = new_table_elem.attributes["pick_random_coord"].value == "TRUE"
    start_x = None
    start_y = None
    if not get_rand_coords :
        start_x = float(new_table_elem.attributes["x_coord"].value)
        start_y = float(new_table_elem.attributes["y_coord"].value)
        print "Starting x: ", start_x
        print "Starting y: ", start_y
  
    #Replace the table if one already exists
    db = create_engine(db_url)
    metadata = MetaData(db)
    if db.has_table(name) and replace_table != "TRUE":
        print "ERROR: Table already exists and replacement not specified"
        return -1
    elif db.has_table(name) :
        temp_table = Table(name, metadata, autoload=True)
        temp_table.drop()
        metadata = MetaData(db)  

    #Copying prexisting columns
    column_name_list = []
    copied_columns = []
    for c in old_t.columns :
        column_name_list.append(c.name)
        copied_columns.append(c.copy())

    #Creating new table
    new_table = Table(name, metadata)
    for c in copied_columns :
        new_table.append_column(c)
    new_table.create()   

    #Getting starting points / verifying current ones
    (x_max, y_max, x_min, y_min) = [None, None, None, None]

    s = select([func.max(old_t.c[ot_xcoord])]).execute()
    x_max = sql_get_agg(s, "float")
        
    s = select([func.min(old_t.c[ot_xcoord])]).execute()
    x_min = sql_get_agg(s, "float")
        
    s = select([func.max(old_t.c[ot_ycoord])]).execute()
    y_max = sql_get_agg(s, "float")
        
    s = select([func.min(old_t.c[ot_ycoord])]).execute()
    y_min = sql_get_agg(s, "float")

    if start_x != None :
        if start_x < x_min or start_x > x_max or start_y < y_min or start_y > y_max :
            print "ERROR: starting coordinates are not inside area covered by input table"
            return -1
    else :
        multiplier = 10000
        start_x = float(random.randint(int(x_min*multiplier), int(x_max*multiplier))) / multiplier
        start_y = float(random.randint(int(y_min*multiplier), int(y_max*multiplier))) / multiplier
        print "Starting x: ", start_x
        print "Starting y: ", start_y
        
    x_mult = (x_max - x_min) / NUM_INCRIMENTS
    y_mult = (y_max - y_min) / NUM_INCRIMENTS
 
    cx_max = None
    cx_min = None
    cy_max = None
    cy_min = None
    
    #Finding appropriate coords (increasing size of the block in a linear manner)
    print "Finding appropriate sized block"
    t = old_t
    x = ot_xcoord
    y = ot_ycoord
    for i in range(NUM_INCRIMENTS) :
        a = i + 1
        
        cx_max = start_x + a*x_mult
        cx_min = start_x - a*x_mult
        cy_max = start_y + a*y_mult
        cy_min = start_y - a*y_mult
        
        s = select([func.count("*")], and_(t.c[x] >= cx_min, t.c[x] <= cx_max, t.c[y] >= cy_min, t.c[y] <= cy_max), from_obj=[t]).execute()
        block_count = parcel_count = sql_get_agg(s, "int")  
        print "Block count: ", block_count
        if block_count > data_set_size :
            print "Block selected"
            break
        
    s = t.select(and_(t.c[x] > cx_min, t.c[x] < cx_max, t.c[y] > cy_min, t.c[y] < cy_max)).execute()
        
    #Inputing rows into the new table
    print "Inserting rows"
    row_list = []
    for row in s:
        temp = {}
        for c in old_t.c :
            temp[c.name] = row[c.name]
        row_list.append(temp)
        
        if len(row_list) == 1000 :
            new_table.insert().execute(row_list)
            row_list = []

    if row_list != [] :
        new_table.insert().execute(row_list)
        
def util_get_table(db_url, table_name) :
    #Get SQL connection                                                                                               
    db = create_engine(db_url)
    metadata = MetaData(db)

    #Get the table that is being used
    t = Table(table_name, metadata, autoload=True)
    return t
 
#Returns the value for a count, max, min, etc.
def sql_get_agg(s, type):
    for row in s :
        if type == "int" :
            return int(row[0])
        elif type == "float" :
            return float(row[0])
    

create_data_set(sys.argv[1])