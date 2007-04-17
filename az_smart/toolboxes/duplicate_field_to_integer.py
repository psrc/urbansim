#imports
import arcgisscripting

#create geoprocessor
gp = arcgisscripting.create()

table = gp.getparameterastext(0)
field = gp.getparameterastext(1)
new_field_name = gp.getparameterastext(2)

gp.AddField(table, new_field_name, "long", "#", "#", "#", "#", "#", "#", "#")

#this will duplicate the contents
expression = "int([%s])" % (field)
gp.CalculateField(table, new_field_name, expression)
