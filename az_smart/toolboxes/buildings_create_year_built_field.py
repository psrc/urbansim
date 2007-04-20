#imports
import arcgisscripting

#create geoprocessor
gp = arcgisscripting.create()

#specify variables
table = gp.getparameterastext(0)

#Adds specific AZ-SMART toolbox so the next command can be executed
#as a native method on the gp object
gp.addtoolbox("D:/svn_working/az_smart/toolboxes/AZ-SMART - Pima County.tbx")

#creates a new field called 'year_built' and copies the contents of
#the existing 'YEAR' field to it
gp.addmessage("Running duplicate field script....")
gp.DuplicateField(table, "YEAR", "year_built")

#create a table view that only contains records specified
#by the where_clause
gp.addmessage("Making table view....")
where_clause = '"year_built" =0'
gp.MakeTableView(table, "table_view", where_clause)

#calculate
gp.addmessage("Calculating field....")
expression = "[CONSTYR]"
gp.CalculateField("table_view", "year_built", expression)