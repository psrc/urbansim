#imports
import arcgisscripting, pymssql, os

#create geoprocessor
gp = arcgisscripting.create()

#specify variables
geodb_table = gp.getparameterastext(0)
original_use_field = gp.getparameterastext(1)
vacant_use_code = gp.getparameterastext(2)

path, table = os.path.split(geodb_table)

#create database connection
con = pymssql.connect(host='aarhus',user='sa',password='UwmssqlAt.5',database='sde_pima')

#create a database cursor
gp.addmessage("Creating db cursor....")
cur = con.cursor()

#add and populate 'developable' field with 0
gp.addmessage("Adding 'developable' field and populating with '0'....")
query = "ALTER TABLE %s "\
       "ADD developable smallint null "\
        "DEFAULT 0 WITH VALUES;" % (table)
cur.execute(query)
con.commit()

#calculate those to be developable = 1
gp.addmessage("Calculating 'developable' = 1....")
query = "UPDATE %s "\
        "SET developable = 1 "\
        "WHERE %s = %s;" % (table, original_use_field, vacant_use_code)
cur.execute(query)
con.commit()
con.close()

gp.addmessage("Finised")

## ALL OF THIS WORKS, BUT IS INCREDIBLY SLOW ##
## NEARLY 30 MINUTES TO RUN ##
#imports
#import arcgisscripting

#create geoprocessor
#gp = arcgisscripting.create()

#specify variables
#table = gp.getparameterastext(0)
#original_use_field = gp.getparameterastext(1)
#vacant_use_code = gp.getparameterastext(2)

#add and populate 'developable' field with 0
#gp.addmessage("Adding field....")
#gp.AddField(table, "developable", "short")
#gp.addmessage("Filling field with 0....")
#gp.CalculateField(table, "developable", 0)

#create a table view that only contains records specified
#by the where_clause
#calculate those to be developable = 1
#gp.addmessage("Creating table view....")
#where_clause = '"%s" = %s' % (original_use_field, vacant_use_code)
#gp.MakeTableView(table, "table_view", where_clause)
#p.addmessage("Calculating developable = 1....")
#gp.CalculateField("table_view", "developable", 1)
