from xml.dom import minidom
import copy
import sys
import math

import MySQLdb
from sqlalchemy import *

class LogTransform :
    
    def __init__(self, element) :
        self.name = element.attributes["name"].value
        self.attribute = element.attributes["attribute"].value

    def get_column(self):
        return Column(self.name, Numeric)

    def set_value(self, row, temp_row):
        trans = 0.0
        if row[self.attribute] > 0 :
            trans = math.log(row[self.attribute] + 1)
            trans = float("%.2f" % trans)
        temp_row[self.name] = trans

class Ratio :
    
    def __init__(self, element) :
        self.name = element.attributes["name"].value
        self.attribute1 = element.attributes["attribute1"].value
        self.attribute2 = element.attributes["attribute2"].value

    def get_column(self):
        return Column(self.name, Numeric)

    def set_value(self, row, temp_row):
        v1 = row[self.attribute1]
        v2 = row[self.attribute2]
        end_value = 0.0
        if v1 > 0 and v2 > 0 :
            end_value = float(v1) / v2
            end_value = float("%.2f" % end_value)

        temp_row[self.name] = end_value

class SuperCategory :
    
    def __init__(self, element) :
        self.name = element.attributes["name"].value
        self.value_dict = {}
        self.other_value = "null"

        for val_element in element.getElementsByTagName('value') :
            if val_element.attributes["type"].value == "defined" :
                temp_list = []
                for sv_elem in val_element.getElementsByTagName('tc') :
                    temp_dict = {}
                    temp_dict["attribute"] = sv_elem.attributes["attribute"].value
                    temp_dict["type"] = sv_elem.attributes["type"].value
                    
                    vt = sv_elem.attributes["vt"].value
                    if vt == "string" :
                        temp_dict["value"] = str(sv_elem.attributes["value"].value)
                    elif vt == "numeric" :
                        temp_dict["value"] = float(sv_elem.attributes["value"].value)
                    
                    temp_list.append(temp_dict)

                self.value_dict[val_element.attributes["name"].value] = temp_list

            elif val_element.attributes["type"].value == "other" :
                self.other_value = val_element.attributes["name"].value
    
    def get_column(self):
        return Column(self.name, UnicodeText(20))

    def set_value(self, row, temp_row):
        found_value = False
        for value, info_list in self.value_dict.items() :
            stop_searching = False
            for criteria in info_list :
                if criteria["type"] == "E" and row[criteria["attribute"]] == criteria["value"] :
                    temp_row[self.name] = value
                    stop_searching = True
                    found_value = True
                    break
                elif criteria["type"] == "NE" and row[criteria["attribute"]] != criteria["value"] :
                    temp_row[self.name] = value
                    stop_searching = True
                    found_value = True
                    break

            if stop_searching :
                break
                              
        if not found_value :
            temp_row[self.name] = self.other_value

class EmptyFeature :
    
    def __init__(self, element) :
        self.name = element.attributes["name"].value
        self.type = element.attributes["value_type"].value

        self.null_value = None
        if self.type == "string" :
            self.null_value = ""
        elif self.type == "numeric" :
            self.null_value = -1.0
   
    def get_column(self):
        if self.type == "string" :
            return Column(self.name, UnicodeText(100))
        elif self.type == "numeric" :
            return Column(self.name, Numeric)

    def set_value(self, row, temp_row):
        temp_row[self.name] = self.null_value

NUM_ROWS_ADDED = 1000

def create_features(xml_config_address):
    
    #Loading information from the configuration
    xmldoc = minidom.parse(xml_config_address)
    
    #Getting old table info
    old_table_elem = xmldoc.getElementsByTagName('old_table')[0]
    db_url = old_table_elem.attributes["db_url"].value
    name = old_table_elem.attributes["name"].value
    old_t = util_get_table(db_url, name)

    #Creating new table
    new_table_elem = xmldoc.getElementsByTagName('new_table')[0]
    db_url = new_table_elem.attributes["db_url"].value
    name = new_table_elem.attributes["name"].value
    replace_table = new_table_elem.attributes["replace"].value
  
    #Replace the table if one already exists
    db = create_engine(db_url)
    metadata = MetaData(db)
    if db.has_table(name) and replace_table != "TRUE":
        print("ERROR: Table already exists and replacement not specified")
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
                
    #Getting creation object
    new_feature_elements = xmldoc.getElementsByTagName('new_feature')
    new_feature_list = []
    for feature in new_feature_elements :
        type = feature.attributes["type"].value
        nf = None
        if type == "log_trans" :
            nf = LogTransform(feature)
        elif type == "ratio" :
            nf = Ratio(feature)
        elif type == "super_category" :
            nf = SuperCategory(feature)
        elif type == "empty_feature" :
            nf = EmptyFeature(feature)
            
        if nf != None :
            new_feature_list.append(nf)
            copied_columns.append(nf.get_column())
    
    #Creating new table
    new_table = Table(name, metadata)
    for c in copied_columns :
        new_table.append_column(c)
    new_table.create()   
    
    #Add rows with new columns
    print("Inserting rows into new table...")
    current_rows = [] 
    count = 0                              
    for row in old_t.select().execute() :                        
        temp_row = {}      
        for column in column_name_list : 
            temp_row[column] = row[column]

        for nf in new_feature_list :
            nf.set_value(row, temp_row)

        current_rows.append(temp_row)
        count += 1

        if len(current_rows) == NUM_ROWS_ADDED:
            new_table.insert().execute(current_rows)
            current_rows = []
            print("Number of rows added: ", count)

    new_table.insert().execute(current_rows)
                                         
    return 0

def util_get_table(db_url, table_name) :
    #Get SQL connection                                                                                               
    db = create_engine(db_url)
    metadata = MetaData(db)

    #Get the table that is being used
    t = Table(table_name, metadata, autoload=True)
    return t

create_features(sys.argv[1])