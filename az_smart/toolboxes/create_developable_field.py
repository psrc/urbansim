#imports
import arcgisscripting

#create geoprocessor
gp = arcgisscripting.create()

#specify variables
table = gp.getparameterastext(0)
original_use_field = gp.getparameterastext(1)
expression = "int([%s])" % (original_use_field)

#add and populate 'developable' field with 0
gp.AddField(table, "developable", "short")
gp.CalculateField(table, "developable", 0)

#add 'land_use_temp' field
#populate it by integerizing the original_use_field
gp.AddField(table, "land_use_temp", "long")
gp.CalculateField(table, "land_use_temp", expression)

#create a table view that only contains records specified
#by the where_clause
#calculate those to be developable = 1
where_clause = '"land_use_temp" <>0 AND "land_use_temp" >=1 AND "land_use_temp" <=99'
gp.MakeTableView(table, "table_view", where_clause)
gp.CalculateField("table_view", "developable", 1)

#delete 'land_use_temp' field
gp.DeleteField(table, "land_use_temp")