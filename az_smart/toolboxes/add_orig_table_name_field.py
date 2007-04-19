#imports
import arcgisscripting, sys, os

#create geoprocessor
gp = arcgisscripting.create()

table = gp.getparameterastext(0)

gp.addmessage("Adding orig_table_name field...")
gp.AddField(table, "orig_table_name", "text", "#", "#", "35", "#", "#", "#", "#")

base, filename = os.path.split(table)

expression = '"%s"' % (filename)

gp.addmessage("Filling in fields with: %s" % (filename))
gp.CalculateField(table, "orig_table_name", expression)

gp.addmessage("FINISHED")